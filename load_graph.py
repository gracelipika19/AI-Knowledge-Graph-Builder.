import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "graph123"
DB = "graphrag"  # keep your existing DB name

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with open("output/useful_relations.json", "r", encoding="utf-8") as f:
    rels = json.load(f)

def insert(tx, s, p, o, doc):
    p = p.upper().replace(" ", "_")
    tx.run(
        f"""
        MERGE (a:Entity {{name:$s}})
        MERGE (b:Entity {{name:$o}})
        MERGE (a)-[:`{p}` {{doc_id:$doc}}]->(b)
        """,
        s=s, o=o, doc=doc
    )

with driver.session(database=DB) as session:
    for r in rels:
        session.execute_write(
            insert,
            r["subject"],
            r["predicate"],
            r["object"],
            r["doc_id"]
        )

print("✓ Graph loaded into Neo4j")

driver.close()
