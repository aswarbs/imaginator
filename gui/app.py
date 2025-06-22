import tkinter as tk
from tkinter import ttk
from logic.handlers import on_click 

class ImaginatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Imaginator")
        self.geometry("1280x720")

        self.create_topbar()

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.create_files_list_frame()

        self.left_frame = ttk.Frame(self.main_frame, borderwidth=0)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.create_directory_select_frame()
        self.create_image_frame()

    def create_topbar(self):
        self.top_bar = ttk.Frame(self, padding=10, borderwidth=2, relief="ridge")
        self.top_bar.pack(side="top", fill="x")

        self.title_label = ttk.Label(self.top_bar, text="Imaginator", font=("Helvetica", 14, "bold"))
        self.title_label.pack()

    def create_image_frame(self):
        self.image_frame = ttk.Frame(self.left_frame, padding=10, borderwidth=2, relief="ridge")
        self.image_frame.pack(side="top", fill="both", expand=True)

        self.click_button = ttk.Button(self.image_frame, text="Click", command=lambda: on_click(self.status_label))
        self.click_button.pack(pady=5)

    def create_files_list_frame(self):
        self.files_list_frame = ttk.Frame(self.main_frame, padding=10, width=150, borderwidth=2, relief="ridge")
        self.files_list_frame.pack(side="right", fill="both", expand=True)

        self.right_label = ttk.Label(self.files_list_frame, text="Files")
        self.right_label.pack()

    def create_directory_select_frame(self):
        self.directory_select_frame = ttk.Frame(self.left_frame, padding=10, borderwidth=2, relief="ridge")
        self.directory_select_frame.pack(side="top", fill="x")

        self.status_label = ttk.Label(self.directory_select_frame, text="Not clicked")
        self.status_label.pack(pady=10)

def launch_app():
    app = ImaginatorApp()
    app.mainloop()
