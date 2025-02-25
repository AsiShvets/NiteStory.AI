# backend/app/services/rouge_service.py

from rouge_score import rouge_scorer

def compute_rouge(candidate: str, reference: str) -> dict:
    """
    Compute ROUGE scores between a candidate and reference text.
    Returns a dictionary with ROUGE-1, ROUGE-2, and ROUGE-L f-measure scores.
    """
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    # For simplicity, we extract the f-measure for each metric.
    rouge_scores = {key: value.fmeasure for key, value in scores.items()}
    return rouge_scores

# Example usage:
if __name__ == "__main__":
    candidate_text = "The quick brown fox jumps over the lazy dog."
    reference_text = "A quick brown fox leaps over a lazy dog."
    rouge_scores = compute_rouge(candidate_text, reference_text)
    print("ROUGE scores:", rouge_scores)
