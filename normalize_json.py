import os
import json
import re
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")

OUTPUT_FILE = os.path.join(STORAGE_DIR, "normalized_documents.json")

# ---------------------------
# TEXT NORMALIZATION
# ---------------------------
def normalize_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)        # collapse spaces
    text = re.sub(r"[^\w\s.,]", "", text)   # remove noise chars
    return text.strip()

# ---------------------------
# FLATTEN RECORD INTO TEXT
# ---------------------------
def record_to_text(record):
    values = []
    for v in record.values():
        if isinstance(v, (str, int, float)):
            values.append(str(v))
    return normalize_text(" ".join(values))

# ---------------------------
# LOAD JSON SAFELY
# ---------------------------
def load_json(filename):
    path = os.path.join(STORAGE_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------
# NORMALIZATION PIPELINE
# ---------------------------
def normalize_all_sources():
    normalized_docs = []
    doc_counter = 1

    # 1. CSV FILES
    csv_data = load_json("ingested_csvs.json") or {}
    for file_name, records in csv_data.items():
        for idx, record in enumerate(records):
            normalized_docs.append({
                "doc_id": f"DOC_{doc_counter:06d}",
                "source_type": "csv",
                "source_name": file_name,
                "text": record_to_text(record),
                "metadata": {"row_index": idx}
            })
            doc_counter += 1

    # 2. EMAILS
    emails = load_json("ingested_emails.json") or []
    for idx, record in enumerate(emails):
        normalized_docs.append({
            "doc_id": f"DOC_{doc_counter:06d}",
            "source_type": "email",
            "source_name": "emails.csv",
            "text": record_to_text(record),
            "metadata": {"row_index": idx}
        })
        doc_counter += 1

    # 3. EXCEL FILES
    excel_data = load_json("ingested_excel.json") or {}
    for file_name, sheets in excel_data.items():
        for sheet_name, records in sheets.items():
            for idx, record in enumerate(records):
                normalized_docs.append({
                    "doc_id": f"DOC_{doc_counter:06d}",
                    "source_type": "excel",
                    "source_name": file_name,
                    "text": record_to_text(record),
                    "metadata": {
                        "sheet": sheet_name,
                        "row_index": idx
                    }
                })
                doc_counter += 1

    # 4. PDFs
    pdfs = load_json("ingested_pdfs.json") or {}
    for file_name, text in pdfs.items():
        normalized_docs.append({
            "doc_id": f"DOC_{doc_counter:06d}",
            "source_type": "pdf",
            "source_name": file_name,
            "text": normalize_text(text),
            "metadata": {}
        })
        doc_counter += 1

    # 5. DATABASE TABLES
    db_data = load_json("ingested_database.json") or {}
    for table_name, records in db_data.items():
        for idx, record in enumerate(records):
            normalized_docs.append({
                "doc_id": f"DOC_{doc_counter:06d}",
                "source_type": "database",
                "source_name": table_name,
                "text": record_to_text(record),
                "metadata": {"row_index": idx}
            })
            doc_counter += 1

    return normalized_docs

# ---------------------------
# SAVE OUTPUT
# ---------------------------
def main():
    print("\n--- NORMALIZATION STARTED ---\n")
    normalized_docs = normalize_all_sources()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_docs, f, indent=4, ensure_ascii=False)

    print(f"[NORMALIZATION] Completed. Documents created: {len(normalized_docs)}")
    print(f"[NORMALIZATION] Saved to: {OUTPUT_FILE}\n")

if __name__ == "__main__":
    main()
