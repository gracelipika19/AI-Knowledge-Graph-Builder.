import json

INPUT = "ingested_storage/clean_relations.json"
ALIAS = "output/alias_map.json"
OUTPUT = "output/canonical_relations.json"

rels = json.load(open(INPUT, encoding="utf-8"))
alias = json.load(open(ALIAS, encoding="utf-8"))

out = []
for r in rels:
    s = alias.get(r["subject"], r["subject"])
    o = alias.get(r["object"], r["object"])
    out.append({
        "subject": s,
        "predicate": r["predicate"].upper(),
        "object": o,
        "doc_id": r["doc_id"]
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=4)

print(f"[✓] saved -> {OUTPUT}, relations: {len(out)}")
