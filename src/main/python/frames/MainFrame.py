import customtkinter as ctk

from src.main.python.models.models import Film

try:
    from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames
except ModuleNotFoundError:
    from frames.ScrollableFilmsFrames import ScrollableFilmsFrames

class MainFrame:
    def __init__(self, settings, main_frame):
        self.settings = settings
        self.main_frame = main_frame
        self.old_selected_genres = []

    def initialize(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.configure()

    def configure(self):
        self.films_frames = []

        self.create_scrollable_frame(Film.find_popular(), 0)

        for i, genre in enumerate(self.settings.selected_genres):
            films = Film.find_by_genre(genre)
            print(genre)
            print(films)
            self.create_scrollable_frame(films, i + 1, genre)

        self.main_frame.after(100, self.add_logic)

    def create_scrollable_frame(self, films, row, title=None):
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew")

        if title:
            title_label = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title_label.grid(row=0, column=0)

        print(films)
        scrollable_films_frame = ScrollableFilmsFrames(frame, films, width=700, height=150, size=(100, 100))
        scrollable_films_frame.grid(row=1, column=0, sticky="ew")


        self.films_frames.append((title, frame, films))

    def add_logic(self):
        if self.old_selected_genres != self.settings.selected_genres and self.settings.update:
            self.old_selected_genres = list(self.settings.selected_genres)
            self.clear_frame_and_configure()
            self.settings.update = False

        self.main_frame.after(100, self.add_logic)

    def clear_frame_and_configure(self):
        for children in self.main_frame.winfo_children():
            children.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.configure()

