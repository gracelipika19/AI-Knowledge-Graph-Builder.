from neo4j import GraphDatabase
import json

# === 1. Neo4j Connection Configuration ===

URI = "neo4j://localhost:7687"   # local routing driver
USER = "neo4j"
PASSWORD = "graph123"            # change if needed
DATABASE = "infopro"             # your active DB

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# === 2. Load triples from JSON ===

with open("ingested_storage/clean_relations.json", "r", encoding="utf-8") as f:
    triples = json.load(f)

# === 3. Insert Triple Function ===

def insert_triple(tx, subject, predicate, object, doc_id):
    predicate = predicate.upper().replace(" ", "_")
    query = f"""
    MERGE (s:Entity {{name:$subject}})
    MERGE (o:Entity {{name:$object}})
    MERGE (s)-[r:`{predicate}` {{doc_id:$doc_id}}]->(o)
    """
    tx.run(query, subject=subject, object=object, doc_id=doc_id)

# === 4. Execute Triple Insertions ===

with driver.session(database=DATABASE) as session:
    for t in triples:
        session.execute_write(
            insert_triple,
            t["subject"],
            t["predicate"],
            t["object"],
            t["doc_id"]
        )

print("\n=== TRIPLES LOADED SUCCESSFULLY INTO NEO4J ===\n")

driver.close()
