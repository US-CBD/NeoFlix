class Settings:
    def __init__(self):
        self.selected_genres = ['Action'] # TODO: Cambiar
        self.update = False

    def add_genre(self, genre):
        self.selected_genres.append(genre)

    def remove_genre(self, genre):
        self.selected_genres.remove(genre)

    def check_genre(self, genre):
        return genre in self.selected_genres