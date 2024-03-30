from configparser import ConfigParser
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
from py2neo import Graph

from src.main.python.frames.neo4jdriver import get_all_films, get_film_data
class DetailsFilmFrame(ctk.CTkFrame):
    def __init__(self, parent, title, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        config = ConfigParser()

        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.ini")
        config.read(config_path)
        uri = config.get("NEO4J", "uri")
        username = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        graph = Graph(uri, auth=(username, password))

        film_data = get_film_data(graph, title)

        self.image_label = ctk.CTkLabel(self)
        self.image_label.pack()
        self.parent = parent
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)
        # Create title label
        self.title_label = ctk.CTkLabel(self, text="Title:")
        self.title_label_name = ctk.CTkLabel(self, text=title)
        self.title_label.pack()
        self.title_label_name.pack()

        # Create rating label
        self.rating_label = ctk.CTkLabel(self, text="Rating:")
        self.rating_label.pack()

        # Create genres label
        self.genres_label = ctk.CTkLabel(self, text="Genres:")
        self.genres_label.pack()

        # Create director label
        self.director_label = ctk.CTkLabel(self, text="Director:")
        self.director_label.pack()

        # Create actors label
        self.actors_label = ctk.CTkLabel(self, text="Actors:")
        self.actors_label.pack()

        # Create description label
        self.description_label = ctk.CTkLabel(self, text="Description:")
        self.description_label.pack()

        # Create close button
        self.close_button = ctk.CTkButton(self, text="Cerrar", command=self.close_details)
        self.close_button.pack()

        # Load and display the film image
        image = Image.open(os.path.join(os.path.dirname(__file__), ".." ,".." ,"resources", "images", "films", f"{title}.jpg"))
        img_resized = image.resize((10, 10))
        photo = ImageTk.PhotoImage(img_resized)
        self.image_label.configure(image=photo)
        self.image_label.image = photo # Keep a reference to the image to prevent it from being garbage collected

        # Update the labels with the film data
        self.update_details(title, os.path.join(os.path.dirname(__file__), ".." ,".." ,"resources", "images", "films", f"{title}.jpg"))

    def close_details(self):
        # Close the details window
        self.destroy()
        self.master.destroy()

    def update_details(self, title, image_path):
        # Update film details in the frame
        self.title_label_name.configure(text=title)


        # Load and display the film image
        image = Image.open(image_path)
        img_resized = image.resize((100, 200))
        photo = ImageTk.PhotoImage(img_resized)
        self.image_label.configure(image=photo)
        self.image_label.image = photo # Keep a reference to the image to prevent it from being garbage collected
    def initialize(self):
        # Create the GUI.
        pass

    def configure(self):
        # Configure the functionality.
        pass

    def add_logic(self):
        # Make requests every x time with .after on the frame.
        pass