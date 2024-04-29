import os

from src.main.python.models.models import User


class Settings:
    """
    Settings class to manage application settings.
    """

    def __init__(self):
        """
        Initializes the Settings instance.
        """
        self.selected_genres = []
        self.update_main = False
        self.update_favourites = False
        self.user = User(username=os.getenv("USERNAME"))
        self.user.save()

    def add_genre(self, genre: str) -> None:
        """
        Adds a genre to the list of selected genres.

        Args:
            genre (str): The genre to add.
        """
        self.selected_genres.append(genre)

    def remove_genre(self, genre: str) -> None:
        """
        Removes a genre from the list of selected genres.

        Args:
            genre (str): The genre to remove.
        """
        self.selected_genres.remove(genre)

    def check_genre(self, genre: str) -> bool:
        """
        Checks if a genre is selected.

        Args:
            genre (str): The genre to check.

        Returns:
            bool: True if the genre is selected, False otherwise.
        """
        return genre in self.selected_genres
