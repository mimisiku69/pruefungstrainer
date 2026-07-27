---
name: ki-glossar
description: >
  Zentrale Begriffsquelle der KI Academy Leipzig (Ingo Günther): verbindliche
  KI-Begriffe mit Definition, Schreibweise, Synonymen und englischen
  Entsprechungen sowie ein Hörfehler-Register für Zoom-/Teams-Transkripte. Single
  Source of Truth für Terminologie. Andere Skills und das Redaktionssystem
  schlagen hier nach, statt eigene Glossare zu führen. Nicht direkt durch
  Nutzereingabe triggern — wird als Unter-Skill geladen, wenn ein Begriff
  nachzuschlagen, eine Schreibweise zu vereinheitlichen oder ein Transkript auf
  Verhörer zu prüfen ist.
---

# ki-glossar — Begriffs- und Terminologiequelle KI Academy Leipzig

**Version 1.0 — 2026-07-27 · Schicht 0 (Fundament) · Lädt: —**

Zweck: Ein einziger, gepflegter Begriffsbestand für alle Skills und das
Redaktionssystem. Statt dass jeder Skill sein eigenes Glossar führt, wird hier
nachgeschlagen. Zusätzlich erkennt der Skill typische Verhörer aus Zoom- und
Teams-Mitschriften und nennt die richtige Zielform.

Changelog:
- 1.0 (2026-07-27): Erstanlage. Begriffsbestand aus dem KI-Glossar der KI
  Academy (Lovable Cloud, Tabelle `glossary_entries`, 536 Einträge) als
  abgeleitete Offline-Fassung übernommen. Hörfehler-Register als kuratierter
  Startbestand aufgebaut.

---

## 1. Was dieser Skill enthält

Drei Bestandteile, alle in `daten/`:

1. **Begriffsbestand** (`daten/glossar.json`). 536 Einträge mit `name`,
   `category`, `teaser`, `body`, `example`, `synonyms`, `related`. Abgeleitete
   Fassung mit Versionsstand und Herkunft. Der Ursprung bleibt die Datenbank
   (siehe `daten/QUELLE.md`).
2. **Schreibweisen-Register.** Kein eigenes File nötig: Das Feld `name` ist die
   **verbindliche Schreibweise**, `synonyms` führt Synonyme und englische
   Entsprechungen. Bei Uneinheitlichkeit gilt immer `name`.
3. **Hörfehler-Register** (`daten/hoerfehler.json`). Typische Verhörer aus
   automatischen Mitschriften mit der jeweils richtigen Zielform.

## 2. Kontextsparsamkeit — der Bestand wird nie ganz geladen

Der Glossarbestand darf **nie vollständig** in den Kontext geladen werden. Es
gibt drei Zugriffswege, alle über die Skripte in `scripts/`:

- **Einzelne Begriffe nachschlagen:**
  `python3 scripts/nachschlagen.py "BEGRIFF" [...]` gibt nur die angefragten
  Einträge aus. Ein exakter Einzeltreffer kommt im Volltext, mehrdeutige
  Kurzsuchen als kompakte Trefferliste. Optionen: `--voll`, `--kategorie "…"`,
  `--suche "…"` (Volltext in teaser/body), `--json`.
- **Transkript prüfen:**
  `python3 scripts/pruefe_transkript.py DATEI` läuft über das Hörfehler-Register
  und meldet nur die Funde mit Zeilennummer und Zielform. Mit `--begriffe`
  zusätzlich, welche Glossarbegriffe im Text vorkommen (nützlich für ein
  Glossar-Kapitel im Workbook).
- **Kapitel-Auszug:** Für ein Glossar-Kapitel nur die dort vorkommenden Begriffe
  über `nachschlagen.py` holen, nicht den ganzen Bestand.

Diese `SKILL.md` bleibt bewusst kurz. Alles Umfangreiche liegt in `daten/` und
wird nur über die Skripte punktuell angefasst.

## 3. Verbindliche Schreibweise

- Maßgeblich ist `name`. Beispiel: „Prompt Engineering", nicht
  „Prompt-Engineering" oder „prompt engineering", wenn `name` die erste Form
  führt.
- `synonyms` sind erlaubte Nebenformen und englische Entsprechungen, keine
  Zielform. In fertigen Texten auf `name` vereinheitlichen.
- Wenn ein Begriff fehlt: nicht raten. Nächstliegenden Eintrag über
  `--suche` prüfen und, falls wirklich neu, in der Datenbank ergänzen (siehe
  Abschnitt 5), nicht nur lokal.

## 4. Nutzung durch andere Skills (Single Source of Truth)

Andere Skills definieren KI-Begriffe **nicht selbst**, sondern verweisen hierher
und schlagen bei Bedarf nach. Konvention für den Pfad im Skill-System:
`/mnt/skills/user/ki-glossar/` (in dieser Sitzung
`/root/.claude/skills/ki-glossar/`).

Vorgesehen für den Verweis statt eigener Definitionen: `seminar-handout`,
`ki-academy-workbook`, `workshop-konzeption`, `vortrag-erstellen`,
`linkedin-beitrag`, `anleitung-verbessern` sowie das Redaktions-Playbook. Diese
Anpassungen sind Folgearbeiten (Versionssprung im jeweiligen Skill, Eintrag in
`skill-erstellen/SKILL-INDEX.md`).

## 5. Herkunft und Aktualisierung

Vollständige Herkunft, Versionsstand und der Aktualisierungsweg stehen in
`daten/QUELLE.md`. Kurz:

- Ursprung: Lovable Cloud (verwaltetes Supabase), Projekt `atrluxtgcuydlwwqxugh`,
  Tabelle `glossary_entries`. Öffentliche App:
  https://ki-manager-methoden.lovable.app/glossar
- Aktualisieren: in Lovable erneut „Export CSV", `daten/glossar_quelle.csv`
  ersetzen, dann `python3 scripts/baue_glossar_json.py --stand JJJJ-MM-TT
  --version X.Y`. In `_meta` Stand und Version erhöhen, `QUELLE.md`
  fortschreiben.

## 6. Verhalten bei Unklarheiten

Rückfragen, eine Frage nach der anderen. Keine Begriffe erfinden, keine
Definition aus dem Gedächtnis schreiben, wenn der Bestand sie nicht hat. Echte
deutsche Umlaute und ß, kein m-dash (Regeln: `stil-und-ton`).

## 7. Verknüpfung mit anderen Skills

Sprache und Ton: `stil-und-ton`. Recht und BFSG: `recht-und-pflicht`. Dieser
Skill selbst erzeugt keine Dokumente, daher gilt die docx-Pflicht-Reihenfolge
hier nicht.
