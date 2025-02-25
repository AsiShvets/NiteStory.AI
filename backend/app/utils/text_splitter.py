# backend/app/utils/text_splitter.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_splitter(chunk_size: int = 500, chunk_overlap: int = 50) -> RecursiveCharacterTextSplitter:
    """
    Creates and returns a RecursiveCharacterTextSplitter instance with the specified parameters.

    Args:
        chunk_size (int): The maximum size of each text chunk.
        chunk_overlap (int): The number of overlapping characters between consecutive chunks.

    Returns:
        RecursiveCharacterTextSplitter: An instance configured with the provided parameters.
    """
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
