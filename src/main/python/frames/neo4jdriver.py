from py2neo import Graph
import os
from configparser import ConfigParser 

# Connect to the Neo4j database
config = ConfigParser()

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.ini")
config.read(config_path)

uri = config.get("NEO4J", "uri")
username = config.get("NEO4J", "user")
password = config.get("NEO4J", "password")
graph = Graph(uri, auth=(username, password))

# Execute a Cypher query to retrieve all nodes and relationships
def get_all_films(graph):
    result = graph.run("MATCH (f:Film) RETURN f")
    films = [record["f"] for record in result]
    return films

def get_film_data(graph, title):
    query = f"MATCH (f:Film {{title: '{title}'}}) RETURN f"
    result = graph.run(query)
    film = result
    return film


film_data = get_film_data(graph, "Kung Fu Panda 4")
print (film_data)