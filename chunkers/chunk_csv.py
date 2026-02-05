import json
import uuid
from common import STORAGE, OUTPUT, chunk_text

INPUT = STORAGE + "/filtered_documents.json"
OUT_CHUNK = OUTPUT + "/csv_chunks.jsonl"
OUT_META = OUTPUT + "/csv_meta.jsonl"

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        docs = json.load(f)

    fw_c = open(OUT_CHUNK, "w", encoding="utf-8")
    fw_m = open(OUT_META, "w", encoding="utf-8")

    for doc in docs:
        if doc["source_type"] != "csv":
            continue

        text = doc["text"]
        for chunk in chunk_text(text):
            cid = str(uuid.uuid4())
            fw_c.write(json.dumps({"id": cid, "text": chunk}) + "\n")
            fw_m.write(json.dumps({
                "id": cid,
                "doc_id": doc["doc_id"],
                "type": "csv"
            }) + "\n")

    fw_c.close()
    fw_m.close()

if __name__ == "__main__":
    main()
