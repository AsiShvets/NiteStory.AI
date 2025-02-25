# backend/app/services/readability_service.py

import textstat

def compute_readability(text: str) -> dict:
    """
    Compute Flesch Reading Ease and Flesch-Kincaid Grade Level for the given text.
    
    Parameters:
        text (str): The text to evaluate.
    
    Returns:
        dict: A dictionary containing:
            - 'flesch_reading_ease': A score between 0 and 100 where higher scores indicate easier readability.
            - 'flesch_kincaid_grade': The U.S. grade level required to understand the text.
    """
    # Flesch Reading Ease: higher score = easier to read
    reading_ease = textstat.flesch_reading_ease(text)
    
    # Flesch-Kincaid Grade Level: indicates the U.S. school grade level
    grade_level = textstat.flesch_kincaid_grade(text)
    
    return {
        "flesch_reading_ease": reading_ease,
        "flesch_kincaid_grade": grade_level
    }
