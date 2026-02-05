import json
import uuid
import re
from common import STORAGE, OUTPUT, chunk_text

INPUT = STORAGE + "/filtered_documents.json"
OUT_CHUNK = OUTPUT + "/email_chunks.jsonl"
OUT_META = OUTPUT + "/email_meta.jsonl"

def clean_email_header(text):
    lines = text.split("\n")
    keep = []
    body = []
    header_done = False

    for line in lines:
        low = line.lower()

        if not header_done:
            if low.startswith("from:") or low.startswith("to:") or low.startswith("subject:") or low.startswith("date:"):
                keep.append(line.strip())
                continue
            if ":" not in low:
                header_done = True

        if header_done:
            body.append(line.strip())

    return keep, " ".join(body)


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        docs = json.load(f)

    fw_c = open(OUT_CHUNK, "w", encoding="utf-8")
    fw_m = open(OUT_META, "w", encoding="utf-8")

    for doc in docs:
        if doc["source_type"] != "email":
            continue

        headers, body = clean_email_header(doc["text"])
        if len(body) < 30:
            continue

        for chunk in chunk_text(body):
            cid = str(uuid.uuid4())

            fw_c.write(json.dumps({"id": cid, "text": chunk}) + "\n")
            fw_m.write(json.dumps({
                "id": cid,
                "doc_id": doc["doc_id"],
                "type": "email",
                "headers": headers
            }) + "\n")

    fw_c.close()
    fw_m.close()

if __name__ == "__main__":
    main()
