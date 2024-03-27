from py2neo import Relationship, Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.Repository import Repository


class PersonRepository(Repository):
    """
    Repositorio para personas en la base de datos Neo4j.
    """

    def create_or_update(self, person):
        """
        Crea o actualiza una persona en la base de datos.

        Args:
            person (Person): La persona a crear o actualizar.
        """
        person_node = Node("Person", name=person.name, age=person.birthday, bibliography=person.bibliography)
        tx = self.graph.begin()
        tx.merge(person_node, "Person", "name")

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
        if person_node := self.find(name):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, person_node), "DIRECTED_BY")
            return [film.start_node for film in films]
        return []

    def find_acted_films(self, name):
        """
        Busca las películas en las que una persona actuó en la base de datos.

        Args:
            name (str): El nombre de la persona.

        Returns:
            list: Lista de nodos de películas en las que la persona actuó.
        """
        if person_node := self.find(name):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, person_node), "ACTED_BY")
            return [film.start_node for film in films]
        return []

    def delete(self, person):
        """
        Elimina una persona de la base de datos.

        Args:
            person (Person): La persona a eliminar.

        Returns:
            bool: True si la persona fue eliminada, False si no se encontró.
        """
        if person_node := self.find(person.name):
            tx = self.graph.begin()
            tx.delete(person_node)
            tx.commit()
            return True
        return False

    @staticmethod
    def singleton():
        if not hasattr(PersonRepository, "_instance"):
            PersonRepository._instance = PersonRepository()
        return PersonRepository._instance
