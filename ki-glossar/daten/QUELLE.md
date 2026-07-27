# Herkunft und Versionsstand des Glossarbestands

**Stand: 2026-07-27 · Version 1.0**

## Woher die Daten stammen

Der Begriffsbestand stammt aus dem KI-Glossar der KI Academy Leipzig, das im
Projekt `ki-manager-methoden` (Lovable Cloud) liegt.

- Backend: Lovable Cloud (verwaltetes Supabase)
- Supabase-Projekt: `atrluxtgcuydlwwqxugh`
- Tabelle: `glossary_entries`
- Öffentliche App: https://ki-manager-methoden.lovable.app/glossar
- Abgeleitet am: 2026-07-27, per CSV-Export aus dem Lovable-Backend
  (Cloud → Database → Tabelle `glossary_entries` → „Export CSV")

## Warum eine abgeleitete Offline-Fassung

Skills laufen offline. Ein Live-Abruf aus dem Lovable-/Supabase-Backend ist im
Lauf nicht verlässlich (Netz-Policy, verwaltetes Backend ohne eigenen
MCP-Zugang). Deshalb trägt der Skill eine abgeleitete Fassung mit Versionsstand
und Herkunftsangabe. **Der Ursprung bleibt die Datenbank.**

## Dateien

- `glossar_quelle.csv` — Roh-Export aus Lovable (Semikolon-getrennt), unverändert.
- `glossar.json` — bereinigte Fassung: `synonyms` und `related` als echte Arrays,
  nach Name sortiert, Metadaten im Feld `_meta`.

## Bestand (Stand 2026-07-27)

- Einträge gesamt: **536**
- Kategorien: Technik & Daten (115), Recht & Regulatorik (85),
  Tools & Anwendungen (83), Management & Strategie (74), KI-Grundlagen (68),
  Methoden & Frameworks (66), Change & Organisation (45)

> Die öffentliche Website blendet die Kategorie „Methoden & Frameworks" aus
> (`EXCLUDED_CATEGORY` im App-Code). Diese Offline-Fassung enthält bewusst
> **alle** Kategorien.

## Aktualisieren

1. In Lovable erneut „Export CSV" der Tabelle `glossary_entries`.
2. CSV als `glossar_quelle.csv` ersetzen.
3. `python3 scripts/baue_glossar_json.py` (falls vorhanden) oder den
   Umwandlungsschritt erneut ausführen, um `glossar.json` neu zu erzeugen.
4. In `glossar.json` unter `_meta` `stand` und `version` erhöhen und diese
   Datei fortschreiben.
