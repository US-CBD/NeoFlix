from py2neo import Node

from src.main.python.models.base import Base
from src.main.python.repositories.FilmRepository import FilmRepository
from src.main.python.repositories.OpinionRepository import OpinionRepository
from src.main.python.repositories.PersonRepository import PersonRepository
from src.main.python.repositories.UserRepository import UserRepository


class Film(Base):

    def __init__(self, title: str, release_date: str, director, description):
        self.title = title
        self.release_date = release_date
        self.director = director
        self.description = description
        self.actors = []
        self.genres = []
        self.opinions = []
        super().__init__(FilmRepository())

    def add_actor(self, actor):
        self.actors.append(actor)

    def add_genre(self, genre):
        self.genres.append(genre)

    def add_opinion(self, opinion):
        self.opinions.append(opinion)

    def to_node(self):
        return Node("Film", title=self.title, release_date=self.release_date, description=self.description)

    @staticmethod
    def from_node(node):
        return Film(title=node["title"], release_date=node["release_date"], director=None,
                    description=node["description"])

    def get_director(self):
        self.director = [Person.from_node(director) for director in
                         self.repository.find_director_for_film(self.title)]
        return self.director

    def get_actors(self):
        self.actors = list(set([Person.from_node(actor) for actor in
                                self.repository.find_actors_for_film(self.title)] + self.actors))
        return self.actors

    def get_genres(self):
        self.genres = list(
            set([genre["name"] for genre in self.repository.find_genres_for_film(self.title)] + self.genres))
        return self.genres

    def get_opinions(self):
        self.opinions = list(set([Opinion.from_node(opinion) for opinion in self.repository.find_opinions_for_film(
            self.title)] + self.opinions)) + self.repository.find_opinions_for_film(self.title)
        return self.opinions

    def average_rating(self):
        if opinions := self.get_opinions():
            return sum(opinion.rating for opinion in opinions) / len(opinions)
        else:
            return 0

class Person(Base):
    def __init__(self, name: str, age: int, bibliography: str):
        self.name = name
        self.age = age
        self.bibliography = bibliography
        self.films = []
        super().__init__(PersonRepository())

    def add_film(self, film):
        self.films.append(film)

    @staticmethod
    def from_node(node):
        return Person(name=node["name"], age=node["age"], bibliography=node["bibliography"])

    def to_node(self):
        return Node("Person", name=self.name, age=self.age, bibliography=self.bibliography)

    def get_acted_films(self):
        return [Film.from_node(film) for film in self.repository.find_acted_films(self.name)]

    def get_directed_films(self):
        return [Film.from_node(film) for film in self.repository.find_directed_films(self.name)]

    def get_films(self):
        return list(set(self.get_acted_films() + self.get_directed_films()))


class Opinion(Base):
    def __init__(self, text, rating, user, film):
        self.text = text
        self.rating = rating
        self.user = user
        self.film = film
        super().__init__(OpinionRepository())

    @staticmethod
    def from_node(node):
        return Opinion(node["text"], node["rating"], None, None)

    def to_node(self):
        return Node("Opinion", text=self.text, rating=self.rating)


class User(Base):
    def __init__(self, username):
        self.username = username
        self.opinions = []
        self.favorite_films = []
        super().__init__(UserRepository())

    def add_favorite_film(self, film):
        self.favorite_films.append(film)

    def add_opinion(self, opinion):
        self.opinions.append(opinion)

    @staticmethod
    def from_node(node):
        return User(username=node["username"])

    def to_node(self):
        return Node("User", username=self.username)

    def get_favorite_films(self):
        self.favorite_films = list(set([Film.from_node(film) for film in self.repository.find_favourite_films(self.username)] + self.favorite_films))
        return self.favorite_films

    def get_opinions(self):
        self.opinions = list(set([Opinion.from_node(opinion) for opinion in self.repository.find_opinions(self.username)] + self.opinions))
        return self.opinions