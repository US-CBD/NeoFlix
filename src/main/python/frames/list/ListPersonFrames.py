import customtkinter as ctk

try:
    from src.main.python.frames.cards.CardPersonFrame import CardPersonFrame
except ModuleNotFoundError:
    from frames.cards.CardPersonFrame import CardPersonFrame


class AllFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, persons, settings, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.persons = persons
        self.settings = settings
        self.num_columns = num_columns
        self.size = size
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        for i, person in enumerate(self.persons):
            row = i // self.num_columns
            column = i % self.num_columns

            CardPersonFrame(self, person, self.settings, row, column, self.size)


    def update_persons(self, filtered_person):
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()
        self.persons = filtered_person
        self.initialize()
