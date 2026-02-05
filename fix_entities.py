import json
import re

INPUT = "output/canonical_relations.json"
OUTPUT = "output/final_relations.json"

# patterns to remove
IRI = re.compile(r"httpwww\.wikidata\.orgentityq[0-9]+")

# nouns to drop
BAD = {"groups","networks","network","company","group","assembly","entity"}

def clean(ent):
    if IRI.fullmatch(ent):
        return None
    ent = ent.strip()
    ent = ent.replace("_"," ").replace("-"," ").title()
    return ent

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

out = []
for r in data:
    s = clean(r["subject"])
    o = clean(r["object"])
    if not s or not o: 
        continue
    if s.lower() in BAD or o.lower() in BAD:
        continue
    out.append({
        "subject": s,
        "predicate": r["predicate"].upper(),
        "object": o,
        "doc_id": r["doc_id"]
    })

with open(OUTPUT,"w",encoding="utf-8") as f:
    json.dump(out, f, indent=4)

print(f"[✓] SAVED {len(out)} cleaned triples → {OUTPUT}")
