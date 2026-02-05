# rag_graph2.py
from neo4j import GraphDatabase

class GraphSearch:
    def __init__(self, uri="neo4j://localhost:7687", user="neo4j", password="graph123", db="graphrag"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.db = db

    def neighbors(self, ent, limit=5):
        with self.driver.session(database=self.db) as session:
            result = session.run(
                """
                MATCH (s:Entity {name:$e})-[r]->(m)
                RETURN type(r) as rel, m.name as neighbor LIMIT $limit
                """,
                e=ent,
                limit=limit
            )
            return [dict(rel=row["rel"], neighbor=row["neighbor"]) for row in result]
