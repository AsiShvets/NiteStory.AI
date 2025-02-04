from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow requests from frontend
origins = [
    "http://localhost:3000",  # If testing locally
    "https://solid-space-doodle-jx449j5rq9q3qx7x-3000.app.github.dev",  # Your GitHub Codespaces URL
]

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use defined origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)


# Image-to-text function
def img2text(path, model_name="Salesforce/blip-image-captioning-base"):
    img_to_text = pipeline(
        task="image-to-text",
        model=model_name,
        token=HUGGINGFACE_API_TOKEN
    )
    text = img_to_text(path)[0]['generated_text']
    return text

# Story generation function
def story_generator(scenario, model_choice):
    if model_choice == "OpenAI (GPT-3.5)":
        template = """
        You are an expert kids' storyteller.
        You generate long, engaging stories based on simple narratives.
        Your story should be more than 200 words, include rich details, characters, and a resolution.

        CONTEXT: {scenario}
        STORY:
        """
        prompt = PromptTemplate(template=template, input_variables=["scenario"])
        story_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        return story_llm.invoke(prompt.format(scenario=scenario))
    else:
        alternative_pipeline = pipeline("text-generation", model="gpt2")
        return alternative_pipeline(f"Write a story based on: {scenario}")[0]['generated_text']

# API Route: Image-to-Text
@app.post("/api/image-to-text")
async def image_to_text(file: UploadFile):
    file_path = f"./{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    scenario = img2text(file_path)
    return JSONResponse(content={"text": scenario})

# API Route: Story Generator
@app.post("/api/story-generator")
async def generate_story(scenario: str = Form(...), modelChoice: str = Form(...)):
    story = story_generator(scenario, modelChoice)
    return JSONResponse(content={"story": story})

@app.get("/")
def read_root():
    return {"message": "CORS fixed!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)