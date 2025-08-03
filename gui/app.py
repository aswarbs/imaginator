import tkinter as tk
from tkinter import ttk
from logic.handlers import on_click, load_next_image
from logic.imageloader import ImageLoader
from logic.imagesaver import save_to_all_same_names

class ImaginatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Imaginator")
        self.geometry("1280x720")

        self.image_directory = "C:\\Users\\amber\\Documents\\Jazzhands\\jazzhands\\levelbank"
        self.loader = ImageLoader(self.image_directory)

        self.create_topbar()

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.create_files_list_frame()

        self.left_frame = ttk.Frame(self.main_frame, borderwidth=0)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.create_directory_select_frame()
        self.create_image_frame()

        load_next_image(self.loader, self.old_image_label, self.status_label, self.new_image_label)

    def create_topbar(self):
        self.top_bar = ttk.Frame(self, padding=10, borderwidth=2, relief="ridge")
        self.top_bar.pack(side="top", fill="x")

        self.title_label = ttk.Label(self.top_bar, text="Imaginator", font=("Helvetica", 14, "bold"))
        self.title_label.pack()

    def create_image_frame(self):
        self.image_frame = ttk.Frame(self.left_frame, padding=10, borderwidth=2, relief="ridge")
        self.image_frame.pack(side="top", fill="both", expand=True)

        # Top area contains OLD vs NEW
        self.top_area = ttk.Frame(self.image_frame)
        self.top_area.pack(side="top", fill="both", expand=True)

        # Use grid so we can split evenly
        self.top_area.columnconfigure(0, weight=1)
        self.top_area.columnconfigure(1, weight=1)
        self.top_area.rowconfigure(0, weight=1)

        # Left: OLD
        self.old_frame = ttk.Frame(self.top_area, padding=5, borderwidth=1, relief="solid")
        self.old_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        # Prevent inner widgets from resizing the frame
        self.old_frame.pack_propagate(False)

        self.old_label = ttk.Label(self.old_frame, text="OLD", font=("TkDefaultFont", 10, "bold"))
        self.old_label.pack(side="top", pady=(0, 5))

        self.old_image_label = ttk.Label(self.old_frame)
        self.old_image_label.pack(side="top", pady=5, fill="both", expand=True)

        self.status_label = ttk.Label(self.old_frame, text="Ready.")
        self.status_label.pack(side="top", pady=5)

        # Right: NEW
        self.new_frame = ttk.Frame(self.top_area, padding=5, borderwidth=1, relief="solid")
        self.new_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
        self.new_frame.pack_propagate(False)

        self.new_label = ttk.Label(self.new_frame, text="NEW", font=("TkDefaultFont", 10, "bold"))
        self.new_label.pack(side="top", pady=(0, 5))

        self.new_image_label = ttk.Label(self.new_frame)
        self.new_image_label.pack(side="top", pady=5, fill="both", expand=True)

        self.new_status_label = ttk.Label(self.new_frame, text="Preview.")
        self.new_status_label.pack(side="top", pady=5)

        # Bottom area: button stays fixed
        self.bottom_area = ttk.Frame(self.image_frame)
        self.bottom_area.pack(side="bottom", fill="x")

        # Prompt label on the left
        self.prompt_label = ttk.Label(self.bottom_area, text="Prompt:")
        self.prompt_label.pack(side="left", padx=(0, 5))


        self.prompt_entry = ttk.Entry(self.bottom_area, width=20)
        self.prompt_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))


        self.generate_button = ttk.Button(
            self.bottom_area,
            text="Generate",
            command=None
        )
        self.generate_button.pack(pady=5, fill="x")

        self.save_button = ttk.Button(
            self.bottom_area,
            text="Save",
            command=lambda:save_to_all_same_names(
            new_image=self.new_image_label.original_image,
            original_path=self.loader.current,
            root_dir=self.image_directory,
            extensions=None,
            case_insensitive=True,
            make_backup=True,
            backup_suffix=".bak"
        )
        )
        self.save_button.pack(pady=5, fill="x")

        self.click_button = ttk.Button(
            self.bottom_area,
            text="Next Image",
            command=lambda: (load_next_image(self.loader, self.old_image_label, self.status_label, self.new_image_label))
        )
        self.click_button.pack(pady=5, fill="x")



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
