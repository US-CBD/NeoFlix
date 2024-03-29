import customtkinter as ctk
try:
    from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames
except ModuleNotFoundError:
    from frames.ScrollableFilmsFrames import ScrollableFilmsFrames

class MainFrame:
    def __init__(self, settings, main_frame):
        self.settings = settings
        self.main_frame = main_frame

    def initialize(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True)

        ###
        # TODO: Se montan los frames necesarios y se le pasan unos datos de prueba, los datos deberán de ser cargados desde settings y almacenados, aquí realizaremos una petición, siendo olos 4 primeros filtros de los N en ese caso.
        self.old_selected_genres = list(self.settings.selected_genres)
        self.configure()

    def configure(self):
        self.films_frames = [
            ("Top Rated", ctk.CTkFrame(self.scrollable_frame),
             [("a", "../../resources/placeholder.jpg"),
              ("b", "../../resources/placeholder.jpg"),
              ("c", "../../resources/placeholder.jpg")])]

        for genres in self.settings.selected_genres:
            self.films_frames.append(
                (genres, ctk.CTkFrame(self.scrollable_frame), [("a", "../../resources/placeholder.jpg"),
                                                               ("b", "../../resources/placeholder.jpg"),
                                                               ("c",
                                                                "../../resources/placeholder.jpg")]))
        for i, (title, frame, films) in enumerate(self.films_frames):
            frame.grid(row=i, column=0, sticky="ew")
            title = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title.grid(row=0, column=0)
            scrollable_films_frame = ScrollableFilmsFrames(frame, films, width=700, height=150, size=(100, 100))
            scrollable_films_frame.grid(row=1, column=0, sticky="ew")

        self.main_frame.after(100, self.add_logic)


    def add_logic(self):
        if self.old_selected_genres != self.settings.selected_genres and self.settings.update:
            self.old_selected_genres = list(self.settings.selected_genres)
            for children in self.main_frame.winfo_children():
                children.destroy()
            self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
            self.scrollable_frame.pack(fill="both", expand=True)
            self.configure()
            self.settings.update = False
        self.main_frame.after(100, self.add_logic)
