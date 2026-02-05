import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")

INPUT_FILE = os.path.join(STORAGE_DIR, "normalized_documents.json")
OUTPUT_FILE = os.path.join(STORAGE_DIR, "filtered_documents.json")

# Allowed non-CSV sources
ALLOWED_SOURCES = {"pdf", "email", "excel"}

# ONLY these CSV files should be kept
ALLOWED_CSV_FILES = {
    "query.csv",
    "sparql_2025-12-13_07-55-26Z.csv",
    "UDISE_2021_22_Table_5.9_0.csv"
}

# -------------------------------
# TEXT QUALITY CHECK
# -------------------------------
def is_valid_text(text: str) -> bool:
    if not text or len(text) < 80:
        return False

    text = text.lower()

    header_keywords = [
        "message-id", "mime-version", "content-type",
        "content-transfer-encoding", "from:", "to:", "subject:", "date:"
    ]
    if sum(1 for k in header_keywords if k in text) >= 2:
        return False

    words = re.findall(r"\b[a-z]{3,}\b", text)
    if len(words) < 8:
        return False

    if "." not in text and "," not in text:
        return False

    return True

# -------------------------------
# FILTER PIPELINE (PATH A FINAL)
# -------------------------------
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    filtered_docs = []

    for doc in documents:
        source_type = doc.get("source_type")
        source_name = doc.get("source_name", "")
        text = doc.get("text", "")

        # PDFs, Emails, Excel
        if source_type in ALLOWED_SOURCES and is_valid_text(text):
            filtered_docs.append(doc)

        # ONLY selected CSVs
        elif (
            source_type == "csv"
            and source_name in ALLOWED_CSV_FILES
            and is_valid_text(text)
        ):
            filtered_docs.append(doc)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered_docs, f, indent=4, ensure_ascii=False)

    print("\n--- PATH A FILTERING (CSV FIXED) ---")
    print(f"Original documents : {len(documents)}")
    print(f"Final clean docs   : {len(filtered_docs)}")
    print(f"Saved to           : {OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()
