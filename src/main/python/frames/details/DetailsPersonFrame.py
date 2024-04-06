import customtkinter as ctk
from PIL import ImageTk


class DetailsPersonFrame(ctk.CTkFrame):
    def __init__(self, parent, person, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.person = person
        self.initialize()

    def initialize(self):
        self.parent.geometry("800x600")
        self.parent.resizable(False, False)

        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=1)

        self.configure_widgets()

    def configure_widgets(self):
        self.configure_image()
        self.configure_details()

    def configure_image(self):
        photo = ImageTk.PhotoImage(file=self.person.get_path(), size=(10, 10))
        image_label = ctk.CTkLabel(self.image_frame, image=photo)
        image_label.grid(row=0, column=0)

    def configure_details(self):
        self.configure_row(self.details_frame, 0, data_text=self.person.title, is_title=True)
        self.configure_row(self.details_frame, 1, "Bibliography: ", self.person.bibliography, is_textbox=True)
        self.configure_row(self.details_frame, 2, "Birthdate: ", self.person.birthdate)

    def configure_row(self, parent, row, label_text, data_text, is_textbox=False, is_title=False):
        if label_text is not None:
            label = ctk.CTkLabel(parent, text=label_text, fg_color="gray")
            label.grid(row=row, column=0)

        if not is_textbox:
            data_label = ctk.CTkLabel(parent, text=data_text, fg_color="gray")
            data_label.grid(row=row + 1, column=0)
        elif is_title:
            title = ctk.CTkLabel(parent, text=data_text, fg_color="gray30", corner_radius=9)
            title.grid(row=row, column=0)
        else:
            textbox = ctk.CTkTextbox(parent, text=data_text, fg_color="gray", corner_radius=6)
            textbox.grid(row=row + 1, column=0, columnspan=2)
