from typing import List, Optional

from py2neo import Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.repository import Repository


class PersonRepository(Repository):
    """
    Repository for people in the Neo4j database.
    """

    def create_or_update(self, person: 'Person') -> None:
        """
        Creates or updates a person in the database.

        Args:
            person (Person): The person to create or update.
        """
        person_node = Node("Person", name=person.name, age=person.birthday, bibliography=person.biography)
        tx = self.graph.begin()
        tx.merge(person_node, "Person", "name")
        tx.commit()

    def find_all(self) -> List[Node]:
        """
        Finds all people in the database.

        Returns:
            list: List of person nodes.
        """
        matcher = NodeMatcher(self.graph)
        return list(matcher.match("Person"))

    def find(self, name: str) -> Optional[Node]:
        """
        Finds a person by name in the database.

        Args:
            name (str): The name of the person to find.

        Returns:
            Node: The found person node, or None if not found.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Person", name=name).first()

    def find_directed_films(self, name: str) -> List[Node]:
        """
        Finds films directed by a person in the database.

        Args:
            name (str): The name of the person.

        Returns:
            list: List of film nodes directed by the person.
        """
        if person_node := self.find(name):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, person_node), "DIRECTED_BY")
            return [film.start_node for film in films]
        return []

    def find_acted_films(self, name: str) -> List[Node]:
        """
        Finds films in which a person acted in the database.

        Args:
            name (str): The name of the person.

        Returns:
            list: List of film nodes in which the person acted.
        """
        if person_node := self.find(name):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, person_node), "ACTED_BY")
            return [film.start_node for film in films]
        return []

    def delete(self, person: 'Person') -> bool:
        """
        Deletes a person from the database.

        Args:
            person (Person): The person to delete.

        Returns:
            bool: True if the person was deleted, False if not found.
        """
        if person_node := self.find(person.name):
            tx = self.graph.begin()
            tx.delete(person_node)
            tx.commit()
            return True
        return False

    def exists(self, name: str) -> bool:
        """
        Checks if a person exists in the database.

        Args:
            name (str): The name of the person to check.

        Returns:
            bool: True if the person exists, False if not.
        """
        return self.find(name) is not None

    @staticmethod
    def singleton() -> 'PersonRepository':
        """
        Gets the singleton instance of this repository.

        Returns:
            PersonRepository: The repository instance.
        """
        if not hasattr(PersonRepository, "_instance"):
            PersonRepository._instance = PersonRepository()
        return PersonRepository._instance

