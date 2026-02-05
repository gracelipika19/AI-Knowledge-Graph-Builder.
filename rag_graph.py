from neo4j import GraphDatabase

class GraphSearch:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="graph123", db="graphrag"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.db = db

    def neighbors(self, ent, limit=6):
        with self.driver.session(database=self.db) as session:
            result = session.run(
                """
                MATCH (a:Entity {name:$e})-[r]->(b)
                RETURN type(r) AS rel, b.name AS neighbor LIMIT $limit
                """,
                e=ent, limit=limit
            )
            return [dict(rel=row["rel"], neighbor=row["neighbor"]) for row in result]
