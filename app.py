import streamlit as st
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import requests

# Load environment variables from .env file
load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not HUGGINGFACE_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set. Check your .env file.")

# Function for image-to-text using Hugging Face
def img2text(path, model_name="Salesforce/blip-image-captioning-base"):
    try:
        img_to_text = pipeline(
            task="image-to-text",
            model=model_name,
            token=HUGGINGFACE_API_TOKEN
        )
        text = img_to_text(path)[0]['generated_text']
        return text
    except FileNotFoundError:
        return "Error: The specified image file was not found."
    except Exception as e:
        return f"Error processing image: {e}"

# Function for story generation
def story_generator(scenario, model_choice):
    if model_choice == "OpenAI (GPT-3.5)":
        template = """
        You are an expert kids' storyteller.
        You can generate long and engaging stories based on a simple narrative.
        Your story should be more than 200 words and include rich details, characters, and a resolution with a happy ending or learning outcome.

        CONTEXT: {scenario}
        STORY:
        """
        prompt = PromptTemplate(template=template, input_variables=["scenario"])
        story_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        return story_llm.invoke(prompt.format(scenario=scenario))
    elif model_choice == "Hugging Face (Alternative)":
        # Example placeholder for an alternative model
        alternative_pipeline = pipeline("text-generation", model="gpt2")
        return alternative_pipeline(f"Write a story based on: {scenario}")[0]['generated_text']

# Function for text-to-speech using Hugging Face
def text2speech(msg):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payloads = {"inputs": str(msg)}
    response = requests.post(API_URL, headers=headers, json=payloads)
    if response.status_code == 200:
        with open("audio.flac", "wb") as f:
            f.write(response.content)
        return "Audio saved as audio.flac"
    else:
        return f"Error: {response.json().get('error', 'Unknown error')}"

# Streamlit app
def main():
    st.set_page_config(page_title="AI Story Teller", page_icon="🤖")
    st.header("We turn images into stories!")

    # Model selection
    model_choice = st.selectbox(
        "Choose your language model:",
        ["OpenAI (GPT-3.5)", "Hugging Face (Alternative)"]
    )

    upload_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    if upload_file is not None:
        binary_data = upload_file.getvalue()
        with open(upload_file.name, "wb") as f:
            f.write(binary_data)
        st.image(upload_file, caption="Image Uploaded", use_container_width=True)

        # Process image and generate story
        scenario = img2text(upload_file.name)
        story = story_generator(scenario, model_choice)
        text2speech(story)

        # Display scenario and story
        with st.expander("Scenario"):
            st.write(scenario)
        with st.expander("Story"):
            st.write(story)
        st.audio("audio.flac")

if __name__ == "__main__":
    main()
