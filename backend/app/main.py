# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import nltk

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Story Teller API")

@app.on_event("startup")
async def startup_event():
    # Download the VADER lexicon when the app starts
    nltk.download('vader_lexicon')

# Configure CORS (adjust allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router with the /api prefix
from app.api.endpoints import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Story Teller API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
