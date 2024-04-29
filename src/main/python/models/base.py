from py2neo import Node

from src.main.python.repositories.repository import Repository


class Base:
    def __init__(self, repository: Repository) -> None:
        """
        Initializes a Base object.

        Args:
            repository (Any): The repository.
        """
        self.repository = repository

    def save(self) -> None:
        """Saves the object."""
        self.repository.create_or_update(self)

    def delete(self) -> None:
        """Deletes the object."""
        self.repository.delete(self)

    def to_node(self) -> Node:
        """Converts the object to a node."""
        raise NotImplementedError("This method must be implemented in the child class")

    @staticmethod
    def from_node(self, node: Node) -> 'Base':
        """Converts a node to an object."""
        raise NotImplementedError("This method must be implemented in the child class")
