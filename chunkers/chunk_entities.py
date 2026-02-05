import json
from common import STORAGE, OUTPUT

INPUT = STORAGE + "/extracted_entities.json"
OUT = OUTPUT + "/entities.jsonl"

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        ents = json.load(f)

    with open(OUT, "w", encoding="utf-8") as fw:
        for e in ents:
            fw.write(json.dumps(e) + "\n")

if __name__ == "__main__":
    main()
