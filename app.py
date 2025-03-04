import streamlit as st
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import requests
import PyPDF2
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not HUGGINGFACE_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set. Check your .env file.")

# PDF Text Extraction
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Split PDF text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# Embed and store PDF context
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store(pdf_text):
    chunks = splitter.split_text(pdf_text)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

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

# Function to retrieve context from PDF
def retrieve_context(query, vector_store):
    docs = vector_store.similarity_search(query, k=3)
    return " ".join([doc.page_content for doc in docs])

# Function for story generation
def story_generator(scenario, model_choice, vector_store=None):
    if model_choice == "OpenAI (GPT-3.5)":
        template = """
        You are an expert kids' storyteller who can turn simple descriptions into magical, engaging tales.
        Create a captivating story with characters, dialogue, and a clear beginning, middle, and end.
        Add emotions, adventures, and a moral lesson at the end.
        
        IMAGE DESCRIPTION: {scenario}
        STORY:
        """
        prompt = PromptTemplate(template=template, input_variables=["scenario"])
        story_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

        # Add context from PDF for personalized story
        if vector_store:
            context = retrieve_context(scenario, vector_store)
            prompt_with_context = f"{context}\n\n{scenario}"
        else:
            prompt_with_context = scenario
        
        generated_story = story_llm.invoke(prompt.format(scenario=prompt_with_context))

        # Extract content from AIMessage object
        story_text = generated_story.content if hasattr(generated_story, 'content') else str(generated_story)
        return story_text.strip()

    elif model_choice == "Hugging Face (Alternative)":
        prompt = f"""
        You are a creative storyteller. Based on the following scenario, write an imaginative, detailed story for kids. 
        Include interesting characters, emotions, dialogue, and a happy ending.

        SCENARIO: {scenario}

        STORY:
        """
        # Use a smaller model like distilgpt2 to avoid space issues
        alternative_pipeline = pipeline("text-generation", model="gpt2-medium", revision="main")
        generated_text = alternative_pipeline(
            prompt,
            max_length=800,
            temperature=0.9,
            top_p=0.95,
            do_sample=True
        )[0]['generated_text']

        return generated_text.strip()

# Streamlit app
def main():
    st.set_page_config(page_title="AI Story Teller", page_icon="🤖")
    st.header("We turn images into stories!")

    # Model selection
    model_choice = st.selectbox(
        "Choose your language model:",
        ["OpenAI (GPT-3.5)", "Hugging Face (Alternative)"]
    )

    # Image upload
    upload_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    # PDF upload
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF content extracted successfully!")
        # Build the vector store once the PDF is uploaded
        vector_store = build_vector_store(pdf_text)

    if upload_file is not None:
        binary_data = upload_file.getvalue()
        with open(upload_file.name, "wb") as f:
            f.write(binary_data)
        st.image(upload_file, caption="Image Uploaded", width=700)

        # Process image and generate story
        scenario = img2text(upload_file.name)
        enriched_scenario = f"This image shows: {scenario}. Imagine an exciting adventure based on this scene."

        # Generate story based on image and model choice
        if st.button("Generate Story"):
            story = story_generator(enriched_scenario, model_choice)
            st.write("Generated Story:")
            st.write(story)

            # Add audio functionality
            st.audio("audio.flac")

        # Generate personalized story with context from PDF
        if st.button("Generate Personalized Story") and uploaded_file is not None:
            personalized_scenario = enriched_scenario + " Also, consider the context from the PDF content."
            personalized_story = story_generator(personalized_scenario, model_choice, vector_store)
            st.write("Generated Personalized Story:")
            st.write(personalized_story)
            
            # Add audio functionality for personalized story
            st.audio("audio.flac")

if __name__ == "__main__":
    main()
