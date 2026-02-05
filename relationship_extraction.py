import os
import json
import spacy

# ---------------- CONFIG ----------------
MAX_DOCS = 10000     # same as entity extraction demo
MAX_CHARS = 1200
# ----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")

INPUT_FILE = os.path.join(STORAGE_DIR, "filtered_documents.json")
OUTPUT_FILE = os.path.join(STORAGE_DIR, "extracted_relations.json")

# Load full spaCy pipeline (parser required)
nlp = spacy.load("en_core_web_sm")

def extract_svo(doc):
    relations = []

    for token in doc:
        # verb
        if token.pos_ == "VERB":
            subj = None
            obj = None

            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subj = child.text
                elif child.dep_ in ("dobj", "pobj", "attr"):
                    obj = child.text

            if subj and obj:
                relations.append((subj, token.lemma_, obj))

    return relations

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    documents = documents[:MAX_DOCS]

    relations_output = []

    print(f"\n[INFO] Extracting relationships from {len(documents)} documents...\n")

    for doc in documents:
        text = doc.get("text", "")[:MAX_CHARS]
        doc_id = doc["doc_id"]

        spacy_doc = nlp(text)
        svos = extract_svo(spacy_doc)

        for s, v, o in svos:
            relations_output.append({
                "doc_id": doc_id,
                "subject": s,
                "predicate": v,
                "object": o
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(relations_output, f, indent=4, ensure_ascii=False)

    print("✅ RELATIONSHIP EXTRACTION COMPLETE")
    print(f"Documents processed : {len(documents)}")
    print(f"Relations extracted : {len(relations_output)}")
    print(f"Saved to            : {OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()
