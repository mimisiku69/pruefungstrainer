#!/usr/bin/env python3
"""Erzeugt daten/glossar.json aus dem Roh-Export daten/glossar_quelle.csv.

Aufruf (aus dem Skill-Ordner):
    python3 scripts/baue_glossar_json.py [--stand JJJJ-MM-TT] [--version X.Y]

Der Roh-Export kommt aus dem Lovable-Backend
(Cloud -> Database -> glossary_entries -> "Export CSV"), Semikolon-getrennt.
Die Array-Spalten synonyms und related liegen dort als JSON-Strings vor.
"""
import argparse
import csv
import json
import os

HIER = os.path.dirname(os.path.abspath(__file__))
DATEN = os.path.normpath(os.path.join(HIER, "..", "daten"))
CSV_DATEI = os.path.join(DATEN, "glossar_quelle.csv")
JSON_DATEI = os.path.join(DATEN, "glossar.json")


def as_array(value):
    value = (value or "").strip()
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else [str(parsed)]
    except json.JSONDecodeError:
        inner = value.strip("{}")
        return [p.strip().strip('"') for p in inner.split(",") if p.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stand", default="2026-07-27")
    ap.add_argument("--version", default="1.0")
    args = ap.parse_args()

    with open(CSV_DATEI, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))

    entries = []
    for r in rows:
        entries.append({
            "slug": r["slug"].strip(),
            "name": r["name"].strip(),
            "letter": (r["letter"] or "").strip() or "#",
            "category": r["category"].strip(),
            "teaser": (r["teaser"] or "").strip(),
            "body": (r["body"] or "").strip(),
            "example": (r["example"] or "").strip(),
            "synonyms": as_array(r["synonyms"]),
            "related": as_array(r["related"]),
            "source": (r["source"] or "").strip(),
        })
    entries.sort(key=lambda e: e["name"].lower())

    doc = {
        "_meta": {
            "titel": "KI-Glossar der KI Academy Leipzig",
            "stand": args.stand,
            "version": args.version,
            "herkunft": ("Lovable Cloud (verwaltetes Supabase), "
                         "Projekt atrluxtgcuydlwwqxugh, Tabelle glossary_entries"),
            "abgeleitet_am": args.stand,
            "abgeleitet_via": "CSV-Export aus dem Lovable-Backend (Database, Export CSV)",
            "anzahl": len(entries),
            "hinweis": ("Abgeleitete Offline-Fassung. Ursprung bleibt die Datenbank. "
                        "Bei Aenderungen dort neu exportieren und Version erhoehen."),
            "felder": {
                "name": "verbindliche Schreibweise (Schreibweisen-Register)",
                "synonyms": "Synonyme und englische Entsprechungen",
                "related": "verwandte Begriffe (slugs)",
            },
        },
        "eintraege": entries,
    }

    with open(JSON_DATEI, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)

    print(f"{len(entries)} Eintraege geschrieben nach {JSON_DATEI}")


if __name__ == "__main__":
    main()
