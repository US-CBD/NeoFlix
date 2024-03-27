from py2neo import Relationship, Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.Repository import Repository


class UserRepository(Repository):

    def create_or_update(self, user):
        node = Node("User", username=user.username)
        tx = self.graph.begin()
        tx.merge(node, "User", "username")
        for film in user.favorite_films:
            film_node = Node("Film", title=film.title, release_date=film.release_date, director=film.director.name,
                             description=film.description)
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(node, "LIKES", film_node))
        for opinion in user.opinions:
            opinion_node = Node("Opinion", text=opinion.text, username=opinion.username)
            tx.merge(opinion_node, "Opinion", "text")
            tx.create(Relationship(node, "WRITTEN_BY", opinion_node))
        tx.commit()

    def find(self, username):
        matcher = NodeMatcher(self.graph)
        return matcher.match("User", username=username).first()

    def find_favourite_films(self, username):
        if user_node := self.find(username):
            matcher = RelationshipMatcher(self.graph)
            favourite_films = matcher.match((user_node, None), "LIKES")
            return [opinion.end_node for opinion in favourite_films]

    def find_opinions(self, username):
        if user_node := self.find(username):
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((None, user_node), "WRITTEN_BY")
            return [opinion.start_node for opinion in opinions]
        return []

    def delete(self, user):
        if user_node := self.find(user.username):
            tx = self.graph.begin()
            tx.delete(user_node)
            tx.commit()
            return True
        return False

    @staticmethod
    def singleton():
        if not hasattr(UserRepository, "_instance"):
            UserRepository._instance = UserRepository()
        return UserRepository._instance
