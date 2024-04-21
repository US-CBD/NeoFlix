import os
from typing import List, Union

import requests
from py2neo import NodeMatcher, RelationshipMatcher, Relationship, Node

from src.main.python.repositories.repository import Repository


class FilmRepository(Repository):
    """
    Repository for movies in the Neo4j database.
    """

    def create_or_update(self, film: 'Film') -> None:
        """
        Creates or updates a movie in the database.

        Args:
            film (Film): The movie to create or update.
        """
        node = Node("Film", title=film.title, release_date=film.release_date, description=film.description,
                    url_image=film.url_image, vote_average=film.vote_average, is_popular=film.is_popular)

        image_path = film.get_path()
        if not os.path.exists(image_path):
            print(f"Downloading image for {film.title}")
            image = requests.get(film.url_image)
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
        print("Committing transaction")
        tx.commit()
        print(f"Committed transaction for {film.title}")

    def _create_or_update_person_node(self, person: 'Person') -> Node:
        """
        Creates or updates a person node in the database.

        Args:
            person (Person): The person to create or update.

        Returns:
            Node: The created or updated person node.
        """
        node = Node("Person", name=person.name, age=person.birthday, bibliography=person.biography,
                    url_image=person.url_image)
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

    def _create_or_update_opinion_node(self, opinion: 'Opinion') -> Node:
        """
        Creates or updates an opinion node in the database.

        Args:
            opinion (Opinion): The opinion to create or update.

        Returns:
            Node: The created or updated opinion node.
        """
        node = Node("Opinion", text=opinion.text, rating=opinion.rating)
        self.graph.merge(node, "Opinion", "text")
        if opinion.user:
            user_node = Node("User", username=opinion.user.username)
            self.graph.merge(user_node, "User", "username")
            self.graph.merge(Relationship(node, "WRITTEN_BY", user_node))
        return node

    def contains(self, title: str) -> List[Node]:
        return self.graph.run("MATCH (f:Film) WHERE f.title CONTAINS $title RETURN DISTINCT f", title=title).data()

    def contains_by_genre(self, genre: str) -> List[Node]:
        return self.graph.run("MATCH (f:Film)-[:IN_GENRE]->(g:Genre) WHERE g.name CONTAINS $genre RETURN DISTINCT f",
                              genre=genre).data()

    def contains_by_actor(self, actor: str) -> List[Node]:
        return self.graph.run(
            f"MATCH (f:Film)-[:ACTED_BY]->(a:Person) WHERE a.name CONTAINS '{actor}' RETURN DISTINCT f").data()

    def contains_by_director(self, director: str) -> List[Node]:
        return self.graph.run(
            f"MATCH (f:Film)-[:DIRECTED_BY]->(d:Person) WHERE d.name CONTAINS '{director}' RETURN DISTINCT f").data()

    def find(self, title: str) -> Union[Node, None]:
        """
        Finds a movie by title in the database.

        Args:
            title (str): The title of the movie to find.

        Returns:
            Union[Node, None]: The found movie node, or None if not found.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film", title=title).first()

    def find_popular(self) -> List[Node]:
        """
        Finds popular movies in the database.

        Returns:
            list: List of nodes of popular movies.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film", is_popular=True)

    def find_by_genre(self, genre: str) -> List[Node]:
        """
        Finds movies by genre in the database.

        Args:
            genre (str): The genre to find.

        Returns:
            list: List of nodes of movies of the specified genre.
        """
        if genre_node := self.find_genre(genre):
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((None, genre_node), "IN_GENRE")
            return [film.start_node for film in films]
        return []

    def find_genre(self, genre: str) -> Union[Node, None]:
        """
        Finds the genre by name in the database.

        Args:
            genre (str): The genre to find.

        Returns:
            Union[Node, None]: The found genre node, or None if not found.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Genre", name=genre).first()

    def find_actors_for_film(self, title: str) -> List[Node]:
        """
        Finds the actors of a movie by title in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            list: List of nodes of actors involved in the movie.
        """
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            actors = matcher.match((film_node, None), "ACTED_BY")
            return [actor.end_node for actor in actors]
        return []

    def find_genres_for_film(self, title: str) -> List[Node]:
        """
        Finds the genres of a movie by title in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            list: List of nodes of genres of the movie.
        """
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            genres = matcher.match((film_node, None), "IN_GENRE")
            return [genre.end_node for genre in genres]
        return []

    def find_director_for_film(self, title: str) -> Union[Node, None]:
        """
        Finds the director of a movie by title in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            Union[Node, None]: The found director node, or None if not found.
        """
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            directors = matcher.match((film_node, None), "DIRECTED_BY")
            return [director.end_node for director in directors]
        return None

    def find_opinions_for_film(self, title: str) -> List[Node]:
        """
        Finds the opinions of a movie by title in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            list: List of nodes of opinions of the movie.
        """
        if film_node := self.find(title):
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((film_node, None), "HAS_OPINION")
            return [opinion.end_node for opinion in opinions]

        return []

    def find_all(self) -> List[Node]:
        """
        Finds all movies in the database.

        Returns:
            list: List of nodes of all movies.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("Film")

    def delete(self, film: 'Film') -> bool:
        """
        Deletes a movie from the database.

        Args:
            film (Film): The movie to delete.

        Returns:
            bool: True if the movie was successfully deleted, False if not found.
        """
        if film_node := self.find(film.title):
            tx = self.graph.begin()
            tx.delete(film_node)
            tx.commit()
            return True
        return False

    def exists(self, title: str) -> bool:
        """
        Checks if a movie exists in the database.

        Args:
            title (str): The title of the movie to check.

        Returns:
            bool: True if the movie exists, False if not exists.
        """
        return self.find(title) is not None

    @staticmethod
    def singleton() -> 'FilmRepository':
        """
        Gets the singleton instance of this repository.

        Returns:
            FilmRepository: The repository instance.
        """
        if not hasattr(FilmRepository, "_instance"):
            FilmRepository._instance = FilmRepository()
        return FilmRepository._instance

