import os

from py2neo import Node

from src.main.python.models.base import Base
from src.main.python.repositories.FilmRepository import FilmRepository
from src.main.python.repositories.OpinionRepository import OpinionRepository
from src.main.python.repositories.PersonRepository import PersonRepository
from src.main.python.repositories.UserRepository import UserRepository


class Film(Base):

    def __init__(self, title: str, release_date: str, description, file, vote_average=0.0, is_popular=False):
        self.title = title
        self.release_date = release_date
        self.directors = []
        self.description = description
        if file is None or not ("." in file or "/" in file) or file == "None" or file == "":
            self.url_image = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
        self.url_image = f'https://image.tmdb.org/t/p/original/{file}'
        if self.url_image == "https://image.tmdb.org/t/p/original/None":
            self.url_image = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
        self.url_image = f'https://image.tmdb.org/t/p/original/{file}'
        self.vote_average = vote_average
        self.is_popular = is_popular
        self.actors = []
        self.genres = []
        self.opinions = []
        super().__init__(FilmRepository.singleton())

    def __str__(self):
        return f"{self.title} ({self.release_date})"

    def add_director(self, director):
        self.directors.append(director)

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

    @staticmethod
    def find_by_genre(genre):
        return [Film.from_node(film) for film in FilmRepository.singleton().find_by_genre(genre)]

    @staticmethod
    def find_popular():
        return [Film.from_node(film) for film in FilmRepository.singleton().find_popular()]



    def get_path(self):
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../resources/images/films/')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder + self.title + "." + self.url_image.split('.')[-1])

    def get_director(self):
        self.director = [Worker.from_node(director) for director in
                         self.repository.find_director_for_film(self.title)]
        return self.director

    def get_actors(self):
        self.actors = list(set([Worker.from_node(actor) for actor in
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


class Worker(Base):
    def __init__(self, name: str, birthday: str, bibliography: str, department: str, file: str):
        self.name = name
        self.birthday = birthday
        self.bibliography = bibliography
        self.department = department
        if file is None or not ("." in file or "/" in file) or file == "None" or file == "":
            self.url_image = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
        self.url_image = f'https://image.tmdb.org/t/p/original/{file}'
        if self.url_image == "https://image.tmdb.org/t/p/original/None":
            self.url_image = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
        self.films = []
        super().__init__(PersonRepository.singleton())

    def add_film(self, film):
        self.films.append(film)

    @staticmethod
    def from_node(node):
        return Worker(name=node["name"], birthday=node["age"], bibliography=node["bibliography"])

    def to_node(self):
        return Node("Person", name=self.name, age=self.birthday, bibliography=self.bibliography)

    def get_acted_films(self):
        return [Film.from_node(film) for film in self.repository.find_acted_films(self.name)]

    def get_directed_films(self):
        return [Film.from_node(film) for film in self.repository.find_directed_films(self.name)]

    def get_films(self):
        return list(set(self.get_acted_films() + self.get_directed_films()))

    def get_path(self):
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../resources/images/persons/')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder + self.name + "." + self.url_image.split('.')[-1])


class Opinion(Base):
    def __init__(self, text, rating, user, film):
        self.text = text
        self.rating = rating
        self.user = user
        self.film = film
        super().__init__(OpinionRepository.singleton())

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