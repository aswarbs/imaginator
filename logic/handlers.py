from PIL import Image, ImageTk, ImageOps
import os

def on_click(label):
    label.config(text="Clicked!")

def _update_image_display(image_label, new_image_label):
    """Resize and display the stored original_image to fit the label's current size."""
    pil_image = getattr(image_label, "original_image", None)
    if pil_image is None:
        return  # nothing to do

    # Get current allocated size; if not yet laid out, try again shortly.
    width = image_label.winfo_width()
    height = image_label.winfo_height()
    if width <= 1 or height <= 1:
        image_label.after(50, lambda: _update_image_display(image_label, new_image_label))
        return

    # Preserve aspect ratio, fit within label size
    fitted = ImageOps.contain(pil_image, (width, height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(fitted)

    # Keep reference to avoid GC
    image_label.image = photo
    image_label.config(image=photo)
    new_image_label.image = photo
    new_image_label.config(image=photo)

def load_next_image(loader, image_label, status_label, new_image_label, max_display_size=(500, 500)):
    try:
        path = loader.next_image_path()
    except Exception as e:
        status_label.config(text=f"Error: {e}")
        return

    status_label.config(text=f"Showing: {os.path.basename(path)}")

    try:
        img = Image.open(path)
    except Exception as e:
        status_label.config(text=f"Failed to open image: {e}")
        return

    # Optionally pre-limit the image to a reasonable maximum to save memory
    img.thumbnail(max_display_size, Image.Resampling.LANCZOS)

    # Store the original (or pre-limited) image for dynamic resizing
    image_label.original_image = img.copy()
    new_image_label.original_image = img.copy()

    # Initial display
    _update_image_display(image_label, new_image_label)

    # Ensure future resizes adjust it
    def on_configure(event):
        _update_image_display(image_label, new_image_label)

    # Avoid binding multiple times
    if not hasattr(image_label, "_resize_bound"):
        image_label.bind("<Configure>", on_configure)
        image_label._resize_bound = True
        new_image_label.bind("<Configure>", on_configure)
        new_image_label._resize_bound = True
        
