import json
import uuid
import re
from common import STORAGE, OUTPUT

INPUT = STORAGE + "/clean_relations.json"
OUT = OUTPUT + "/relations_sentences.jsonl"


def clean(e):
    e = re.sub(r"http\S+", "", e)
    e = e.replace("_", " ")
    return e.strip().title()


def sem_rel(sub, pred, obj):
    pred_map = {
        "founder": "is founded by",
        "founded_by": "is founded by",
        "ceo": "is the CEO of",
        "owner": "is owned by",
        "member_of": "is a member of",
        "located_in": "is located in"
    }
    pred = pred_map.get(pred.lower(), f"has relation '{pred}' with")
    return f"{sub} {pred} {obj}."


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        rels = json.load(f)

    with open(OUT, "w", encoding="utf-8") as fw:
        for r in rels:
            sub = clean(r["subject"])
            obj = clean(r["object"])
            pred = clean(r["predicate"])

            if not sub or not obj or not pred:
                continue

            sentence = sem_rel(sub, pred, obj)
            fw.write(json.dumps({
                "id": str(uuid.uuid4()),
                "doc_id": r.get("doc_id"),
                "text": sentence
            }) + "\n")

if __name__ == "__main__":
    main()
