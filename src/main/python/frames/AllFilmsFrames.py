from configparser import ConfigParser
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from py2neo import Graph
from src.main.python.frames.DetailsFilmFrame import DetailsFilmFrame
from src.main.python.frames.neo4jdriver import get_all_films, get_film_data

class AllFilmsFrames(ctk.CTkFrame):
    def __init__(self, parent_frame, films, num_columns=4, size=(100, 100), *args, **kwargs):
        super().__init__(parent_frame, *args, **kwargs)
        self.films = films
        self.num_columns = num_columns
        self.detail_frame = None # Initialize the details frame to None
        self.grid(sticky="nsew")
        self.initialize()

    def initialize(self):
        config = ConfigParser()

        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.ini")
        config.read(config_path)

        uri = config.get("NEO4J", "uri")
        username = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        graph = Graph(uri, auth=(username, password))

        self.films = get_all_films(graph)
        for i, film in enumerate(self.films):
            title = film.get('title')
            row = i // self.num_columns
            column = i % self.num_columns

            film_frame = ctk.CTkFrame(self)
            film_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            title_label = ctk.CTkLabel(film_frame, text=title, fg_color="gray30", corner_radius=6)
            title_label.pack()
            image_path = os.path.join(os.path.dirname(__file__), ".." ,".." ,"resources", "images", "films", f"{title}.jpg")
            film_image = Image.open(image_path)
            film_image = film_image.resize((50, 50), Image.ADAPTIVE)
            film_image = ImageTk.PhotoImage(film_image)

            image_label = tk.Label(film_frame, image=film_image)
            image_label.image = film_image # Keep a reference to the image to prevent it from being garbage collected
            image_label.pack()

            film_frame.bind("<Button-1>", lambda event, title=title, image_path=image_path: self.show_detail_frame(title, image_path))

            button = ctk.CTkButton(film_frame, text="Show details", command=lambda title=title, image_path=image_path: self.show_detail_frame(title, image_path))
            button.pack()

    def show_detail_frame(self, title, image_path):
        # Create a new top-level window
        config = ConfigParser()

        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.ini")
        config.read(config_path)

        uri = config.get("NEO4J", "uri")
        username = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        graph = Graph(uri, auth=(username, password))

        film_data = get_film_data(graph, title)

        # Create a new top-level window
        self.details_window = tk.Toplevel(self)
        self.details_window.configure(bg="black")

        # Create an instance of DetailsFilmFrame with the film data and pack it into the new window
        self.detail_frame = DetailsFilmFrame(self.details_window, title)
        self.detail_frame.pack()

        # Set the title of the details window
        self.details_window.title(title)

    def hide_detail_frame(self):
        if self.detail_frame:
            self.detail_frame.destroy()
            self.grid()


    def update_films(self, filtered_films):
        # Remove all current films from the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Add the filtered films to the frame
        for i, film in enumerate(filtered_films):
            title = film.get('title')
            row = i // self.num_columns
            column = i % self.num_columns

            film_frame = ctk.CTkFrame(self)
            film_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            title_label = ctk.CTkLabel(film_frame, text=title, fg_color="gray30", corner_radius=6)
            title_label.pack()

            image_path = os.path.join(os.path.dirname(__file__), ".." ,".." ,"resources", "images", "films", f"{title}.jpg")
            film_image = Image.open(image_path)
            film_image = film_image.resize((50, 50), Image.ADAPTIVE)
            film_image = ImageTk.PhotoImage(film_image)

            image_label = tk.Label(film_frame, image=film_image)
            image_label.image = film_image # Keep a reference to the image to prevent it from being garbage collected
            image_label.pack()

            film_frame.bind("<Button-1>", lambda event, title=title, image_path=image_path: self.show_detail_frame(title, image_path))

            button = ctk.CTkButton(film_frame, text="Show details", command=lambda title=title, image_path=image_path: self.show_detail_frame(title, image_path))
            button.pack()
