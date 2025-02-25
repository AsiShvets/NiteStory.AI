# backend/app/services/pdf_service.py

import PyPDF2
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {e}")

# Initialize the text splitter and embeddings to be used when building the vector store.
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store(pdf_text: str):
    """
    Splits the PDF text into chunks and builds a FAISS vector store for similarity search.

    Args:
        pdf_text (str): The full text extracted from the PDF.

    Returns:
        FAISS: A FAISS vector store containing the embedded text chunks.
    """
    try:
        # Split the text into smaller chunks
        chunks = splitter.split_text(pdf_text)
        # Create a vector store from the chunks using the defined embeddings
        vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        raise Exception(f"Error building vector store: {e}")
