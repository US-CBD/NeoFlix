class User:
    def __init__(self, username):
        self.username = username
        self.opinions = []
        self.favorite_films = []

    def add_favorite_film(self, film):
        self.favorite_films.append(film)

    def add_opinion(self, opinion):
        self.opinions.append(opinion)