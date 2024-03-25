import customtkinter as ctk

from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames


class MainFrame:
    def __init__(self, settings, main_frame):
        self.settings = settings
        self.main_frame = main_frame

    def initialize(self):
        scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        scrollable_frame.pack(fill="both", expand=True)

        ###
        # TODO: Se montan los frames necesarios y se le pasan unos datos de prueba, los datos deberán de ser cargados desde settings y almacenados, aquí realizaremos una petición, siendo olos 4 primeros filtros de los N en ese caso.
        self.films_frames = [("Top Rated", ctk.CTkFrame(scrollable_frame), [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")]), ("Popular", ctk.CTkFrame(scrollable_frame), [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")]), ("Upcoming", ctk.CTkFrame(scrollable_frame), [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")])]
        for genres in ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]:
            self.films_frames.append((genres, ctk.CTkFrame(scrollable_frame), [("a", "../../resources/placeholder.jpg"), ("b", "../../resources/placeholder.jpg"), ("c", "../../resources/placeholder.jpg")]))
        ###
        self.configure()

    def configure(self):
        for i, (title, frame, films) in enumerate(self.films_frames):
            frame.grid(row=i, column=0, sticky="ew")
            title = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title.grid(row=0, column=0)
            scrollable_films_frame = ScrollableFilmsFrames(frame, films, width=700, height=150, size=(100, 100))
            scrollable_films_frame.grid(row=1, column=0, sticky="ew")


    def add_logic(self):
        # Realiza peticiones cada x tiempo con .after en el frame.
        pass