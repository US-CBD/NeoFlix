import customtkinter as ctk
from PIL import Image, ImageTk


class DetailsPersonFrame(ctk.CTkFrame):
    def __init__(self, parent, person, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.person = person
        self.initialize()

    def initialize(self):
        self.parent.title(self.person.title)
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

    def configure_image(self):
        image = Image.open(self.person.get_path())
        image.thumbnail((200, 400))
        photo = ImageTk.PhotoImage(image)
        image_label = ctk.CTkLabel(self.image_frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.grid(row=0, column=0)

    def configure_details(self):
        title = ctk.CTkLabel(self.details_frame, text=self.person.title, font=("Helvetica", 16, "bold"),
                             fg_color="gray30")
        title.grid(row=0, column=0, sticky="w")

        bibliography = ctk.CTkLabel(self.details_frame, text="Bibliography:", font=("Helvetica", 12, "bold"),
                                    fg_color="gray")
        bibliography.grid(row=1, column=0, sticky="w", pady=(10, 5))

        bibliography_text = ctk.CTkTextbox(self.details_frame, text=self.person.bibliography, fg_color="gray",
                                           corner_radius=6, width=40, height=10)
        bibliography_text.grid(row=2, column=0, sticky="w")

        birthdate = ctk.CTkLabel(self.details_frame, text="Birthdate:", font=("Helvetica", 12, "bold"), fg_color="gray")
        birthdate.grid(row=3, column=0, sticky="w", pady=(10, 5))

        birthdate_text = ctk.CTkLabel(self.details_frame, text=self.person.birthdate, fg_color="gray")
        birthdate_text.grid(row=4, column=0, sticky="w")
