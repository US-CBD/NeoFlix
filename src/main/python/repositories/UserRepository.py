from py2neo import Relationship, Node, NodeMatcher, RelationshipMatcher

from src.main.python.repositories.Repository import Repository


class UserRepository(Repository):

    def create_or_update(self, user):
        node = Node("User", username=user.username)
        tx = self.graph.begin()
        tx.merge(node, "User", "username")
        for film in user.favorite_films:
            film_node = Node("Film", title=film.title, release_date=film.release_date, director=film.director.name, description=film.description)
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(node, "LIKES", film_node))
        for opinion in user.opinions:
            opinion_node = Node("Opinion", text=opinion.text, username=opinion.username)
            tx.merge(opinion_node, "Opinion", "text")
            tx.create(Relationship(node, "OPINIONS", opinion_node))
        tx.commit()

    def create_or_update(self, user):
        node = Node("User", username=user.username)
        tx = self.graph.begin()
        tx.merge(node, "User", "username")
        for film in user.favorite_films:
            film_node = Node("Film", title=film.title, release_date=film.release_date, director=film.director.name, description=film.description)
            tx.merge(film_node, "Film", "title")
            tx.create(Relationship(node, "LIKES", film_node))
        for opinion in user.opinions:
            opinion_node = Node("Opinion", text=opinion.text, username=opinion.username)
            tx.merge(opinion_node, "Opinion", "text")
            tx.create(Relationship(node, "OPINIONS", opinion_node))
        tx.commit()

    def find(self, username):
        matcher = NodeMatcher(self.graph)
        user_node = matcher.match("User", username=username).first()
        return user_node

    def find_favorite_films(self, username):
        user_node = self.find(username)
        if user_node:
            matcher = RelationshipMatcher(self.graph)
            films = matcher.match((user_node, None), "LIKES")
            return [film.end_node for film in films]

    def find_opinions(self, username):
        user_node = self.find(username)
        if user_node:
            matcher = RelationshipMatcher(self.graph)
            opinions = matcher.match((user_node, None), "OPINIONS")
            return [opinion.end_node for opinion in opinions]
        return []

    def delete(self, username):
        user_node = self.find(username)
        if user_node:
            tx = self.graph.begin()
            tx.delete(user_node)
            tx.commit()
            return True
        return False