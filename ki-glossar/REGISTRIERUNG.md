# Registrierung und Folgearbeiten für `ki-glossar`

Dieser Skill ist ein **neuer Fundament-Skill (Schicht 0)**. Freigabe durch Ingo
erteilt am 2026-07-27. Damit er dauerhaft im Skill-System ankommt, sind die
folgenden Schritte laut `skill-erstellen` (Abschnitt 8) offen.

## 1. SKILL-INDEX.md ergänzen

In `skill-erstellen/SKILL-INDEX.md` unter „Schicht 0 — Fundament" diese Zeile
aufnehmen:

```
| ki-glossar | 1.0 | 2026-07-27 | — | aktiv |
```

Danach `skill-erstellen` neu als ZIP packen und hochladen.

## 2. Skill ins System laden

Den Ordner `ki-glossar/` als `ki-glossar.zip` packen und in die
Skill-Bibliothek hochladen (Laufzeitpfad dann
`/mnt/skills/user/ki-glossar/`). Ein fertiges ZIP wird separat bereitgestellt
(Chat-Download); es lässt sich jederzeit aus diesem Ordner neu packen mit
`zip -qr ki-glossar.zip ki-glossar`.

## 3. Verweis statt eigener Definitionen (spätere Versionssprünge)

Diese Skills sollen KI-Begriffe künftig aus `ki-glossar` beziehen statt eigener
Glossare. Je Skill ein Versionssprung und Eintrag im SKILL-INDEX:

- `seminar-handout`
- `ki-academy-workbook`
- `workshop-konzeption`
- `vortrag-erstellen`
- `linkedin-beitrag`
- `anleitung-verbessern`
- Redaktions-Playbook (Redaktionssystem)

Der Verweis lautet jeweils: Begriffe über
`python3 /mnt/skills/user/ki-glossar/scripts/nachschlagen.py "BEGRIFF"` holen,
verbindliche Schreibweise ist das Feld `name`.

## 4. Datenpflege

Bei Änderungen am Glossar in Lovable erneut exportieren und
`glossar.json` neu bauen (siehe `daten/QUELLE.md`). Das Hörfehler-Register
laufend aus echten Transkripten ergänzen (`scripts/baue_hoerfehler.py`).
