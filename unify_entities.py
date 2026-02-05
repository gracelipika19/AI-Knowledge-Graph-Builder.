import json
import re
from collections import defaultdict
from difflib import SequenceMatcher

INPUT = "ingested_storage/clean_relations.json"
OUTPUT = "output/clusters.json"

def normalize(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return s

def similar(a, b, threshold=0.78):
    return SequenceMatcher(None, a, b).ratio() >= threshold

with open(INPUT, "r", encoding="utf-8") as f:
    rels = json.load(f)

names = set()
for r in rels:
    names.add(r["subject"])
    names.add(r["object"])

names = list(names)
clusters = []
visited = set()

for i, name in enumerate(names):
    if name in visited: continue
    base = normalize(name)
    group = [name]
    visited.add(name)
    for other in names[i+1:]:
        if other in visited: continue
        if similar(base, normalize(other)):
            group.append(other)
            visited.add(other)
    clusters.append(group)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(clusters, f, indent=4)

print(f"[✓] clusters saved -> {OUTPUT}, groups: {len(clusters)}")
