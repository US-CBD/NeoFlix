import tkinter as tk
from tkinter.messagebox import showinfo
import customtkinter as ctk

from src.main.python.models.models import Opinion


class ReviewsFrame(ctk.CTkFrame):
    def __init__(self, parent, film, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.film = film
        self.settings = settings
        self.opinions = []
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)
        self.parent.pack_propagate(True)

        self.reviews_frame = ctk.CTkFrame(self)
        self.reviews_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.configure_widgets()

    def configure_widgets(self):
        self.add_label(self.reviews_frame, text="Reviews for " + self.film.title, row=0, column=0, sticky="w",
                       fg_color="gray30", corner_radius=9)

        self.opinions = self.settings.film.get_opinions()
        if self.opinions:
            for i, opinion in enumerate(self.opinions, start=1):
                self.add_label(self.reviews_frame, text=f"Opinion {i}:", row=i, column=0, sticky="w", fg_color="gray")
                self.add_textbox(self.reviews_frame, text=opinion.text, row=i, column=1, rowspan=2)
        else:
            self.add_label(self.reviews_frame, text="No opinions yet", row=1, column=0, sticky="w", fg_color="gray")

        # Add button to add a new opinion
        add_opinion_button = ctk.CTkButton(self.reviews_frame, text="Add Opinion", fg_color="gray",
                                           command=self.create_opinion_frame)
        add_opinion_button.grid(row=10, column=0, sticky="w", pady=(10, 0))

    def add_label(self, parent, text, row, column, sticky, fg_color=None, text_color=None, corner_radius=None):
        label = ctk.CTkLabel(parent, text=text, fg_color=fg_color, text_color=text_color, corner_radius=corner_radius)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)

    def add_textbox(self, parent, text, row, column, rowspan):
        textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6)
        textbox.insert("1.0", text)
        textbox.grid(row=row, column=column, columnspan=2, rowspan=rowspan, sticky="w", padx=5, pady=5)

    def create_opinion_frame(self):
        new_opinion_window = tk.Toplevel(self)
        new_opinion_window.title("Add New Opinion")

        new_opinion_frame = ctk.CTkFrame(new_opinion_window)
        new_opinion_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_label(new_opinion_frame, text="Enter your opinion about the film:", row=0, column=0, sticky="w",
                       fg_color="gray30", corner_radius=9)

        opinion_text_entry = ctk.CTkEntry(new_opinion_frame)
        opinion_text_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.add_label(new_opinion_frame, text="Enter your rating for the film (0-10):", row=2, column=0, sticky="w",
                       fg_color="gray30", corner_radius=9)

        rating_entry = ctk.CTkEntry(new_opinion_frame)
        rating_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        submit_button = ctk.CTkButton(new_opinion_frame, text="Submit", fg_color="gray",
                                      command=lambda: self.submit_opinion(new_opinion_window, opinion_text_entry.get(),
                                                                          rating_entry.get()))
        submit_button.grid(row=4, column=0, sticky="w")

    def submit_opinion(self, window, opinion_text, rating):
        try:
            rating = float(rating)
            if 0 <= rating <= 10:
                new_opinion = Opinion(opinion_text, rating, self.settings.user, self.film)
                self.settings.user.add_opinion(new_opinion)
                self.settings.user.create_or_update()
                showinfo("Success", "Opinion added successfully")
                window.destroy()
            else:
                showinfo("Error", "Rating must be between 0 and 10")
        except ValueError:
            showinfo("Error", "Invalid rating. Please enter a number between 0 and 10.")

