import tkinter as tk
from tkinter import ttk
from logic.handlers import on_click

def launch_app():
    root = tk.Tk()
    root.title("Imaginator")
    root.geometry("640x360")

    label = ttk.Label(root, text="Not clicked")
    label.pack(pady=10)

    button = ttk.Button(root, text="Click", command=lambda: on_click(label))
    button.pack(pady=5)

    root.mainloop()
