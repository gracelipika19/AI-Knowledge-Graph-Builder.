import os
import json
import sqlite3
import pandas as pd
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directory for persistent JSON storage
STORAGE_DIR = os.path.join(BASE_DIR, "ingested_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

# ---------------------------
# STORAGE HELPER FUNCTION
# ---------------------------
def save_to_json(data, filename):
    """
    Saves various data types into a JSON file, ensuring all 
    DataFrames are converted to serializable formats.
    """
    path = os.path.join(STORAGE_DIR, filename)
    
    def handle_serialization(obj):
        # Convert DataFrames to list of dictionaries
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        
        # Recurse through dictionaries (Excel sheets/DB tables)
        if isinstance(obj, dict):
            return {k: handle_serialization(v) for k, v in obj.items()}
        
        # Recurse through lists
        if isinstance(obj, list):
            return [handle_serialization(i) for i in obj]
        
        return obj

    try:
        serializable_data = handle_serialization(data)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)
        print(f"[STORAGE] Successfully saved: {filename}")
    except Exception as e:
        print(f"[STORAGE] Error saving {filename}: {e}")

# ---------------------------
# 1. CSV INGESTION (with Cleaning)
# ---------------------------
def ingest_csv_files():
    csv_dir = os.path.join(BASE_DIR, "csv_files")
    csv_data = {}
    if not os.path.exists(csv_dir): return {}
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            path = os.path.join(csv_dir, file)
            try:
                df = pd.read_csv(path, low_memory=False)
                # CLEANING: Handle missing values
                csv_data[file] = df.fillna("Not Applicable")
                print(f"[CSV] Loaded and cleaned {file}")
            except Exception as e:
                print(f"[CSV] Failed {file}: {e}")
    return csv_data

# ---------------------------
# 2. EMAIL INGESTION (with Cleaning)
# ---------------------------
def ingest_emails():
    email_path = os.path.join(BASE_DIR, "emails", "emails.csv")
    try:
        df = pd.read_csv(email_path, low_memory=False)
        print(f"[EMAILS] Loaded and cleaned emails.csv")
        return df.fillna("Not Applicable")
    except Exception as e:
        print(f"[EMAILS] Failed: {e}")
        return None

# ---------------------------
# 3. EXCEL INGESTION (with Cleaning)
# ---------------------------
def ingest_excel_files():
    excel_dir = os.path.join(BASE_DIR, "excel")
    excel_data = {}
    if not os.path.exists(excel_dir): return {}
    for file in os.listdir(excel_dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            path = os.path.join(excel_dir, file)
            try:
                sheets = pd.read_excel(path, sheet_name=None)
                cleaned_sheets = {}
                for sheet_name, df in sheets.items():
                    cleaned_sheets[sheet_name] = df.fillna("Not Applicable")
                excel_data[file] = cleaned_sheets
                print(f"[EXCEL] Loaded and cleaned {file}")
            except Exception as e:
                print(f"[EXCEL] Failed {file}: {e}")
    return excel_data

# ---------------------------
# 4. PDF INGESTION
# ---------------------------
def ingest_pdfs():
    pdf_dir = os.path.join(BASE_DIR, "pdfs-data")
    pdf_texts = {}
    if not os.path.exists(pdf_dir): return {}
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_dir, file)
            try:
                reader = PdfReader(path)
                text = "".join([page.extract_text() or "" for page in reader.pages])
                pdf_texts[file] = text
                print(f"[PDF] Loaded {file}")
            except Exception as e:
                print(f"[PDF] Failed {file}: {e}")
    return pdf_texts

# ---------------------------
# 5. STRUCTURED DB INGESTION (with Cleaning)
# ---------------------------
def ingest_database():
    db_path = os.path.join(BASE_DIR, "internal_db", "enterprise.db")
    db_data = {}
    if not os.path.exists(db_path): return {}
    try:
        conn = sqlite3.connect(db_path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        for table in tables:
            t_name = table[0]
            df = pd.read_sql_query(f"SELECT * FROM {t_name}", conn)
            db_data[t_name] = df.fillna("Not Applicable")
            print(f"[DB] Loaded and cleaned table {t_name}")
        conn.close()
    except Exception as e:
        print(f"[DB] Failed: {e}")
    return db_data

# ---------------------------
# MAIN PIPELINE
# ---------------------------
def main():
    print("\n--- DATA INGESTION & JSON STORAGE STARTED ---\n")

    # Ingest and Store all sources
    save_to_json(ingest_csv_files(), "ingested_csvs.json")
    
    email_raw = ingest_emails()
    if email_raw is not None:
        save_to_json(email_raw, "ingested_emails.json")

    save_to_json(ingest_excel_files(), "ingested_excel.json")
    save_to_json(ingest_pdfs(), "ingested_pdfs.json")
    save_to_json(ingest_database(), "ingested_database.json")

    print(f"\n--- SUCCESS: Data cleaned and saved in {STORAGE_DIR} ---\n")

if __name__ == "__main__":
    main()