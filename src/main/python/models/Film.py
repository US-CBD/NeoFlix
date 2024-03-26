from py2neo import Node, Relationship

class Film:
    def __init__(self, title: str, release_date: str, director, description):
        self.title = title
        self.release_date = release_date
        self.director = director
        self.description = description
        self.actors = []
        self.genres = []
        self.opinions = []
        self.opinions = []


    def add_actor(self, actor):
        self.actors.append(actor)

    def add_genre(self, genre):
        self.genres.append(genre)

    def add_opinion(self, opinion):
        self.opinions.append(opinion)