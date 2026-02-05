import os
import json
import sqlite3
import pandas as pd
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------
# 1. CSV INGESTION
# ---------------------------
def ingest_csv_files():
    csv_dir = os.path.join(BASE_DIR, "csv_files")
    csv_data = {}

    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            path = os.path.join(csv_dir, file)
            try:
                df = pd.read_csv(path, low_memory=False)
                csv_data[file] = df
                print(f"[CSV] Loaded {file} | Rows: {len(df)}")
            except Exception as e:
                print(f"[CSV] Failed {file}: {e}")

    return csv_data


# ---------------------------
# 2. EMAIL INGESTION
# ---------------------------
def ingest_emails():
    email_path = os.path.join(BASE_DIR, "emails", "emails.csv")
    try:
        df = pd.read_csv(email_path, low_memory=False)
        print(f"[EMAILS] Loaded emails.csv | Rows: {len(df)}")
        return df
    except Exception as e:
        print(f"[EMAILS] Failed: {e}")
        return None


# ---------------------------
# 3. EXCEL INGESTION
# ---------------------------
def ingest_excel_files():
    excel_dir = os.path.join(BASE_DIR, "excel")
    excel_data = {}

    for file in os.listdir(excel_dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            path = os.path.join(excel_dir, file)
            try:
                sheets = pd.read_excel(path, sheet_name=None)
                excel_data[file] = sheets
                print(f"[EXCEL] Loaded {file} | Sheets: {len(sheets)}")
            except Exception as e:
                print(f"[EXCEL] Failed {file}: {e}")

    return excel_data


# ---------------------------
# 4. PDF INGESTION
# ---------------------------
def ingest_pdfs():
    pdf_dir = os.path.join(BASE_DIR, "pdfs-data")
    pdf_texts = {}

    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_dir, file)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                pdf_texts[file] = text
                print(f"[PDF] Loaded {file} | Characters: {len(text)}")
            except Exception as e:
                print(f"[PDF] Failed {file}: {e}")

    return pdf_texts


# ---------------------------
# 5. JSON INGESTION
# ---------------------------
# def ingest_json():
#     json_dir = os.path.join(BASE_DIR, "json_file")
#     json_data = {}

#     for file in os.listdir(json_dir):
#         if file.endswith(".json"):
#             path = os.path.join(json_dir, file)
#             try:
#                 records = []
#                 with open(path, "r", encoding="utf-8") as f:
#                     for line in f:
#                         records.append(json.loads(line.strip()))
#                 json_data[file] = records
#                 print(f"[JSON] Loaded {file} | Records: {len(records)}")
#             except Exception as e:
#                 print(f"[JSON] Failed {file}: {e}")

#     return json_data



# ---------------------------
# 6. STRUCTURED DB INGESTION
# ---------------------------
def ingest_database():
    db_path = os.path.join(BASE_DIR, "internal_db", "enterprise.db")
    db_data = {}

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            db_data[table_name] = df
            print(f"[DB] Loaded table {table_name} | Rows: {len(df)}")

        conn.close()
    except Exception as e:
        print(f"[DB] Failed: {e}")

    return db_data


# ---------------------------
# MAIN PIPELINE
# ---------------------------
def main():
    print("\n--- DATA INGESTION STARTED ---\n")

    csv_data = ingest_csv_files()
    email_data = ingest_emails()
    excel_data = ingest_excel_files()
    pdf_data = ingest_pdfs()
    # json_data = ingest_json()
    db_data = ingest_database()

    print("\n--- DATA INGESTION SUMMARY ---")
    print(f"CSV files ingested     : {len(csv_data)}")
    print(f"Excel files ingested   : {len(excel_data)}")
    print(f"PDFs ingested          : {len(pdf_data)}")
    # print(f"JSON files ingested    : {len(json_data)}")
    print(f"DB tables ingested     : {len(db_data)}")

    print("\n--- DATA INGESTION COMPLETED SUCCESSFULLY ---\n")


if __name__ == "__main__":
    main()
