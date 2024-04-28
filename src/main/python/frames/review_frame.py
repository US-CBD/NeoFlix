from tkinter import messagebox as tkmessagebox

import customtkinter as ctk

from src.main.python.models.models import Opinion, Film
from src.main.python.settings import Settings


class ReviewFrame:
    def __init__(self, film: Film, settings: Settings) -> None:
        """
        Initializes a ReviewFrame object.

        Args:
            film (Film): The film to review.
            settings (Any): The settings.
        """
        self.root = ctk.CTkToplevel()
        self.film = film
        self.settings = settings
        self.initialize()

    def initialize(self) -> None:
        """Initializes the review frame."""
        self.root.title("Review")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.opinion_label = ctk.CTkLabel(self.scrollable_frame, text="Give your opinion", fg_color="gray30", corner_radius=6, font=("Helvetica", 12))
        self.opinion_label.pack(pady=(10, 5))

        self.opinion_textbox = ctk.CTkTextbox(self.scrollable_frame, fg_color="gray", corner_radius=6, font=("Helvetica", 10))
        self.opinion_textbox.pack(padx=20, pady=5, fill="x")

        self.opinion_rating_label = ctk.CTkLabel(self.scrollable_frame, text="Rating (0-10)", fg_color="gray", corner_radius=6, font=("Helvetica", 12))
        self.opinion_rating_label.pack(pady=(10, 5))

        self.opinion_rating = ctk.CTkTextbox(self.scrollable_frame, fg_color="gray", corner_radius=6, width=50, height=1, font=("Helvetica", 10))
        self.opinion_rating.pack(padx=20, pady=5)

        self.submit_button = ctk.CTkButton(self.scrollable_frame, text="Submit", fg_color="gray", corner_radius=6, font=("Helvetica", 12),
                                           command=self.submit_opinion)
        self.submit_button.pack(pady=(20, 5))

    def submit_opinion(self) -> None:
        """Submits the opinion."""
        opinion = self.opinion_textbox.get("1.0", "end-1c")
        rating = self.opinion_rating.get("1.0", "end-1c")

        if not opinion.strip() or not rating.strip():
            tkmessagebox.showerror("Error", "Please enter both opinion and rating.")
            return

        try:
            rating = float(rating)
            if not 0 <= rating <= 10:
                raise ValueError("Rating must be between 0 and 10.")
        except ValueError as e:
            tkmessagebox.showerror("Error", str(e))
            return

        opinion_object = Opinion(film=self.film, user=self.settings.user, text=opinion, rating=rating)
        opinion_object.save()
        self.film.add_opinion(opinion)
        tkmessagebox.showinfo("Success", "Opinion added successfully")



