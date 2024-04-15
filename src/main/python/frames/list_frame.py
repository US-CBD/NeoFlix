import customtkinter as ctk

from src.main.python.frames.cards import CardFilmFrame, CardPersonFrame


class ListFrames(ctk.CTkScrollableFrame):
    def __init__(self, parent_frame, items, item_type, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.items = items
        self.num_columns = num_columns
        self.size = size
        self.settings = settings
        self.item_type = item_type
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        for i, item in enumerate(self.items):
            row = i // self.num_columns
            column = i % self.num_columns

            self.get_card_frame(item, row, column)

    def get_card_frame(self, item, row, column):
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, items):
        # Remove all current items from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.items = items
        self.initialize()


class ListFilmsFrames(ListFrames):
    def __init__(self, parent_frame, films, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, films, 'film', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, film, row, column):
        CardFilmFrame(self, film, self.settings, row, column, self.size)


class ListPersonsFrames(ListFrames):
    def __init__(self, parent_frame, persons, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, persons, 'person', settings, num_columns, size, *args, **kwargs)

    def get_card_frame(self, person, row, column):
        CardPersonFrame(self, person, self.settings, row, column, self.size)

