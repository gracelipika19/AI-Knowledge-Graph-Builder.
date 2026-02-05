from neo4j import GraphDatabase
import json

URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "graph123"
DATABASE = "graphrag"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# === Load triples ===
with open("ingested_storage/clean_relations.json", "r", encoding="utf-8") as f:
    triples = json.load(f)

# === Batch loader ===
def insert_batch(tx, batch):
    for t in batch:
        pred = t["predicate"].upper().replace(" ", "_")
        tx.run(
            f"""
            MERGE (s:Entity {{name:$s}})
            MERGE (o:Entity {{name:$o}})
            MERGE (s)-[r:`{pred}` {{doc_id:$doc}}]->(o)
            """,
            s=t["subject"], o=t["object"], doc=t["doc_id"]
        )

# === Execute ===
BATCH_SIZE = 1000

with driver.session(database=DATABASE) as session:
    for i in range(0, len(triples), BATCH_SIZE):
        batch = triples[i:i + BATCH_SIZE]
        session.execute_write(insert_batch, batch)
        print(f"Loaded batch {i // BATCH_SIZE + 1}")

print("\n=== LOADED ALL TRIPLES INTO NEO4J ===\n")
driver.close()
