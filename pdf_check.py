import json, os

path = r"D:\Desktop\ML\info_pro\ingested_storage\filtered_documents.json"
docs = json.load(open(path, "r", encoding="utf-8"))

pdfs = [d for d in docs if d["source_type"]=="pdf"]

print("PDFs count:", len(pdfs))
print(pdfs[:3])
