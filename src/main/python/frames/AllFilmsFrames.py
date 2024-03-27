import math
import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class AllFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films, num_columns=6, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.num_columns = num_columns
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        num_films = len(self.films)

        # Add the films to the frame
        for i, (title, image) in enumerate(self.films):
            # Calculate the row and column for the current film
            row = i // self.num_columns
            column = i % self.num_columns

            # Create a frame for the film
            film_frame = ctk.CTkFrame(self)
            film_frame.grid(row=row, column=column, padx=10, sticky="nsew") 

            # Create a label for the film title
            title_label = ctk.CTkLabel(film_frame, text=title, fg_color="gray30", corner_radius=6)
            title_label.pack()

            # Load and resize the image
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), image)
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.ADAPTIVE)  
            image = ImageTk.PhotoImage(image)

            # Create a label for the film image
            image_label = tk.Label(film_frame, image=image)
            image_label.image = image  
            image_label.pack()

    def update_films(self, filtered_films):
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the filtered films to the frame
        for i, film in enumerate(filtered_films):
            # Calculate the row and column for the current film
            row = i // self.num_columns
            column = i % self.num_columns

            # Create a frame for the film
            film_frame = ctk.CTkFrame(self)
            film_frame.grid(row=row, column=column, padx=10, sticky="nsew")  
            
            # Create a label for the film title
            title_label = ctk.CTkLabel(film_frame, text=film[0])  
            title_label.pack()

            # Load and resize the image
            image_path = film[1]  
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.ADAPTIVE)  
            image = ImageTk.PhotoImage(image)

            # Create a label for the film image
            image_label = tk.Label(film_frame, image=image)
            image_label.image = image  
            image_label.pack()