from py2neo import Node, Relationship

from src.main.python.repositories.repository import Repository


class OpinionRepository(Repository):
    """
    Repository for opinions in the Neo4j database.
    """

    def create_or_update(self, opinion: 'Opinion') -> None:
        """
        Creates or updates an opinion in the database.

        Args:
            opinion (Opinion): The opinion to create or update.
        """
        opinion_node = Node("Opinion", text=opinion.text, rating=opinion.rating)
        tx = self.graph.begin()
        tx.merge(opinion_node, "Opinion", "text")
        if opinion.user:
            user_node = Node("User", username=opinion.user.username)
            tx.merge(user_node, "User", "username")
            tx.create(Relationship(opinion_node, "WRITTEN_BY", user_node))
        if opinion.film:
            film_node = Node("Film", title=opinion.film.title)
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(film_node, "HAS_OPINION", opinion_node))
        tx.commit()

    @staticmethod
    def singleton() -> 'OpinionRepository':
        """
        Gets the singleton instance of this repository.

        Returns:
            OpinionRepository: The repository instance.
        """
        if not hasattr(OpinionRepository, "_instance"):
            OpinionRepository._instance = OpinionRepository()
        return OpinionRepository._instance
