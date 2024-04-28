from typing import Optional, List

from py2neo import Relationship, Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.repository import Repository


class UserRepository(Repository):
    """
    Repository for managing user data in the Neo4j database.
    """

    def create_or_update(self, user: 'User') -> None:
        """
        Creates or updates a user in the database.

        Args:
            user (User): The user to create or update.
        """
        node = Node("User", username=user.username)
        tx = self.graph.begin()
        tx.merge(node, "User", "username")
        for film in user.favorite_films:
            film_node = Node("Film", title=film.title, release_date=film.release_date, description=film.description)
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(node, "LIKES", film_node))
        for opinion in user.opinions:
            opinion_node = Node("Opinion", text=opinion.text, rating=opinion.rating)
            tx.merge(opinion_node, "Opinion", "text")
            tx.create(Relationship(node, "WRITTEN_BY", opinion_node))
        tx.commit()

    def find(self, username: str) -> Optional[Node]:
        """
        Finds a user by username in the database.

        Args:
            username (str): The username of the user to find.

        Returns:
            Node: The found user node, or None if not found.
        """
        matcher = NodeMatcher(self.graph)
        return matcher.match("User", username=username).first()

    def find_favourite_films(self, username: str) -> List[Node]:
        """
        Finds the favorite films of a user in the database.

        Args:
            username (str): The username of the user.

        Returns:
            List[Node]: List of favorite film nodes.
        """
        user_node = self.find(username)
        if user_node:
            matcher = RelationshipMatcher(self.graph)
            favourite_films = matcher.match((user_node, None), "LIKES")
            return [opinion.end_node for opinion in favourite_films]
        return []

    def find_favourite_film(self, username: str, title: str) -> Optional[Node]:
        """
        Finds a specific favorite film of a user in the database.

        Args:
            username (str): The username of the user.
            title (str): The title of the film.

        Returns:
            Node: The found film node, or None if not found.
        """
        user_node = self.find(username)
        if user_node:
            matcher = RelationshipMatcher(self.graph)
            favourite_film = matcher.match((user_node, None), "LIKES")
            for film in favourite_film:
                if film.end_node["title"] == title:
                    return film.end_node
        return None

    def find_opinions(self, username: str) -> List[Node]:
        """
        Finds the opinions written by a user in the database.

        Args:
            username (str): The username of the user.

        Returns:
            List[Node]: List of opinion nodes written by the user.
        """
        user_node = self.find(username)
        if user_node:
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((None, user_node), "WRITTEN_BY")
            return [opinion.start_node for opinion in opinions]
        return []

    def add_opinion(self, user: 'User', opinion: 'Opinion') -> bool:
        """
        Adds an opinion written by a user to the database.

        Args:
            user (User): The user writing the opinion.
            opinion (Opinion): The opinion to add.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        user_node = self.find(user.username)
        if user_node:
            opinion_node = Node("Opinion", text=opinion.text, rating=opinion.rating)
            tx = self.graph.begin()
            tx.merge(opinion_node, "Opinion", "text")
            tx.create(Relationship(user_node, "WRITTEN_BY", opinion_node))
            tx.commit()
            return True
        return False

    def delete(self, user: 'User') -> bool:
        """
        Deletes a user from the database.

        Args:
            user (User): The user to delete.

        Returns:
            bool: True if the user is successfully deleted, False otherwise.
        """
        user_node = self.find(user.username)
        if user_node:
            tx = self.graph.begin()
            tx.delete(user_node)
            tx.commit()
            return True
        return False

    def add_favorite_film(self, user: 'User', film: 'Film') -> bool:
        """
        Adds a film to the list of favorite films of a user in the database.

        Args:
            user (User): The user.
            film (Film): The film to add to favorites.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        user_node = self.find(user.username)
        if user_node:
            film_node = Node("Film", title=film.title, release_date=film.release_date, description=film.description)
            tx = self.graph.begin()
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(user_node, "LIKES", film_node))
            tx.commit()
            return True
        return False

    def remove_favorite_film(self, user: 'User', film: 'Film') -> bool:
        """
        Removes a film from the list of favorite films of a user in the database.

        Args:
            user (User): The user.
            film (Film): The film to remove from favorites.

        Returns:
            bool: True if the operation is successful, False otherwise.
        """
        user_node = self.find(user.username)
        if user_node:
            film_node = self.find_favourite_film(user.username, film.title)
            if film_node:
                relations = RelationshipMatcher(self.graph)
                relations = relations.match((user_node, film_node), "LIKES")
                for relation in relations:
                    tx = self.graph.begin()
                    tx.separate(relation)
                    tx.commit()
                return True
        return False

    def state_film(self, user: 'User', film: 'Film') -> bool:
        """
        Checks if a film is in the list of favorite films of a user in the database.

        Args:
            user (User): The user.
            film (Film): The film to check.

        Returns:
            bool: True if the film is in favorites, False otherwise.
        """
        return self.find(user.username) and self.find_favourite_film(user.username, film.title)

    @staticmethod
    def singleton() -> "UserRepository":
        """
        Get the singleton instance of UserRepository.

        Returns:
            UserRepository: The singleton instance.
        """
        if not hasattr(UserRepository, "_instance"):
            UserRepository._instance = UserRepository()
        return UserRepository._instance

