import os
import json
import spacy
# ---------------- CONFIG ----------------
MAX_DOCS = 10000        # demo-friendly size
MAX_CHARS = 1200       # truncate long texts
BATCH_SIZE = 64
# ----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")

INPUT_FILE = os.path.join(STORAGE_DIR, "filtered_documents.json")
OUTPUT_FILE = os.path.join(STORAGE_DIR, "extracted_entities.json")

# Load spaCy model (NER only)
nlp = spacy.load(
    "en_core_web_sm",
    disable=["tagger", "parser", "lemmatizer"]
)

ENTITY_LABEL_MAP = {
    "PERSON": "Person",
    "ORG": "Organization",
    "GPE": "Location",
    "LOC": "Location",
    "PRODUCT": "Product",
    "EVENT": "Event",
    "DATE": "Date",
    "TIME": "Time",
    "MONEY": "Money",
    "NORP": "Group",
    "FAC": "Facility"
}

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    # 🎯 DEMO SUBSET
    documents = documents[:MAX_DOCS]

    texts, doc_ids = [], []

    for doc in documents:
        text = doc.get("text", "").strip()
        if text:
            texts.append(text[:MAX_CHARS])
            doc_ids.append(doc["doc_id"])

    extracted_entities = []

    print(f"\n[INFO] Processing {len(texts)} documents (demo mode)...\n")

    for spacy_doc, doc_id in zip(
        nlp.pipe(texts, batch_size=BATCH_SIZE),
        doc_ids
    ):
        for ent in spacy_doc.ents:
            if ent.label_ in ENTITY_LABEL_MAP:
                extracted_entities.append({
                    "doc_id": doc_id,
                    "entity_text": ent.text,
                    "entity_type": ENTITY_LABEL_MAP[ent.label_]
                })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted_entities, f, indent=4, ensure_ascii=False)

    print("✅ ENTITY EXTRACTION COMPLETE (DEMO MODE)")
    print(f"Documents processed : {len(texts)}")
    print(f"Entities extracted  : {len(extracted_entities)}")
    print(f"Saved to            : {OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()
