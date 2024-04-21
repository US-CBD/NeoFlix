import os
import time

import requests
from py2neo import NodeMatcher, RelationshipMatcher, Relationship, Node

from src.main.python.repositories.repository import Repository


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
        node = Node("Film", title=film.title, release_date=film.release_date, description=film.description, url_image=film.url_image, vote_average=film.vote_average, is_popular=film.is_popular)


        image_path = film.get_path()
        if not os.path.exists(image_path):
            print(f"Downloading image for {film.title}")
            image = requests.get(film.url_image)
            print(image)
            with open(image_path, "wb") as file:
                file.write(image.content)

        tx = self.graph.begin()
        tx.merge(node, "Film", "title")
        already_save = []
        for director in film.directors:
            print("Director: ", director.name)
            if director.name in already_save:
                continue
            director_node = self._create_or_update_person_node(director)
            tx.create(Relationship(node, "DIRECTED_BY", director_node))
        already_save = []
        for actor in film.actors:
            print("Actor: ", actor.name + " " + film.title)
            if actor.name in already_save:
                continue
            already_save.append(actor.name)
            actor_node = self._create_or_update_person_node(actor)
            tx.create(Relationship(node, "ACTED_BY", actor_node))
        already_save = []
        for genre in film.genres:
            print("Genre: ", genre + " " + film.title)
            if genre in already_save:
                continue
            already_save.append(genre)
            genre_node = Node("Genre", name=genre)
            tx.merge(genre_node, "Genre", "name")
            tx.create(Relationship(node, "IN_GENRE", genre_node))
        for opinion in film.opinions:
            print("Opinion: ", opinion.text + " " + film.title)
            opinion_node = self._create_or_update_opinion_node(opinion)
            tx.create(Relationship(node, "HAS_OPINION", opinion_node))
        print("Commiting transaction")
        tx.commit()
        print(f"Commited transaction for {film.title}")

    def _create_or_update_person_node(self, person):
        """
        Crea o actualiza un nodo de persona en la base de datos.

        Args:
            person (Person): La persona a crear o actualizar.

        Returns:
            Node: El nodo de persona creado o actualizado.
        """
        node = Node("Person", name=person.name, age=person.birthday, bibliography=person.bibliography, url_image=person.url_image)
        image_path = person.get_path()
        if not os.path.exists(image_path):
            print(f"Downloading image for {person.name}")
            print(image_path)
            try:
                image = requests.get(person.url_image)
                with open(image_path, "wb") as file:
                    file.write(image.content)
            except Exception as e:
                print(f"Error downloading image for {person.name}: {e}")
        self.graph.merge(node, "Person", "name")
        print("Person node created")
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
    
    def contains(self, title):
        return self.graph.run("MATCH (f:Film) WHERE f.title CONTAINS $title RETURN DISTINCT f", title=title).data()

    def contains_by_genre(self, genre):
        return self.graph.run("MATCH (f:Film)-[:IN_GENRE]->(g:Genre) WHERE g.name CONTAINS $genre RETURN DISTINCT f", genre=genre).data()
    def contains_by_actor(self, actor):
        return self.graph.run("MATCH (f:Film)-[:ACTED_BY]->(a:Person) WHERE a.name CONTAINS " +'"'+actor+ '"'+" RETURN DISTINCT f").data()

    def contains_by_director(self, director):
        return self.graph.run("MATCH (f:Film)-[:DIRECTED_BY]->(d:Person) WHERE d.name CONTAINS "+ '"'+director+'"'+" RETURN DISTINCT f").data()

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

    def find_popular(self):
        """
        Busca las películas populares en la base de datos.

        Returns:
            list: Lista de nodos de películas populares.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film", is_popular=True)

    def find_by_genre(self, genre):
        """
        Busca películas por género en la base de datos.

        Args:
            genre (str): El género a buscar.

        Returns:
            list: Lista de nodos de películas del género especificado.
        """
        if genre_node := self.find_genre(genre):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, genre_node), "IN_GENRE")
            return [film.start_node for film in films]
        return []

    def find_genre(self, genre):
        """
        Busca el gebrero por nombre en la base de datos.

        Args:
            genre (str): El gebrero a buscar.

        Returns:
            Node: El nodo de gebrero encontrado, o None si no se encuentra.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Genre", name=genre).first()

    def find_actors_for_film(self, title):
        """
        Busca los actores de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            list: Lista de nodos de actores que participan en la película.
        """
        if film_node := self.find(title):
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
        if film_node := self.find(title):
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
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            directors = matcher.match((film_node, None), "DIRECTED_BY")
            return [director.end_node for director in directors]
        return None

    def find_opinions_for_film(self, title):
        """
        Busca las opiniones de una película por título en la base de datos.

        Args:
            title (str): El título de la película.

        Returns:
            list: Lista de nodos de opiniones de la película.
        """
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((film_node, None), "HAS_OPINION")
            return [opinion.end_node for opinion in opinions]
            
        return []

    def find_all(self):
        """
        Busca todas las películas en la base de datos.

        Returns:
            list: Lista de nodos de todas las películas.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film")

    def delete(self, film):
        """
        Elimina una película de la base de datos.

        Args:
            film (Film): La película a eliminar.

        Returns:
            bool: True si la película se eliminó correctamente, False si no se encontró.
        """
        if film_node := self.find(film.title):
            tx = self.graph.begin()
            tx.delete(film_node)
            tx.commit()
            return True
        return False

    def exists(self, title):
        """
        Verifica si una película existe en la base de datos.

        Args:
            title (str): El título de la película a verificar.

        Returns:
            bool: True si la película existe, False si no existe.
        """
        return self.find(title) is not None

    @staticmethod
    def singleton():
        """
        Obtiene la única instancia de este repositorio.

        Returns:
            FilmRepository: La instancia del repositorio.
        """
        if not hasattr(FilmRepository, "_instance"):
            FilmRepository._instance = FilmRepository()
        return FilmRepository._instance
