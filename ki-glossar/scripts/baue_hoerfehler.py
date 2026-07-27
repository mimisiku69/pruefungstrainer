#!/usr/bin/env python3
"""Erzeugt daten/hoerfehler.json aus einer kuratierten Liste.

Jede Zielform wird gegen daten/glossar.json geprüft und der slug automatisch
verlinkt (Treffer auf name oder Synonym). So gibt es keine toten Verweise. Nicht
im Glossar gefundene Zielformen werden gemeldet und ohne slug übernommen.

Aufruf (aus dem Skill-Ordner):
    python3 scripts/baue_hoerfehler.py
"""
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
DATEN = os.path.normpath(os.path.join(HIER, "..", "daten"))
GLOSSAR = os.path.join(DATEN, "glossar.json")
ZIEL = os.path.join(DATEN, "hoerfehler.json")

# (richtige Zielform, [typische Falschformen aus Zoom/Teams-Mitschriften], Hinweis)
KURATIERT = [
    ("Machine Learning", ["Meschin Lörning", "Määschin Lörning", "Machine Lörning", "Mäschin Learning", "Maschin Lörning"], "engl. Fachbegriff, oft phonetisch verschriftet"),
    ("Deep Learning", ["Diep Lörning", "Diep Learning", "Deep Lörning", "Diep Löning"], ""),
    ("Reinforcement Learning", ["Rienforcement Lörning", "Reinforsment Learning", "Rihnforsment Lörning"], ""),
    ("Supervised Learning", ["Supervaisd Lörning", "Sjupervaisd Learning"], ""),
    ("Unsupervised Learning", ["Ansupervaisd Lörning", "Unsupervaisd Learning"], ""),
    ("Prompt", ["Promt", "Prompd", "Promd", "Brompt", "Prombt"], "häufigster Tippfehler: t statt pt"),
    ("Prompt Engineering", ["Promt Engineering", "Prompt Ingenieuring", "Promt Endschiniering"], ""),
    ("System-Prompt", ["System Promt", "Systemprompt", "System-Promt"], ""),
    ("Token", ["Tocken", "Tokken", "Toten"], ""),
    ("Embedding", ["Ambedding", "Imbedding", "Embeding", "Em Bedding", "Ähmbedding"], ""),
    ("Fine-Tuning", ["Feintuning", "Fein Tuning", "Fine Tuning", "Feintjuning"], "im Deutschen mit Bindestrich"),
    ("Transformer", ["Transformör", "Träänsformer", "Transformäer"], "Architektur, nicht das Spielzeug"),
    ("Large Language Model", ["Larsch Language Model", "Lartsch Längwidsch Model", "Large Längwitsch Modell"], ""),
    ("LLM", ["El El Em", "Ell Ell Emm"], "Abkürzung, wird oft ausbuchstabiert transkribiert"),
    ("Hugging Face", ["Hacking Face", "Haging Face", "Hugging Fäis", "Hägging Face"], "Plattform, nicht Hacking"),
    ("ChatGPT", ["Chat GPT", "Chat GPD", "Tschät Gpt", "Schät Dschi Pi Ti", "Chat Gpt"], ""),
    ("GPT", ["GPD", "JPT", "Sche Pe Te", "Gpt"], ""),
    ("Bias", ["Beis", "Bajas", "Baias", "Bei As"], "Verzerrung, engl. ausgesprochen"),
    ("Halluzination", ["Haluzination", "Haluzinationen", "Halutination", "Halluzinazion"], ""),
    ("Inferenz", ["Infrängs", "Inferens", "In Ferenz"], ""),
    ("Overfitting", ["Oberfitting", "Over Fitting", "Owerfitting"], ""),
    ("Underfitting", ["Anderfitting", "Under Fitting"], ""),
    ("Framework", ["Freimwörk", "Frame Work", "Fräimwörk", "Freim Work"], ""),
    ("Open Source", ["Open Sors", "Oppen Source", "Open Sauce", "Open Sohs"], ""),
    ("Cloud", ["Klaud", "Claud"], ""),
    ("Dataset", ["Data Set", "Deiter Set", "Deita Set"], "Datensatz"),
    ("Data Science", ["Data Seiens", "Deita Science", "Data Sains"], ""),
    ("API", ["Ei Pi Ei", "A P I", "APi"], "Schnittstelle"),
    ("Chatbot", ["Tschätbott", "Chat Bot", "Schätbot", "Tschät Bot"], ""),
    ("Agent", ["Ähdschent", "Ädschent", "Ehdschent"], "im KI-Kontext: KI-Agent"),
    ("Agentisch", ["Agentik", "Ädschentik", "Agentisch e"], ""),
    ("Stable Diffusion", ["Steibl Diffusion", "Stable Diffjuschn", "Steibel Diffusion"], ""),
    ("Midjourney", ["Mid Journey", "Mitschörni", "Mid Dschörni", "Midschörni"], "Bildgenerator"),
    ("DALL-E", ["Dali", "Doll E", "Dall I", "Dall E"], "OpenAI-Bildmodell, nicht der Maler"),
    ("Copilot", ["Co Pilot", "Kopilot", "Ko Pilot"], ""),
    ("RAG", ["Räg", "Rack", "Reg", "R A G"], "Retrieval Augmented Generation"),
    ("Retrieval Augmented Generation", ["Retrieval Augmented Generäischn", "Ritrievel Augmented Generation"], ""),
    ("Vektordatenbank", ["Wektordatenbank", "Vektor Datenbank", "Wektor Datenbank"], ""),
    ("Chain of Thought", ["Tschein of Thought", "Chain of Sort", "Tschäin of Thot"], "Gedankenkette"),
    ("Zero-Shot", ["Siro Schott", "Zero Schott", "Siro Shot"], ""),
    ("Few-Shot", ["Fju Schott", "Few Schott", "Fjuh Shot"], ""),
    ("Foundation Model", ["Faundäischn Model", "Foundäischn Modell", "Faundation Model"], ""),
    ("Multimodal", ["Multi Modal", "Multimodahl"], ""),
    ("Guardrails", ["Gard Rails", "Guard Reils", "Gardreils"], "Leitplanken"),
    ("Governance", ["Governanz", "Gawernans", "Gowernans"], ""),
    ("Compliance", ["Complaiens", "Kompliance", "Komplaiens"], ""),
    ("EU AI Act", ["EU AI Ekt", "EU KI Act", "EU AI Äkt", "EU A I Act"], "EU-Verordnung"),
    ("Deepfake", ["Diepfake", "Deep Fake", "Diep Feik", "Dief Fake"], ""),
    ("Ground Truth", ["Graund Truth", "Ground Trust", "Graund Trues"], ""),
    ("Annotation", ["Annotäischn", "Anotation", "Annotäation"], ""),
    ("Labeling", ["Läibeling", "Leibeling", "Label ing"], "Datenkennzeichnung"),
    ("Pipeline", ["Peiplain", "Pipe Line", "Peip Lain"], ""),
    ("Deployment", ["Deploiment", "Diploiment", "Deploimänt"], ""),
    ("Scraping", ["Skreiping", "Scrapen", "Skräiping"], ""),
    ("Benchmark", ["Bentschmark", "Bench Mark", "Bentsch Mark"], ""),
    ("Quantisierung", ["Quantaiseischn", "Kwantisierung", "Quantifizierung"], "Modellkompression, nicht Quantifizierung"),
    ("Kontextfenster", ["Kontext Windou", "Context Window", "Kontext Fenster"], ""),
    ("Jailbreak", ["Dschailbreak", "Jail Break", "Scheilbreik", "Dscheilbreak"], ""),
    ("Alignment", ["Alainment", "Alignmänt", "Alain Ment"], "Ausrichtung"),
    ("Reasoning", ["Riesning", "Räsoning", "Riehsoning"], ""),
    ("Diffusionsmodell", ["Diffjuschn Modell", "Diffusion Model", "Diffjuschn Model"], ""),
    ("Neuronales Netz", ["Neurales Netz", "Njuronales Netz", "Neuronale Netz"], ""),
    ("Künstliche Intelligenz", ["Künstige Intelligenz", "Künstlicher Intelligenz e", "Kunstliche Intelligenz"], ""),
]


# Zielformen, die im Glossar unter längerem Namen stehen (verifiziert 2026-07-27).
OVERRIDES = {
    "Large Language Model": "large-language-model-grosses-sprachmodell",
    "Chain of Thought": "chain-of-thought-gedankenkette",
    "Few-Shot": "few-shot-learning",
    "Multimodal": "multimodale-modelle",
    "Agent": "agenten",
    "Agentisch": "agentisches-verhalten",
    "Reasoning": "reasoning-modell",
    "Neuronales Netz": "neuronales-netzwerk",
    "Künstliche Intelligenz": "kuenstliche-intelligenz-ki",
    "Pipeline": "datenpipeline",
}


def norm(s):
    return (s or "").strip().lower()


def main():
    with open(GLOSSAR, encoding="utf-8") as fh:
        glossar = json.load(fh)
    # Index: name/synonym (normalisiert) -> slug
    index = {}
    gueltige_slugs = set()
    for e in glossar["eintraege"]:
        gueltige_slugs.add(e["slug"])
        for key in [e["name"]] + e.get("synonyms", []):
            index.setdefault(norm(key), e["slug"])

    # Overrides gegen echte slugs prüfen
    for richtig, slug in OVERRIDES.items():
        if slug not in gueltige_slugs:
            print(f"WARNUNG: Override-slug '{slug}' für '{richtig}' existiert nicht.",
                  file=sys.stderr)

    eintraege = []
    ohne_slug = []
    for richtig, falsch, hinweis in KURATIERT:
        slug = OVERRIDES.get(richtig) or index.get(norm(richtig), "")
        if not slug:
            ohne_slug.append(richtig)
        eintraege.append({
            "richtig": richtig,
            "slug": slug,
            "falsch": falsch,
            "hinweis": hinweis,
        })

    doc = {
        "_meta": {
            "titel": "Hörfehler-Register KI Academy Leipzig",
            "stand": "2026-07-27",
            "version": "1.0",
            "zweck": ("Typische Verhörer englischer KI-Begriffe aus automatischen "
                      "Zoom-/Teams-Mitschriften mit der richtigen Zielform."),
            "anzahl": len(eintraege),
            "hinweis": ("Kuratierter Startbestand. Aus echten Transkripten laufend "
                        "ergänzen. slug verweist auf den Glossareintrag der Zielform."),
        },
        "eintraege": eintraege,
    }
    with open(ZIEL, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)

    print(f"{len(eintraege)} Hörfehler-Einträge geschrieben, "
          f"{len(eintraege) - len(ohne_slug)} mit Glossar-Verweis.")
    if ohne_slug:
        print("Zielform nicht (exakt) im Glossar:", file=sys.stderr)
        for r in ohne_slug:
            print("  " + r, file=sys.stderr)


if __name__ == "__main__":
    main()
