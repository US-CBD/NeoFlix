from py2neo import Node, Relationship

from src.main.python.repositories.repository import Repository


class OpinionRepository(Repository):
    """
    Repositorio para opiniones en la base de datos Neo4j.
    """

    def create_or_update(self, opinion):
        """
        Crea o actualiza una opinión en la base de datos.

        Args:
            opinion (Opinion): La opinión a crear o actualizar.
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
    def singleton():
        if not hasattr(OpinionRepository, "_instance"):
            OpinionRepository._instance = OpinionRepository()
        return OpinionRepository._instance