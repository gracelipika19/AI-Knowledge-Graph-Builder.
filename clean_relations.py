import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")

INPUT_FILE = os.path.join(STORAGE_DIR, "extracted_relations.json")
OUTPUT_FILE = os.path.join(STORAGE_DIR, "clean_relations.json")

PRONOUNS = {"i", "we", "you", "he", "she", "it", "they", "them", "us"}

def is_valid_relation(r):
    s = r["subject"].lower()
    o = r["object"].lower()
    p = r["predicate"].lower()

    if s in PRONOUNS or o in PRONOUNS:
        return False
    if len(s) < 3 or len(o) < 3:
        return False
    if s == o:
        return False
    if len(p) < 3:
        return False
    return True

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        relations = json.load(f)

    clean = [r for r in relations if is_valid_relation(r)]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=4, ensure_ascii=False)

    print("✅ RELATION CLEANING COMPLETE")
    print(f"Original relations : {len(relations)}")
    print(f"Clean relations    : {len(clean)}")
    print(f"Saved to           : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
