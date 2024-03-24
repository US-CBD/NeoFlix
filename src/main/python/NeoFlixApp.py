import customtkinter as ctk

class NeoFlixApp:
    def __init__(self, app):
        self.app = app
        self.app.title("NeoFlix")
        self.app.geometry("800x600")
        self.app.configure(bg="black")
        self.app.resizable(False, False)
        self.app.iconbitmap("../resources/favicon.ico")

        self.app.mainloop()

if __name__ == "__main__":
    app = ctk.CTk()
    NeoFlixApp(app)
