from py2neo import Relationship, Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.Repository import Repository


class PersonRepository(Repository):
    """
    Repositorio para personas en la base de datos Neo4j.
    """

    def find(self, name):
        """
        Busca una persona por nombre en la base de datos.

        Args:
            name (str): El nombre de la persona a buscar.

        Returns:
            Node: El nodo de persona encontrado, o None si no se encuentra.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Person", name=name).first()

    def find_directed_films(self, name):
        """
        Busca las películas dirigidas por una persona en la base de datos.

        Args:
            name (str): El nombre de la persona.

        Returns:
            list: Lista de nodos de películas dirigidas por la persona.
        """
        person_node = self.find(name)
        if person_node:
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((person_node, None), "DIRECTED_BY")
            return [film.end_node for film in films]
        return []

    def find_acted_films(self, name):
        """
        Busca las películas en las que una persona actuó en la base de datos.

        Args:
            name (str): El nombre de la persona.

        Returns:
            list: Lista de nodos de películas en las que la persona actuó.
        """
        person_node = self.find(name)
        if person_node:
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((person_node, None), "ACTED_BY")
            return [film.end_node for film in films]
        return []


    def delete(self, name):
        """
        Elimina una persona de la base de datos.

        Args:
            name (str): El nombre de la persona a eliminar.

        Returns:
            bool: True si la persona fue eliminada, False si no se encontró.
        """
        person_node = self.find(name)
        if person_node:
            tx = self.graph.begin()
            tx.delete(person_node)
            tx.commit()
            return True
        return False