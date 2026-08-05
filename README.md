# Prüfungstrainer

Ein Lerntrainer zur Prüfungsvorbereitung: Aussagen-Training (richtig/falsch), Multiple-Choice, Themen-Simulation und Prüfungssimulation mit Zeitlimit. Der Lernstand wird pro Fragenset im Browser gespeichert.

Die App ist eine einzelne HTML-Datei ohne Build-Schritt und ohne Server. Die Fragen selbst liegen daneben als JSON-Dateien im Repo.

## Aufrufen

Der Trainer muss über HTTP laufen, nicht per Doppelklick. Er lädt die Fragensets zur Laufzeit nach, und Browser blockieren solche Zugriffe bei `file://`.

Lokal:

```
npx http-server -p 8791
```

Dann `http://127.0.0.1:8791/index.html` im Browser öffnen.

Wird `index.html` doch per `file://` geöffnet, startet die App mit einem eingebauten Ersatz-Fragenset, damit sie nicht leer bleibt. Die Auswahlliste zeigt dann nur dieses eine Set.

## Fragenset hinzufügen

Drei Schritte, kein Eingriff in `index.html`:

1. Fragenset als JSON-Datei ins Repo legen, z. B. `fragenset-mein-thema.json`.
2. In `fragensets.json` einen Eintrag anhängen:

```json
{
  "id": "mein-thema-2026",
  "file": "fragenset-mein-thema.json",
  "label": "Mein Thema · Übungsset"
}
```

3. Committen und pushen. Das neue Set steht danach allen Nutzenden in der Auswahlliste zur Verfügung.

Wichtig: Das Feld `id` im Manifest muss mit dem Feld `id` **in** der JSON-Datei übereinstimmen. Das `label` aus dem Manifest ist der Text, der in der Auswahlliste, in der Kopfzeile und im Browser-Tab erscheint — eine Umbenennung ist also eine Zeile hier, nicht im Code.

### Aufbau einer Fragenset-Datei

```json
{
  "id": "mein-thema-2026",
  "title": "Mein Thema",
  "subtitle": "Übungsset",
  "config": {
    "examQuestions": 35,
    "examMinutes": 60,
    "passPercent": 60,
    "topicSimQuestions": 20
  },
  "topics": [
    { "id": "grundlagen", "name": "Grundlagen" }
  ],
  "statements": [
    {
      "id": "grundlagen-s1",
      "topic": "grundlagen",
      "context": "Optionaler Fallkontext, ein bis zwei Sätze.",
      "question": "Die zu bewertende Aussage.",
      "answer": true,
      "explanation": "Begründung, die nach der Antwort erscheint."
    }
  ],
  "mcQuestions": [
    {
      "id": "grundlagen-m1",
      "topic": "grundlagen",
      "question": "Die Fragestellung. Hinweis: eine oder mehrere Antworten richtig.",
      "options": [
        { "text": "Antwortoption", "correct": true,  "explanation": "Warum richtig." },
        { "text": "Antwortoption", "correct": false, "explanation": "Warum falsch." }
      ]
    }
  ]
}
```

Regeln, die die App beim Laden prüft und bei Verstoß mit einer Meldung quittiert:

- `id`, `title` und eine nicht leere Liste `topics` sind Pflicht.
- Mindestens eine der Listen `statements` oder `mcQuestions` muss Einträge haben; die jeweils andere darf fehlen.
- Jede MC-Frage braucht mindestens zwei Optionen und mindestens eine als `correct` markierte.
- `config` ist optional. Fehlende Werte werden mit den oben gezeigten Vorgaben aufgefüllt.

Darüber hinaus sollte jedes `topic` einer Frage einer `id` aus `topics` entsprechen und jede Frage-`id` innerhalb des Sets eindeutig sein. Beides prüft die App nicht, beides führt sonst aber zu fehlenden Fragen in der Themenauswahl bzw. zu vermischten Lernständen.

## Fragenset ausprobieren, bevor es ins Repo geht

Über „Fragenset importieren" lässt sich eine JSON-Datei direkt im Browser laden. Sie liegt dann nur in diesem einen Browser und ist für andere nicht sichtbar — praktisch zum Gegenlesen, kein Ersatz für den Commit.

„JSON exportieren" gibt das gerade aktive Set als Datei aus. Damit lässt sich ein importiertes Set anschließend ins Repo übernehmen.

## Lernstand

Der Lernstand liegt im `localStorage` des jeweiligen Browsers, getrennt nach Fragenset (`pt_prog_<set-id>`). Er wandert nicht zwischen Geräten und geht verloren, wenn die Browserdaten gelöscht werden. „Lernstand zurücksetzen" löscht nur den Stand des aktiven Sets.

## Dateien

| Datei | Zweck |
| --- | --- |
| `index.html` | Die komplette App: Oberfläche, Logik, Styles |
| `fragensets.json` | Manifest der im Repo verfügbaren Fragensets |
| `fragenset-*.json` | Die Fragensets selbst |
| `fonts/` | Schrift Arimo, lokal ausgeliefert |
| `site.webmanifest`, `icon-*.png`, `apple-touch-icon.png` | Installierbarkeit auf dem Homescreen |

## Schrift

Arimo liegt unter `fonts/` im Repo und wird von dort ausgeliefert, nicht von Google. Damit gehen beim Aufruf der Seite keine Besucherdaten an einen Drittanbieter — das Einbinden über `fonts.googleapis.com` ist in Deutschland abmahnfähig (LG München I, Urteil vom 20.01.2022, 3 O 17493/20).

Arimo ist eine Variable Font: eine Datei deckt die Gewichte 400 bis 700 ab. Über `unicode-range` lädt der Browser nur, was der Text braucht — für deutsche Inhalte sind das 20 KB (`arimo-latin.woff2`); `arimo-latin-ext.woff2` kommt nur bei Sonderzeichen anderer lateinischer Sprachen dazu.

Lizenz: SIL Open Font License 1.1, siehe `fonts/OFL.txt`.
