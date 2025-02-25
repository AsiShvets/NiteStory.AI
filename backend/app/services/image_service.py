# backend/app/services/image_service.py

import os
from transformers import pipeline

# Retrieve the Hugging Face API token from environment variables.
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HUGGINGFACE_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set. Please check your .env file.")

def img2text(path: str, model_name: str = "Salesforce/blip-image-captioning-base") -> str:
    """
    Converts an image to text using a Hugging Face image-to-text model.

    Args:
        path (str): The file path to the image.
        model_name (str): The Hugging Face model name to use for captioning.

    Returns:
        str: The generated text from the image, or an error message if processing fails.
    """
    try:
        # Initialize the image-to-text pipeline with the provided model and API token.
        img_to_text = pipeline(
            task="image-to-text",
            model=model_name,
            token=HUGGINGFACE_API_TOKEN
        )
        # Process the image and extract the generated text.
        result = img_to_text(path)
        text = result[0].get("generated_text", "")
        return text
    except FileNotFoundError:
        return "Error: The specified image file was not found."
    except Exception as e:
        return f"Error processing image: {e}"
