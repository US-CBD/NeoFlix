from configparser import ConfigParser

from py2neo import Graph, Node, Relationship

class Repository:
    def __init__(self):
        config = ConfigParser()
        config.read("../config.ini")
        uri = config.get("NEO4J", "uri")
        user = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        self.graph = Graph(uri, auth=(user, password))

    def create_or_update(self, entity):
        raise NotImplementedError("This method must be implemented in the child class")

    def delete(self, entity):
        raise NotImplementedError("This method must be implemented in the child class")