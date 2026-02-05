import json
import os
from common import normalize, split_sentences

DATA_DIR = "D:/Desktop/ML/info_pro/ingested_storage"
OUT_DIR = "D:/Desktop/ML/info_pro/output"

INPUT = {
    "emails": "filtered_documents.json",
    "relations": "clean_relations.json",
    "entities": "extracted_entities.json"
}

os.makedirs(OUT_DIR, exist_ok=True)

def chunk_relations():
    infile = os.path.join(DATA_DIR, INPUT["relations"])
    outfile = os.path.join(OUT_DIR, "relations_sentences.jsonl")

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "w", encoding="utf-8") as out:
        for r in json.load(f):
            txt = f"{r['subject']} {r['predicate']} {r['object']}"
            out.write(json.dumps({
                "id": f"rel::{r['doc_id']}",
                "text": normalize(txt),
                "subject": r['subject'],
                "predicate": r['predicate'],
                "object": r['object']
            }) + "\n")


def chunk_emails():
    infile = os.path.join(DATA_DIR, "filtered_documents.json")
    outfile = os.path.join(OUT_DIR, "email_chunks.jsonl")

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "w", encoding="utf-8") as out:
        for doc in json.load(f):
            if doc["source_type"] != "email": 
                continue
            text = normalize(doc["text"])
            sents = split_sentences(text)
            for i, s in enumerate(sents):
                if len(s) > 20:
                    out.write(json.dumps({
                        "id": f"email::{doc['doc_id']}::{i}",
                        "text": s
                    }) + "\n")


def chunk_csv():
    infile = os.path.join(DATA_DIR, "filtered_documents.json")
    outfile = os.path.join(OUT_DIR, "csv_chunks.jsonl")

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "w", encoding="utf-8") as out:
        for doc in json.load(f):
            if doc["source_type"] != "csv":
                continue
            out.write(json.dumps({
                "id": f"csv::{doc['doc_id']}",
                "text": normalize(doc["text"])
            }) + "\n")


def chunk_excel():
    infile = os.path.join(DATA_DIR, "filtered_documents.json")
    outfile = os.path.join(OUT_DIR, "excel_chunks.jsonl")

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "w", encoding="utf-8") as out:
        for doc in json.load(f):
            if doc["source_type"] != "excel":
                continue
            out.write(json.dumps({
                "id": f"excel::{doc['doc_id']}",
                "text": normalize(doc["text"])
            }) + "\n")


def run():
    chunk_relations()
    chunk_emails()
    chunk_csv()
    chunk_excel()


if __name__ == "__main__":
    run()
