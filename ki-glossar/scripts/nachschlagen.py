#!/usr/bin/env python3
"""Schlägt Begriffe im KI-Glossar nach und gibt NUR die Treffer aus.

Zweck: Kontextsparsamkeit. Der Glossarbestand (536 Einträge) wird nie ganz in
den Kontext geladen. Dieses Skript liest daten/glossar.json und gibt nur die
angefragten Einträge aus.

Beispiele:
    python3 scripts/nachschlagen.py "Prompt Engineering"
    python3 scripts/nachschlagen.py Halluzination Token Embedding
    python3 scripts/nachschlagen.py "RAG" --voll
    python3 scripts/nachschlagen.py --kategorie "Recht & Regulatorik"
    python3 scripts/nachschlagen.py "Agent" --json
    python3 scripts/nachschlagen.py --suche "Datenschutz"     # Volltext in teaser/body

Matching (in dieser Reihenfolge, Groß/Klein egal):
    1. exakt auf name, slug oder ein Synonym
    2. Teilstring in name oder Synonym
Mehrdeutige Kurzsuchen liefern eine kompakte Trefferliste, kein Volltext.
"""
import argparse
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
JSON_DATEI = os.path.normpath(os.path.join(HIER, "..", "daten", "glossar.json"))


def lade():
    with open(JSON_DATEI, encoding="utf-8") as fh:
        return json.load(fh)


def norm(s):
    return (s or "").strip().lower()


def finde(entries, begriff):
    b = norm(begriff)
    exakt, teil = [], []
    for e in entries:
        namen = [e["name"], e["slug"]] + e.get("synonyms", [])
        namen_n = [norm(x) for x in namen]
        if b in namen_n:
            exakt.append(e)
        elif any(b in x for x in namen_n):
            teil.append(e)
    return exakt, teil


def volltextsuche(entries, begriff):
    b = norm(begriff)
    return [e for e in entries
            if b in norm(e.get("teaser")) or b in norm(e.get("body"))
            or b in norm(e.get("name"))]


def zeile_kompakt(e):
    return f"- {e['name']}  [{e['category']}]  ({e['slug']})\n    {e['teaser']}"


def block_voll(e, entries_by_slug):
    zeilen = [f"### {e['name']}   [{e['category']}]"]
    if e.get("synonyms"):
        zeilen.append("Schreibweisen/Synonyme: " + ", ".join(e["synonyms"]))
    zeilen.append("")
    zeilen.append(e.get("teaser", ""))
    if e.get("body"):
        zeilen.append("")
        zeilen.append(e["body"])
    if e.get("example"):
        zeilen.append("")
        zeilen.append("Beispiel: " + e["example"])
    if e.get("related"):
        namen = [entries_by_slug.get(s, {}).get("name", s) for s in e["related"]]
        zeilen.append("")
        zeilen.append("Verwandt: " + ", ".join(namen))
    if e.get("source"):
        zeilen.append("Quelle: " + e["source"])
    return "\n".join(zeilen)


def main():
    ap = argparse.ArgumentParser(description="KI-Glossar nachschlagen")
    ap.add_argument("begriffe", nargs="*", help="ein oder mehrere Begriffe")
    ap.add_argument("--voll", action="store_true", help="vollen Eintrag ausgeben")
    ap.add_argument("--kategorie", help="alle Namen einer Kategorie auflisten")
    ap.add_argument("--suche", help="Volltextsuche in teaser/body")
    ap.add_argument("--json", action="store_true", help="Treffer als JSON")
    args = ap.parse_args()

    doc = lade()
    entries = doc["eintraege"]
    by_slug = {e["slug"]: e for e in entries}

    treffer = []

    if args.kategorie:
        kat = norm(args.kategorie)
        treffer = [e for e in entries if norm(e["category"]) == kat]
        if not treffer:
            kats = sorted({e["category"] for e in entries})
            print(f"Keine Kategorie '{args.kategorie}'. Vorhanden:", file=sys.stderr)
            for k in kats:
                print("  " + k, file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(treffer, ensure_ascii=False, indent=2))
        else:
            print(f"Kategorie '{args.kategorie}' ({len(treffer)} Einträge):\n")
            for e in sorted(treffer, key=lambda x: x["name"].lower()):
                print(f"- {e['name']}  ({e['slug']})")
        return

    if args.suche:
        treffer = volltextsuche(entries, args.suche)
        if args.json:
            print(json.dumps(treffer, ensure_ascii=False, indent=2))
        else:
            print(f"Volltextsuche '{args.suche}' ({len(treffer)} Treffer):\n")
            for e in sorted(treffer, key=lambda x: x["name"].lower()):
                print(zeile_kompakt(e))
        return

    if not args.begriffe:
        ap.print_help()
        sys.exit(1)

    gesehen = set()
    ausgabe = []
    for begriff in args.begriffe:
        exakt, teil = finde(entries, begriff)
        gefunden = exakt if exakt else teil
        if not gefunden:
            ausgabe.append(("miss", begriff, None))
            continue
        # Bei genau einem exakten Treffer: Volltext sinnvoll. Sonst kompakt.
        voll = args.voll or (len(exakt) == 1 and not teil)
        for e in gefunden:
            if e["slug"] in gesehen:
                continue
            gesehen.add(e["slug"])
            ausgabe.append(("hit", e, voll))

    if args.json:
        hits = [x[1] for x in ausgabe if x[0] == "hit"]
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        misses = [x[1] for x in ausgabe if x[0] == "miss"]
        if misses:
            print("Nicht gefunden: " + ", ".join(misses), file=sys.stderr)
        return

    for art, e, voll in ausgabe:
        if art == "miss":
            print(f"[nicht gefunden] {e}\n")
            continue
        if voll:
            print(block_voll(e, by_slug))
            print()
        else:
            print(zeile_kompakt(e))


if __name__ == "__main__":
    main()
