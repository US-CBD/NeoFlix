import os

from src.main.python.models.models import User


class Settings:
    def __init__(self):
        self.selected_genres = []
        self.update = False
        self.user = User(username=os.getenv("USERNAME"))
        self.user.save()


    def add_genre(self, genre):
        self.selected_genres.append(genre)

    def remove_genre(self, genre):
        self.selected_genres.remove(genre)

    def check_genre(self, genre):
        return genre in self.selected_genres