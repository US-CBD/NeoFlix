import customtkinter as ctk
from PIL import Image

from src.main.python.Settings import Settings
from src.main.python.frames.ScrollableFilmsFrames import ScrollableFilmsFrames
from src.main.python.models.models import Worker


class DetailsPersonFrame(ctk.CTkFrame):
    def __init__(self, parent, person, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.person = person
        self.settings = settings
        self.initialize()

    def initialize(self):
        self.parent.title(self.person.name)
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=1, padx=10, pady=10)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()
        self.configure_films()

    def configure_image(self):
        pil_image = Image.open(self.person.get_path())
        ctk_image = ctk.CTkImage(pil_image, size=(200, 400))
        image_label = ctk.CTkLabel(self.image_frame, text="", image=ctk_image, width=200, height=400, corner_radius=6)
        image_label.pack(fill="both", expand=True)

    def configure_details(self):
        title_frame = ctk.CTkFrame(self.details_frame)
        title_frame.grid(row=0, column=0, sticky="w")

        self.title_label = ctk.CTkLabel(title_frame, text=self.person.name, fg_color="gray30", corner_radius=9,
                                         font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.add_label(self.details_frame, text="Bibliography:", row=1, column=0, sticky="w",
                       fg_color="gray", font=("Helvetica", 12, "bold"))
        self.add_textbox(self.details_frame, text=self.person.bibliography, row=2, column=0, rowspan=2)

        self.add_label(self.details_frame, text="Birthday:", row=4, column=0, sticky="w",
                       fg_color="gray", font=("Helvetica", 12, "bold"))
        self.add_label(self.details_frame, text=self.person.birthday, row=5, column=0, sticky="w", fg_color="gray")

    def configure_films(self):
        films = self.person.get_films()
        if len(films) == 0:
            return
        scrollable_frame = ScrollableFilmsFrames(self.details_frame, films, self.settings, width=700, height=150)
        scrollable_frame.grid(row=6, column=0, sticky="ew")

    def add_label(self, parent, text, row, column, sticky, fg_color=None, text_color=None, corner_radius=None, font=None):
        label = ctk.CTkLabel(parent, text=text, fg_color=fg_color, text_color=text_color, corner_radius=corner_radius, font=font)
        label.grid(row=row, column=column, sticky=sticky, padx=5, pady=5)

    def add_textbox(self, parent, text, row, column, rowspan):
        textbox = ctk.CTkTextbox(parent, fg_color="gray", corner_radius=6)
        textbox.insert("1.0", text)
        textbox.grid(row=row, column=column, columnspan=2, rowspan=rowspan, sticky="w", padx=5, pady=5)


if __name__ == "__main__":
    root = ctk.CTk()
    frame = DetailsPersonFrame(root, Worker.find("Astrid Whettnall"), Settings())
    frame.grid(row=0, column=0)
    root.mainloop()