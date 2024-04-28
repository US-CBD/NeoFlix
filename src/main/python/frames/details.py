import tkinter.messagebox as tkmessagebox
from typing import Any, Tuple, List

import PIL.Image
import customtkinter as ctk
from PIL import Image
import networkx as nx
from numpy import record
from py2neo import Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from configparser import ConfigParser
import os, re
import matplotlib.pyplot as plt
from src.main.python.frames.review_frame import ReviewFrame

from customtkinter import CTkScrollableFrame

from src.main.python.frames.review_frame import ReviewFrame
from src.main.python.models.models import Film, Worker


class DetailFrame:
    def __init__(self, item: Any, settings: Any) -> None:
        """
        Initializes a DetailFrame object.

        Args:
            item (Any): The item to display details for.
            settings (Any): The settings for the frame.
        """
        self.root = ctk.CTkToplevel()
        self.item = item
        self.settings = settings
        self.initialize()
        self.root.mainloop()

    def initialize(self) -> None:
        """Initializes the DetailFrame."""
        self.root.title(self.item.name if hasattr(self.item, 'name') else self.item.title)
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        self.image_frame = ctk.CTkFrame(self.root)
        self.image_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.details_frame = ctk.CTkScrollableFrame(self.root, orientation="vertical", width=1200, height=1400)
        self.details_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.configure_widgets()

    def configure_widgets(self) -> None:
        """Configures widgets for the DetailFrame."""
        self.configure_image()
        self.configure_details()

    def configure_image(self) -> None:
        """Configures the image display."""
        try:
            print(self.item.get_path())
            pil_image = PIL.Image.open(self.item.get_path())
        except PIL.UnidentifiedImageError:
            pil_image = PIL.Image.new("RGB", (200, 400), "gray")

        ctk_image = ctk.CTkImage(pil_image, size=(200, 400))
        image_label = ctk.CTkLabel(self.image_frame, text="", image=ctk_image, width=200, height=400, corner_radius=6)
        image_label.pack(fill="both", expand=True)

    def configure_details(self) -> None:
        """Configures the details display."""
        pass  # This function will be implemented in subclasses

    def add_label(self, parent: Any, text: str, row: int, column: int, sticky: str, fg_color: str = None,
                  text_color: str = None, corner_radius: int = None, font: Tuple[str, int, str] = None,
                  cursor: str = None) -> Any:
        """
        Adds a label to the parent widget.

        Args:
            parent (Any): The parent widget.
            text (str): The text to display.
            row (int): The row position.
            column (int): The column position.
            sticky (str): The sticky configuration.
            fg_color (str, optional): The foreground color. Defaults to None.
            text_color (str, optional): The text color. Defaults to None.
            corner_radius (int, optional): The corner radius. Defaults to None.
            font (Tuple[str, int, str], optional): The font. Defaults to None.
            cursor (str, optional): The cursor style. Defaults to None.

        Returns:
            Any: The label widget.
        """
        label = ctk.CTkLabel(parent, text=text or "Not available", fg_color=fg_color, text_color=text_color,
                             corner_radius=corner_radius, font=font, cursor=cursor)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)
        return label

    def add_textbox(self, parent: Any, text: str, row: int, column: int, rowspan: int) -> None:
        """
        Adds a textbox to the parent widget.

        Args:
            parent (Any): The parent widget.
            text (str): The text to display.
            row (int): The row position.
            column (int): The column position.
            rowspan (int): The number of rows spanned.
        """
        textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6, width=400)
        textbox.insert("1.0", text or "Not available")
        textbox.grid(row=row, column=column, columnspan=2, rowspan=rowspan, sticky="w", padx=5, pady=5)


class DetailsFilmFrame(DetailFrame):
    def configure_details(self) -> None:
        """Configures details specific to films."""
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = self.add_label(title_frame, text=self.item.title, row=0, column=0, sticky="w",
                                          fg_color="gray30", corner_radius=9, font=("Helvetica", 24, "bold"),
                                          cursor="hand1")
        self.title_label.bind("<Button-1>", self.mark_as_favorite)
        self.update_favorite_button_text()

        self.add_label(self.details_frame, text=self.item.vote_average, row=0, column=1, sticky="w",
                       fg_color=self.get_color(self.item.vote_average), text_color="black", corner_radius=10,
                       font=("Helvetica", 12, "bold"))
        print(self.item.get_genres())
        if len(self.item.get_genres()) >= 1:
            self.add_label(self.details_frame, text="Genres: ", row=1, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons(self.details_frame, self.item.get_genres(), row=2, column=0)
        if len(self.item.get_directors()) >= 1:
            self.add_label(self.details_frame, text="Directors: ", row=3, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons_for_persons(self.details_frame,
                                                               self.item.get_directors(), row=4,
                                                               column=0)
        if len(self.item.get_actors()) >= 1:
            self.add_label(self.details_frame, text="Actors: ", row=5, column=0, sticky="w", fg_color="gray",
                           corner_radius=6, font=("Helvetica", 16, "bold"))
            self.add_scrollable_frame_with_buttons_for_persons(self.details_frame, self.item.get_actors(),
                                                               row=6, column=0)
        self.add_label(self.details_frame, text="Description: ", row=7, column=0, sticky="w", fg_color="gray",
                       corner_radius=6, font=("Helvetica", 16, "bold"))
        self.add_textbox(self.details_frame, text=self.item.description, row=8, column=0, rowspan=2)

        self.opinion_buttom = ctk.CTkButton(self.details_frame, text="👍 Give your opinion", fg_color="gray",
                                            command=self.open_opinion_frame)
        self.opinion_buttom.grid(row=10, column=0, sticky="w", pady=(10, 0))
        
        self.graph_buttom = ctk.CTkButton(self.details_frame, text="📊 Show graph", fg_color="gray"
                                          , command=self.show_graph)
        self.graph_buttom.grid(row=10, column=1, sticky="w", pady=(10, 0))

        if len(self.item.get_opinions()) >= 1:
            self.add_label(self.details_frame, text="Opinions: ", row=11, column=0, sticky="w", fg_color="gray")
            for i, opinion in enumerate(self.item.get_opinions()):
                self.add_label(self.details_frame, text=str(opinion), row=12 + i, column=0, sticky="w", fg_color="gray")

    def add_scrollable_frame_with_buttons(self, parent: CTkScrollableFrame, items: List[Any], row: int, column: int) -> None:
        """
        Adds a scrollable frame with buttons to the parent widget.

        Args:
            parent (CTkScrollableFrame): The parent widget.
            items (List[Any]): The items to display as buttons.
            row (int): The row position.
            column (int): The column position.
        """
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=500, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item, command=lambda genre=item: self.new_frame_genres(genre))
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)

    def new_frame_genres(self, genre):
        """
        Opens a new frame with the given genre.

        Args:
            genre (Any): The genre to display.
        """
        self.new_frame = ctk.CTkToplevel()
        self.new_frame.title(genre)
        self.new_frame.geometry("800x600")
        self.new_frame.resizable(False, False)
        self.new_frame.configure(bg="black")

        from src.main.python.frames.films_with_genre_frame import FilmsWithGenreFrames
        self.scrollable_frame = FilmsWithGenreFrames(self.new_frame, genre, self.settings, num_columns=4, size=(100, 100), width=700, height=150,)


    def open_opinion_frame(self) -> None:
        """Opens the opinion frame."""
        ReviewFrame(self.item, self.settings)


    def show_graph(self):
        config = ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "../config.ini")
        config.read(config_path)
        uri = config.get("NEO4J", "uri")
        user = config.get("NEO4J", "user")
        password = config.get("NEO4J", "password")
        graph = Graph(uri, auth=(user, password))
        query = f"MATCH (u:Film)-[a]->(m) WHERE u.title = '{self.item.title}' RETURN *"
        result = graph.run(query).data()
        G = nx.DiGraph()
        edge_labels = {}
        for r in result:
            film_node = r['u']
            other_node = r['m']
            match = re.search(r'\[:([^]]+)\]', str(r['a']))
            if match:
                relation_type = match.group(1)
            else:
                relation_type = ''
            try:
                G.add_edge(film_node['title'], other_node['name'])
            except Exception as e:
                print(other_node["text"])
                G.add_edge(film_node['title'], other_node["text"])
            if("name" in other_node):
                edge_labels[(film_node['title'], other_node['name'])] = relation_type
            elif("text" in other_node):
                edge_labels[(film_node['title'], other_node['text'])] = relation_type
            
        pos = nx.spring_layout(G)
        print(edge_labels)
        # Restablecer el estilo de Matplotlib
        plt.style.use('default')

        # Obtener los ejes actuales
        ax = plt.gca()
        
        # Establecer el color de fondo de los ejes utilizando el método set_facecolor
        ax.set_facecolor('black')
        
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=1.5)

        # Dibujar etiquetas de arista
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='black')

        plt.show()
        
    def get_color(self, rating: float) -> str:
        """
        Gets the color based on the rating.

        Args:
            rating (float): The rating value.

        Returns:
            str: The color string.
        """

        if rating >= 7.5:
            return "green"
        elif rating >= 5:
            return "yellow"
        else:
            return "red"

    def mark_as_favorite(self, event: Any) -> None:
        """
        Marks the item as favorite or removes it from favorites.

        Args:
            event (Any): The event triggering the function.
        """
        if self.settings.user.state_film(self.item):
            self.settings.user.remove_favorite_film(self.item)
            tkmessagebox.showinfo("Success", f"{self.item.title} removed from favorites")
        else:
            self.settings.user.add_favorite_film(self.item)
            tkmessagebox.showinfo("Success", f"{self.item.title} added to favorites")
        self.settings.update_favourites = True
        self.update_favorite_button_text()

    def update_favorite_button_text(self) -> None:
        """Updates the text of the favorite button."""
        if self.settings.user.state_film(self.item):
            self.title_label.configure(text=f"{self.item.title} ⭐️")
        else:
            self.title_label.configure(text=f"{self.item.title}")

    def add_scrollable_frame_with_buttons_for_persons(self, parent: CTkScrollableFrame, items: List[Worker], row: int, column: int) -> None:
        """
        Adds a scrollable frame with buttons for persons to the parent widget.

        Args:
            parent (CTkScrollableFrame): The parent widget.
            items (List[Worker]): The workers to display as buttons.
            row (int): The row position.
            column (int): The column position.
        """
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=500, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(items):
            button = ctk.CTkButton(scrollable_frame, text=item.name,
                                   command=lambda person=item: DetailsPersonFrame(person, self.settings))
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)


class DetailsPersonFrame(DetailFrame):
    def configure_details(self) -> None:
        """Configures details specific to persons."""
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = self.add_label(title_frame, text=self.item.name, row=0, column=0, sticky="w",
                                          fg_color="gray30", corner_radius=9, font=("Helvetica", 24, "bold"),
                                          cursor="hand1")

        self.add_label(self.details_frame, text="Biography:", row=1, column=0, sticky="w", fg_color="gray",
                       font=("Helvetica", 16, "bold"), corner_radius=6)
        self.add_textbox(self.details_frame, text=self.item.biography, row=2, column=0, rowspan=2)

        self.add_label(self.details_frame, text="Birthday:", row=4, column=0, sticky="w", fg_color="gray",
                       font=("Helvetica", 16, "bold"), corner_radius=6)
        self.add_label(self.details_frame, text=self.item.birthday, row=5, column=0, sticky="w", fg_color="gray")

        self.configure_films()

    def configure_films(self) -> None:
        """Configures films associated with the person."""
        films = self.item.get_films()
        self.add_label(self.details_frame, text="Films:", row=6, column=0, sticky="w",
                       fg_color="gray", font=("Helvetica", 16, "bold"), corner_radius=6)
        if len(films) == 0:
            self.add_label(self.details_frame, text="No films available", row=7, column=0, sticky="w",
                           fg_color="gray")
            return
        self.add_scrollable_frame_with_buttons_for_films(self.details_frame, films, row=7, column=0)

    def add_scrollable_frame_with_buttons_for_films(self, parent: CTkScrollableFrame, films: List[Film], row: int, column: int) -> None:
        """
        Adds a scrollable frame with buttons for films to the parent widget.

        Args:
            parent (CTkScrollableFrame): The parent widget.
            films (List[Film]): The films to display as buttons.
            row (int): The row position.
            column (int): The column position.
        """
        scrollable_frame = ctk.CTkScrollableFrame(parent, orientation="horizontal", width=200, height=30)
        scrollable_frame.grid(row=row, column=column, sticky="w", columnspan=2)
        for i, item in enumerate(films):
            button = ctk.CTkButton(scrollable_frame, text=item.title,
                                   command=lambda film=item: DetailsFilmFrame(film, self.settings))
            button.grid(row=row, column=i, sticky="w", padx=2, pady=2)

