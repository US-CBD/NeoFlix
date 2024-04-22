import os
from configparser import ConfigParser
from py2neo import Graph
from typing import Any


class Repository:
    def __init__(self) -> None:
        config = ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "../config.ini")
        config.read(config_path)
        uri = config.get("NEO4J", "uri")
        user = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        self.graph = Graph(uri, auth=(user, password))

    def create_or_update(self, entity: 'Base') -> None:
        """
        Creates or updates an entity in the database.

        Args:
            entity (Base): The entity to create or update.
        """
        raise NotImplementedError("This method must be implemented in the child class")

    def delete(self, entity: 'Base') -> None:
        """
        Deletes an entity from the database.

        Args:
            entity (Base): The entity to delete.
        """
        raise NotImplementedError("This method must be implemented in the child class")
