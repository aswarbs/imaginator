from openai import OpenAI
from PIL import Image, ImageOps
import io, base64, os
from dotenv import load_dotenv
from logic.handlers import _update_image_display
from PIL import ImageTk
import traceback


# Load variables from .env into environment
load_dotenv()

# Get API key
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

def generate_image_variation(old_image: Image.Image, prompt: str, image_label, new_image_label, new_status_label, background):

    # Pick output aspect ratio based on background flag
    if background:
        size = "1536x1024"  # landscape
    else:
        size = "1024x1536"  # portrait

    # Build the base instruction depending on background flag
    if background:
        base_instruction = (
            "Create a digital illustration (non-ai looking) variation of this background, suitable for a game."
            "Match the sci-fi, musical galaxy theme."
        )
    else:
        base_instruction = (
            "Create a digital illustration (non-ai looking) variation of this image with a transparent background, suitable for a game."
            "Match the sci-fi, musical galaxy theme."
        )


    # Append user description if provided
    prompt = prompt.strip() if prompt else ""
    if prompt:
        full_prompt = f"{base_instruction} The image description is: {prompt}"
    else:
        full_prompt = base_instruction

    if not full_prompt.strip():
        new_status_label.config(text="Prompt cannot be empty — please provide a description.")
        return

    try:
        # Convert to PNG bytes
        old_image_resized = ImageOps.contain(old_image, (1024, 1024), Image.Resampling.LANCZOS)
        img_bytes = io.BytesIO()
        old_image_resized.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        image_file = ("image.png", img_bytes, "image/png")

        # API request — must use `images` list, not `image`
        response = client.images.edit(
            model="gpt-image-1",
            prompt=full_prompt,
            image=image_file,
            size=size
        )

        # Decode new image
        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        new_image = Image.open(io.BytesIO(image_bytes))

        # Update GUI
        tk_image = ImageTk.PhotoImage(new_image)
        new_image_label.configure(image=tk_image)
        new_image_label.image = tk_image
        new_image_label.original_image = new_image
        _update_image_display(new_image_label)

        new_status_label.config(text="New image generated.")

    except Exception as e:
        new_status_label.config(text=f"Error: {e}")
        print(traceback.format_exc())
