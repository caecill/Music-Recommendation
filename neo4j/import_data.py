from neo4j import GraphDatabase


URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "musik123"


class Neo4jConnection:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        )


    def close(self):
        self.driver.close()


    def query(self, query, params=None):

        with self.driver.session(database="musikdb") as session:

            result = session.run(
                query,
                params or {}
            )

            return [record.data() for record in result]