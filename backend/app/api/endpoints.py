# backend/app/api/endpoints.py

import os
import tempfile
import base64
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

# Import service functions from the respective modules
from app.services.story_service import story_generator
from app.services.image_service import img2text
from app.services.pdf_service import extract_text_from_pdf, build_vector_store
from app.services.sentiment_service import analyze_emotional_depth
from app.services.readability_service import compute_readability  
from app.services.coherence_service import evaluate_coherence_flow 
from app.services.rouge_service import compute_rouge

router = APIRouter()

@router.get("/hello")
async def hello():
    """
    A simple endpoint to test the API.
    """
    return {"message": "Hello from the AI Story Teller API!"}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image, generate a caption, and show the uploaded image.
    """
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        caption = img2text(tmp_path)
        
        encoded_image = base64.b64encode(contents).decode('utf-8')
        image_data = f"data:{file.content_type};base64,{encoded_image}"
        os.remove(tmp_path)

        return {"caption": caption, "image": image_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF, extract text, and build a vector store for RAG.
    """
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        vector_store = build_vector_store(text)
        os.remove(tmp_path)

        return {"message": "PDF processed successfully.", "vector_store_info": "Vector store built."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-story")
async def generate_story_endpoint(
    scenario: str = Form(...),
    model_choice: str = Form(...)
):
    """
    Generate a story based on a provided scenario and model choice,
    and evaluate its sentiment and readability.
    """
    try:
        story = story_generator(scenario, model_choice)
        sentiment = analyze_emotional_depth(story)
        readability = compute_readability(story)
        return {"story": story, "sentiment": sentiment, "readability": readability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-story-from-image")
async def generate_story_from_image_endpoint(
    image: UploadFile = File(...),
    model_choice: str = Form(...),
    pdf: Optional[UploadFile] = File(None)
):
    """
    Accepts an image and an optional PDF.
    Generates a story based on the image (and PDF context, if provided),
    and evaluates its sentiment, readability, coherence, and ROUGE score
    using the PDF text as the reference.
    """
    try:
        # Process the image to generate a caption
        image_contents = await image.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as img_tmp:
            img_tmp.write(image_contents)
            img_tmp_path = img_tmp.name

        caption = img2text(img_tmp_path)
        os.remove(img_tmp_path)

        pdf_text = None
        vector_store = None
        # If a PDF is provided, extract its text and build a vector store
        if pdf is not None:
            pdf_contents = await pdf.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_tmp:
                pdf_tmp.write(pdf_contents)
                pdf_tmp_path = pdf_tmp.name

            pdf_text = extract_text_from_pdf(pdf_tmp_path)
            vector_store = build_vector_store(pdf_text)
            os.remove(pdf_tmp_path)

        # Generate the story using the caption, model choice, and PDF vector store (if available)
        story = story_generator(caption, model_choice, vector_store)
        sentiment = analyze_emotional_depth(story)
        readability = compute_readability(story)
        coherence = evaluate_coherence_flow(story)

        rouge_scores = None
        # Use the PDF text as the reference for ROUGE evaluation, if available.
        if pdf_text:
            rouge_scores = compute_rouge(story, pdf_text)

        response = {
            "caption": caption,
            "story": story,
            "sentiment": sentiment,
            "readability": readability,
            "coherence": coherence,
        }
        if rouge_scores is not None:
            response["rouge_scores"] = rouge_scores

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/evaluate-story")
async def evaluate_story_endpoint(story: str = Form(...)):
    """
    Evaluate the coherence and flow of a story using NLP metrics such as BARTScore and Perplexity Score.
    """
    try:
        evaluation = evaluate_coherence_flow(story)
        return {"evaluation": evaluation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
