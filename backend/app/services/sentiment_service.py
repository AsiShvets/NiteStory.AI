# backend/app/services/sentiment_service.py

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_emotional_depth(text: str) -> dict:
    """
    Analyze the emotional depth of the text using VADER sentiment analysis.
    
    Parameters:
        text (str): The input text to analyze.
    
    Returns:
        dict: A dictionary containing sentiment scores with keys 'neg', 'neu', 'pos', and 'compound'.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    return sentiment_scores
