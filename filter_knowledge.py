import json, re

INPUT = "output/final_relations.json"
OUTPUT = "output/useful_relations.json"

EMAIL_NOISE = {
    "messageid","mimeversion","charsetusascii","contenttransferencoding",
    "xorigin","xfrom","xto","subject","date","time","folder","filename"
}

COMMON = {
    "buyer","meeting","dates","problem","terms","call","var","description",
    "fund","marketplace"
}

PROPER = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$")

out = []

with open(INPUT,"r",encoding="utf-8") as f:
    triples = json.load(f)

for r in triples:
    s = r["subject"].lower()
    o = r["object"].lower()

    # rule-1: remove email header noise
    if s in EMAIL_NOISE or o in EMAIL_NOISE:
        continue

    # rule-2: remove generic noun phrases
    if s in COMMON or o in COMMON:
        continue

    # rule-3: require at least one proper entity
    if not (PROPER.match(r["subject"]) or PROPER.match(r["object"])):
        continue

    out.append(r)

with open(OUTPUT,"w",encoding="utf-8") as f:
    json.dump(out,f,indent=4)

print(f"[OK] Reduced {len(triples)} → {len(out)} relations")
