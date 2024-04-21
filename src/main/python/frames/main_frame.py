import customtkinter as ctk

from src.main.python.frames.scrollable_films_frames import ScrollableFilmsFrames
from src.main.python.models.models import Film
from src.main.python.settings import Settings


class MainFrame:
    def __init__(self, settings: Settings, main_frame: ctk.CTkFrame) -> None:
        """
        Initializes a MainFrame object.

        Args:
            settings (Settings): The settings for the frame.
            main_frame (ctk.): The main frame.
        """
        self.settings = settings
        self.main_frame = main_frame
        self.old_selected_genres = []

    def initialize(self) -> None:
        """Initializes the main frame."""
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.configure()

    def configure(self) -> None:
        """Configures the main frame."""
        self.films_frames = []
        self.create_scrollable_frame(Film.find_popular(), 0)

        for i, genre in enumerate(self.settings.selected_genres):
            films = Film.find_by_genre(genre.capitalize())
            self.create_scrollable_frame(films, i + 1, genre)

        self.main_frame.after(100, self.add_logic)

    def create_scrollable_frame(self, films: List[Film], row: int, title: Optional[str] = None) -> None:
        """Creates a scrollable frame."""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.grid(row=row, column=0, sticky="ew")

        if title:
            title_label = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title_label.grid(row=0, column=0)

        scrollable_films_frame = ScrollableFilmsFrames(frame, films, self.settings, width=700, height=150, size=(100, 100))
        scrollable_films_frame.grid(row=1, column=0, sticky="ew")

        self.films_frames.append((title, frame, films))

    def add_logic(self) -> None:
        """Adds logic to the main frame."""
        if self.old_selected_genres != self.settings.selected_genres and self.settings.update_main:
            self.old_selected_genres = list(self.settings.selected_genres)
            self.clear_frame_and_configure()
            self.settings.update_main = False

        self.main_frame.after(100, self.add_logic)

    def clear_frame_and_configure(self) -> None:
        """Clears the frame and reconfigures it."""
        for children in self.main_frame.winfo_children():
            children.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.configure()


