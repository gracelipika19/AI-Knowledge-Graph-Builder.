import json
from collections import defaultdict

INPUT = "D:\Desktop\ML\info_pro\ingested_storage\clean_relations.json"

with open(INPUT, "r") as f:
    data = json.load(f)

nodes = set()
rels = defaultdict(list)

for item in data:
    s = item["subject"]
    p = item["predicate"]
    o = item["object"]

    nodes.add(s)
    nodes.add(o)
    rels[p].append((s, o))

print(f"Nodes: {len(nodes)}, Relations: {len(data)}")

open("schema.cypher", "w").write(
    "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE;\n"
)

with open("load_nodes.cypher", "w") as f:
    for n in nodes:
        f.write(f"MERGE (a:Entity {{id:'{n}'}});\n")

for i, (p, pairs) in enumerate(rels.items(), start=1):
    with open(f"load_rel_{i:02d}.cypher", "w") as f:
        for s, o in pairs:
            f.write(f"MATCH (a:Entity{{id:'{s}'}}),(b:Entity{{id:'{o}'}}) MERGE (a)-[:`{p}`]->(b);\n")
