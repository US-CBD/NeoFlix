from configparser import ConfigParser
import os
from py2neo import Graph, Node, Relationship

class Repository:
    def __init__(self):
        config = ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "../config.ini")
        config.read(config_path)
        uri = config.get("NEO4J", "uri")
        user = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        self.graph = Graph(uri, auth=(user, password))

    def create_or_update(self, entity):
        raise NotImplementedError("This method must be implemented in the child class")

    def delete(self, entity):
        raise NotImplementedError("This method must be implemented in the child class")