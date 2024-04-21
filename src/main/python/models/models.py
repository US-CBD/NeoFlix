import os
from typing import List

from PIL import Image
from py2neo import Node
import customtkinter as ctk

from src.main.python.models.base import Base
from src.main.python.repositories.film_repository import FilmRepository
from src.main.python.repositories.opinion_repository import OpinionRepository
from src.main.python.repositories.person_repository import PersonRepository
from src.main.python.repositories.user_repository import UserRepository


class Film(Base):
    def __init__(self, title: str, release_date: str, description, file, vote_average=0.0, is_popular=False):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.url_image = self._get_url_image(file)
        self.vote_average = vote_average
        self.is_popular = is_popular
        self.directors = []
        self.actors = []
        self.genres = []
        self.opinions = []
        super().__init__(FilmRepository.singleton())
        self._load_image()

    def __str__(self):
        return f"{self.title} ({self.release_date})"

    def _get_url_image(self, file: str) -> str:
        if file and ('.' in file or '/' in file) and file != "None" and file != "":
            return f'https://image.tmdb.org/t/p/original/{file}'
        return "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

    def _load_image(self) -> None:
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.get_path())
        try:
            ctk.CTkImage(Image.open(image_path), size=(100, 100))
        except:
            self.url_image = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

    def add_director(self, director: 'Worker') -> None:
        self.directors.append(director)

    def add_actor(self, actor: 'Worker') -> None:
        self.actors.append(actor)

    def add_genre(self, genre: 'Genre') -> None:
        self.genres.append(genre)

    def add_opinion(self, opinion: 'Opinion') -> None:
        self.opinions.append(opinion)

    def to_node(self) -> Node:
        return Node("Film", title=self.title, release_date=self.release_date, description=self.description,
                    vote_average=self.vote_average, url_image=self.url_image, is_popular=self.is_popular,
                    path=self.get_path())

    @staticmethod
    def from_node(node: Node) -> 'Film':
        return Film(title=node["title"], release_date=node["release_date"], description=node["description"],
                    file=node["url_image"], vote_average=node["vote_average"], is_popular=node["is_popular"])

    @staticmethod
    def from_node2(node: Node) -> 'Film':
        film_node = node['f']
        return Film(
            title=film_node["title"],
            release_date=film_node["release_date"],
            description=film_node["description"],
            file=film_node["url_image"],
            is_popular=film_node.get("is_popular", False),
            vote_average=film_node.get("vote_average", 0.0)
        )

    @staticmethod
    def find_all() -> List['Film']:
        return [Film.from_node(film) for film in FilmRepository.singleton().find_all()]

    @staticmethod
    def find_by_title(title: str) -> List['Film']:
        return [Film.from_node(film) for film in FilmRepository.singleton().find(title)]

    @staticmethod
    def find_by_genre(genre: 'Genre') -> List['Film']:
        return [Film.from_node(film) for film in FilmRepository.singleton().find_by_genre(genre)]

    @staticmethod
    def contain_by_title(title: str) -> List['Film']:
        return [Film.from_node2(film) for film in FilmRepository.singleton().contains(title)]

    @staticmethod
    def contain_by_genre(genre: 'Genre') -> List['Film']:
        return [Film.from_node2(film) for film in FilmRepository.singleton().contains_by_genre(genre)]

    @staticmethod
    def contain_by_actor(actor: 'Worker') -> List['Film']:
        return [Film.from_node2(film) for film in FilmRepository.singleton().contains_by_actor(actor)]

    @staticmethod
    def contain_by_director(director: 'Worker') -> List['Film']:
        return [Film.from_node2(film) for film in FilmRepository.singleton().contains_by_director(director)]

    @staticmethod
    def find_popular() -> List['Film']:
        return [Film.from_node(film) for film in FilmRepository.singleton().find_popular()]

    @staticmethod
    def exists(title) -> bool:
        return FilmRepository.singleton().exists(title)

    def get_path(self) -> str:
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../resources/images/films/')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder + self.title + "." + self.url_image.split('.')[-1])

    def get_directors(self) -> List['Worker']:
        return [Worker.from_node(director) for director in self.repository.find_director_for_film(self.title)]

    def get_actors(self) -> List['Worker']:
        return [Worker.from_node(actor) for actor in self.repository.find_actors_for_film(self.title)]

    @staticmethod
    def get_directors_for_film(title: str) -> List['Worker']:
        return [Worker.from_node(director) for director in FilmRepository.singleton().find_director_for_film(title)]

    @staticmethod
    def get_actors_for_film(title: str) -> List['Worker']:
        return [Worker.from_node(actor) for actor in FilmRepository.singleton().find_actors_for_film(title)]

    def get_genres(self) -> List[str]:
        self.genres = list(
            set([genre["name"] for genre in self.repository.find_genres_for_film(self.title)] + self.genres))
        return self.genres

    def get_opinions(self) -> List['Opinion']:
        self.opinions = [Opinion.from_node(opinion) for opinion in self.repository.find_opinions_for_film(self.title)]
        return self.opinions

    def average_rating(self) -> float:
        opinions = self.get_opinions()
        return sum(opinion.rating for opinion in opinions) / len(opinions) if opinions else 0


class Worker(Base):
    def __init__(self, name: str, birthday: str, biography: str, department: str, file: str):
        self.name = name
        self.birthday = birthday
        self.biography = biography
        self.department = department
        self.url_image = self._get_url_image(file)
        self.films = []
        super().__init__(PersonRepository.singleton())

    def _get_url_image(self, file: str) -> str:
        if file and ('.' in file or '/' in file) and file != "None" and file != "":
            return f'https://image.tmdb.org/t/p/original/{file}'
        return "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

    def add_film(self, film: Film) -> None:
        self.films.append(film)

    @staticmethod
    def from_node(node: Node) -> 'Worker':
        return Worker(name=node["name"], birthday=node["age"], biography=node["biography"],
                      department=node["department"], file=node["url_image"])

    def to_node(self) -> Node:
        return Node("Person", name=self.name, age=self.birthday, biography=self.biography)

    def get_acted_films(self) -> List['Worker']:
        return [Film.from_node(film) for film in self.repository.find_acted_films(self.name)]

    def get_directed_films(self) -> List['Worker']:
        return [Film.from_node(film) for film in self.repository.find_directed_films(self.name)]

    def get_films(self) -> List[Film]:
        return list(set(self.get_acted_films() + self.get_directed_films()))

    def get_path(self) -> str:
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../resources/images/persons/')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder + self.name + "." + self.url_image.split('.')[-1])

    @staticmethod
    def exists(name: str) -> bool:
        return PersonRepository.singleton().exists(name)

    @staticmethod
    def find(name: str) -> 'Worker':
        return Worker.from_node(PersonRepository.singleton().find(name))

    @staticmethod
    def find_all() -> List['Worker']:
        return [Worker.from_node(person) for person in PersonRepository.singleton().find_all()]

    @staticmethod
    def find_by_department(department: str) -> List['Worker']:
        return [Worker.from_node(person) for person in PersonRepository.singleton().find_by_department(department)]


class Opinion(Base):
    def __init__(self, text: str, rating: int, user: 'User', film: Film) -> None:
        self.text = text
        self.rating = rating
        self.user = user
        self.film = film
        super().__init__(OpinionRepository.singleton())

    @staticmethod
    def from_node(node: Node) -> 'Opinion':
        return Opinion(node["text"], node["rating"], None, None)

    def to_node(self) -> Node:
        return Node("Opinion", text=self.text, rating=self.rating)

    def save(self):
        self.repository.create_or_update(self)

    def __str__(self):
        return f"Opinion: {self.text} Rating: {self.rating}"


class User(Base):
    def __init__(self, username: str) -> None:
        self.username = username
        self.opinions = []
        self.favorite_films = []
        super().__init__(UserRepository())

    def add_favorite_film(self, film: Film) -> bool:
        return self.repository.add_favorite_film(self, film)

    def remove_favorite_film(self, film: Film) -> bool:
        return self.repository.remove_favorite_film(self, film)

    def state_film(self, film: Film) -> bool:
        return self.repository.state_film(self, film)

    def add_opinion(self, opinion: Opinion) -> bool:
        return self.repository.add_opinion(self, opinion)

    @staticmethod
    def from_node(node: Node) -> 'User':
        return User(username=node["username"])

    def to_node(self) -> Node:
        return Node("User", username=self.username)

    def get_favorite_films(self) -> List[Film]:
        self.favorite_films = [Film.from_node(film) for film in self.repository.find_favourite_films(self.username)]
        return self.favorite_films

    def get_opinions(self) -> List[Opinion]:
        self.opinions = list(set([Opinion.from_node(opinion) for opinion in self.repository.find_opinions(self.username)] + self.opinions))
        return self.opinions
