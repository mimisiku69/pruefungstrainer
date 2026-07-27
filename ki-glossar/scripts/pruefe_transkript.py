#!/usr/bin/env python3
"""Prüft ein Transkript gegen das Hörfehler-Register und meldet nur die Funde.

Zweck: Zoom-/Teams-Mitschriften verhören englische KI-Begriffe systematisch
(zum Beispiel "Meschin Lörning" statt "Machine Learning"). Dieses Skript läuft
lokal über daten/hoerfehler.json und meldet je Fund die Zeilennummer, die
gefundene Falschform und die richtige Zielform. Es lädt nichts in den Kontext,
was nicht Fund ist.

Aufruf:
    python3 scripts/pruefe_transkript.py TRANSKRIPT.txt
    python3 scripts/pruefe_transkript.py TRANSKRIPT.txt --json
    python3 scripts/pruefe_transkript.py TRANSKRIPT.txt --begriffe   # zusätzlich: welche Glossarbegriffe kommen vor

Unterstützt reine Textdateien (.txt, .vtt, .srt, .md). Für .docx vorher den
Text extrahieren.
"""
import argparse
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
DATEN = os.path.normpath(os.path.join(HIER, "..", "daten"))
HOERFEHLER = os.path.join(DATEN, "hoerfehler.json")
GLOSSAR = os.path.join(DATEN, "glossar.json")

# Wortgrenze inkl. deutscher Umlaute (Python \b kennt sie, ist aber bei
# gemischten Grenzen unzuverlässig; wir setzen eigene Lookarounds).
WORT = r"[0-9A-Za-zÄÖÜäöüß]"


def lade(datei):
    with open(datei, encoding="utf-8") as fh:
        return json.load(fh)


def baue_muster(register):
    """Ein kompiliertes Muster je Falschform, längste zuerst (Phrasen vor Wörtern)."""
    muster = []
    for eintrag in register["eintraege"]:
        for falsch in eintrag.get("falsch", []):
            pat = re.compile(
                rf"(?<!{WORT})" + re.escape(falsch) + rf"(?!{WORT})",
                re.IGNORECASE,
            )
            muster.append((len(falsch), falsch, pat, eintrag))
    muster.sort(key=lambda x: -x[0])
    return muster


def main():
    ap = argparse.ArgumentParser(description="Transkript gegen Hörfehler-Register prüfen")
    ap.add_argument("transkript", help="Pfad zur Transkriptdatei (Text)")
    ap.add_argument("--json", action="store_true", help="Funde als JSON")
    ap.add_argument("--begriffe", action="store_true",
                    help="zusätzlich vorkommende Glossarbegriffe auflisten")
    args = ap.parse_args()

    if not os.path.exists(args.transkript):
        print(f"Datei nicht gefunden: {args.transkript}", file=sys.stderr)
        sys.exit(1)

    register = lade(HOERFEHLER)
    muster = baue_muster(register)

    with open(args.transkript, encoding="utf-8", errors="replace") as fh:
        zeilen = fh.readlines()

    funde = []
    for nr, zeile in enumerate(zeilen, start=1):
        # Pro Zeile jede Trefferposition nur einmal (längste Phrase gewinnt).
        belegt = [False] * len(zeile)
        for _, falsch, pat, eintrag in muster:
            for m in pat.finditer(zeile):
                if any(belegt[m.start():m.end()]):
                    continue
                for i in range(m.start(), m.end()):
                    belegt[i] = True
                funde.append({
                    "zeile": nr,
                    "gefunden": m.group(0),
                    "richtig": eintrag["richtig"],
                    "slug": eintrag.get("slug", ""),
                    "hinweis": eintrag.get("hinweis", ""),
                })

    if args.json:
        print(json.dumps(funde, ensure_ascii=False, indent=2))
    else:
        if not funde:
            print("Keine Hörfehler gefunden.")
        else:
            print(f"{len(funde)} mögliche Hörfehler:\n")
            for f in funde:
                extra = f"  ({f['hinweis']})" if f["hinweis"] else ""
                print(f"  Zeile {f['zeile']:>4}: „{f['gefunden']}“  →  {f['richtig']}{extra}")

    if args.begriffe:
        glossar = lade(GLOSSAR)
        text = "".join(zeilen).lower()
        vorhanden = []
        for e in glossar["eintraege"]:
            kandidaten = [e["name"]] + e.get("synonyms", [])
            for k in kandidaten:
                if re.search(rf"(?<!{WORT}){re.escape(k)}(?!{WORT})", text, re.IGNORECASE):
                    vorhanden.append(e["name"])
                    break
        vorhanden = sorted(set(vorhanden))
        print(f"\nVorkommende Glossarbegriffe ({len(vorhanden)}):")
        for n in vorhanden:
            print("  " + n)

    sys.exit(0 if not funde else 2)


if __name__ == "__main__":
    main()
