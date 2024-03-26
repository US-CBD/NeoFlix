from py2neo import NodeMatcher, RelationshipMatcher, Relationship, Node
from src.main.python.repositories.Repository import Repository

class FilmRepository(Repository):
    """
    Repositorio para películas en la base de datos Neo4j.
    """

    def create_or_update(self, film):
        """
        Crea o actualiza una película en la base de datos.

        Args:
            film (Film): La película a crear o actualizar.
        """
        node = Node("Film", title=film.title, release_date=film.release_date, description=film.description)
        tx = self.graph.begin()
        tx.merge(node, "Film", "title")
        if film.director:
            director_node = self._create_or_update_person_node(film.director)
            tx.create(Relationship(node, "DIRECTED_BY", director_node))
        for actor in film.actors:
            actor_node = self._create_or_update_person_node(actor)
            tx.create(Relationship(node, "ACTED_BY", actor_node))
        for genre in film.genres:
            genre_node = Node("Genre", name=genre)
            tx.merge(genre_node, "Genre", "name")
            tx.create(Relationship(node, "IN_GENRE", genre_node))
        for opinion in film.opinions:
            opinion_node = self._create_or_update_opinion_node(opinion)
            tx.create(Relationship(node, "HAS_OPINION", opinion_node))
        tx.commit()

    def _create_or_update_person_node(self, person):
        """
        Crea o actualiza un nodo de persona en la base de datos.

        Args:
            person (Person): La persona a crear o actualizar.

        Returns:
            Node: El nodo de persona creado o actualizado.
        """
        node = Node("Person", name=person.name, age=person.age, bibliography=person.bibliography)
        self.graph.merge(node, "Person", "name")
        return node

    def _create_or_update_opinion_node(self, opinion):
        """
        Crea o actualiza un nodo de opinión en la base de datos.

        Args:
            opinion (Opinion): La opinión a crear o actualizar.

        Returns:
            Node: El nodo de opinión creado o actualizado.
        """
        node = Node("Opinion", text=opinion.text, rating=opinion.rating)
        self.graph.merge(node, "Opinion", "text")
        if opinion.user:
            user_node = Node("User", username=opinion.user.username)
            self.graph.merge(user_node, "User", "username")
            self.graph.merge(Relationship(node, "WRITTEN_BY", user_node))
        return node

    def find(self, title):
        """
        Busca una película por título en la base de datos.

        Args:
            title (str): El título de la película a buscar.

        Returns:
            Node: El nodo de película encontrado, o None si no se encuentra.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film", title=title).first()

    def find_actors_for_film(self, title):
        """
        Busca los actores de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            list: Lista de nodos de actores que participan en la película.
        """
        film_node = self.find(title)
        if film_node:
            matcher = RelationshipMatcher(self.graph)
            actors = matcher.match((film_node, None), "ACTED_BY")
            return [actor.end_node for actor in actors]
        return []

    def find_genres_for_film(self, title):
        """
        Busca los géneros de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            list: Lista de nodos de géneros de la película.
        """
        film_node = self.find(title)
        if film_node:
            matcher = RelationshipMatcher(self.graph)
            genres = matcher.match((film_node, None), "IN_GENRE")
            return [genre.end_node for genre in genres]
        return []

    def find_director_for_film(self, title):
        """
        Busca el director de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            Node: El nodo de director encontrado, o None si no se encuentra.
        """
        film_node = self.find(title)
        if film_node:
            matcher = RelationshipMatcher(self.graph)
            director_rel = matcher.match((film_node, None), "DIRECTED_BY").first()
            return director_rel.end_node
        return None

    def find_opinions_for_film(self, title):
        """
        Busca las opiniones de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            list: Lista de nodos de opiniones de la película.
        """
        film_node = self.find(title)
        if film_node:
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((None, film_node), "HAS_OPINION")
            return [opinion.start_node for opinion in opinions]
        return []

    def delete(self, title):
        """
        Elimina una película de la base de datos por título.

        Args:
            title (str): El título de la película a eliminar.

        Returns:
            bool: True si la película se eliminó correctamente, False si no se encontró.
        """
        film_node = self.find(title)
        if film_node:
            tx = self.graph.begin()
            tx.delete(film_node)
            tx.commit()
            return True
        return False
