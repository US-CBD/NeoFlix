import customtkinter as ctk
import tkinter as tk
import os
try:
    from src.main.python.frames.AllFilmsFrames import AllFilmsFrames
except ModuleNotFoundError:
    from frames.AllFilmsFrames import AllFilmsFrames

class FilterFrame:
    def __init__(self, settings, filter_frame):
        self.settings = settings
        self.filter_frame = filter_frame
        self.genres = []
        self.fav = []
        

    def initialize(self):
        # Crea un frame para los filtros
        top_frame = ctk.CTkFrame(self.filter_frame)
        top_frame.pack(fill="x")

        # Crea el dropdown button
        self.filter_option = tk.StringVar()
        self.filter_option.set("filter")
        dropdown_button = ctk.CTkButton(top_frame, textvariable=self.filter_option, command=self.open_menu)
        dropdown_button.grid(row=0, column=1)

        # Crea el search bar
        self.search_var = tk.StringVar()
        search_bar = ctk.CTkEntry(top_frame, textvariable=self.search_var)
        search_bar.grid(row=0, column=2)
        self.search_var.trace("w", self.filter_films)


        scrollable_frame = ctk.CTkScrollableFrame(self.filter_frame)
        scrollable_frame.pack(fill="both", expand=True)

        # Crea el dropdown menu
        self.dropdown_menu = ctk.CTkFrame(top_frame)
        for option in ["filter", "actor", "director", "film"]:
            button = ctk.CTkButton(self.dropdown_menu, text=option, command=lambda option=option: self.select_option(option))
            button.pack()

        self.films_frames = [("Filtro", ctk.CTkFrame(scrollable_frame), 
                      [(f"Pelicula{i}", os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../resources/placeholder.jpg")) for i in range(70)])]
        self.configure()

    def open_menu(self):
        # Abre el menu de opciones
        self.dropdown_menu.grid(row=1, column=1)

    def select_option(self, option):
        # Selecciona la opcion
        self.filter_option.set(option)
        self.dropdown_menu.grid_forget() 

    def filter_films(self, *args):
        filter_option = self.filter_option.get()
        search_text = self.search_var.get()
        for (title, frame, films), all_films_frame in zip(self.films_frames, self.all_films_frame):
            if filter_option == "film":
                filtered_films = [film for film in films if search_text.lower() in film[0].lower()]
            else:
                filtered_films = films
            
            all_films_frame.update_films(filtered_films)
            
    def configure(self):
        self.filter_frame.grid_rowconfigure(0, weight=1)
        self.filter_frame.grid_columnconfigure(0, weight=1)

        self.all_films_frame = []
        for i, (title, frame, films) in enumerate(self.films_frames):
            frame.grid(row=i, column=0, sticky="ew")
            title = ctk.CTkLabel(frame, text=title, fg_color="gray30", corner_radius=6)
            title.grid(row=0, column=0)
            all_films_frame = AllFilmsFrames(frame, films, width=700, height=150, size=(100, 100))
            all_films_frame.grid(row=1, column=0, sticky="nsew")
            self.all_films_frame.append(all_films_frame)



    
    def add_logic(self):
        # Realiza peticiones cada x tiempo con .after en el frame.
        pass