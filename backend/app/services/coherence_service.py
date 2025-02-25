# backend/app/services/coherence_service.py

import torch
from transformers import BartForConditionalGeneration, BartTokenizer, GPT2LMHeadModel, GPT2TokenizerFast

# Initialize the BART model and tokenizer for coherence scoring.
# We use the "facebook/bart-large" model; adjust as needed.
bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
bart_model.eval()

# Initialize the GPT-2 model and tokenizer for computing perplexity.
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
gpt2_model.eval()


def compute_bart_score(story: str) -> float:
    """
    Compute a coherence score for the story using a BART model.
    The story is fed as both input and target so that the model's loss
    (negative log likelihood) can be transformed into a score. A higher
    exponentiated score indicates better coherence and fluency.
    """
    # Tokenize the story with truncation for long inputs.
    inputs = bart_tokenizer(
        story,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )
    with torch.no_grad():
        # Compute loss by using the input as both source and target.
        outputs = bart_model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            labels=inputs["input_ids"]
        )
        # The loss is the average negative log-likelihood over the tokens.
        # We convert it to a score (higher is better) by taking the exponent of the negative loss.
        score = torch.exp(-outputs.loss)
    return score.item()


def compute_perplexity(story: str) -> float:
    """
    Compute the perplexity of the story using a GPT-2 model.
    Perplexity is computed by sliding over the text in chunks.
    Lower perplexity indicates that the text is more predictable and fluent.
    """
    # Encode the story text.
    encodings = gpt2_tokenizer(story, return_tensors="pt")
    input_ids = encodings.input_ids
    max_length = gpt2_model.config.n_positions
    stride = 512  # Adjust stride as necessary based on available resources.
    nlls = []

    # Slide over the input tokens in chunks.
    for i in range(0, input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = i + stride
        trg_len = end_loc - i  # Number of tokens to predict in this slice.
        input_ids_slice = input_ids[:, begin_loc:end_loc].clone()
        
        # Create labels with -100 to ignore tokens not in the target span.
        target_ids = input_ids_slice.clone()
        if trg_len < input_ids_slice.size(1):
            target_ids[:, :-trg_len] = -100
        
        with torch.no_grad():
            outputs = gpt2_model(input_ids_slice, labels=target_ids)
            # Multiply the loss by the target length to get the total loss for this slice.
            nll = outputs.loss * trg_len
        nlls.append(nll)
    
    # Total negative log-likelihood over the entire text.
    total_nll = torch.stack(nlls).sum()
    # Average negative log-likelihood per token.
    avg_nll = total_nll / input_ids.size(1)
    # Perplexity is the exponentiation of the average negative log-likelihood.
    perplexity = torch.exp(avg_nll)
    return perplexity.item()


def evaluate_coherence_flow(story: str) -> dict:
    """
    Evaluate the coherence and flow of the provided story.
    Returns a dictionary containing both the BARTScore and the Perplexity Score.
    """
    bart_score = compute_bart_score(story)
    perplexity_score = compute_perplexity(story)
    return {
        "bart_score": bart_score,
        "perplexity_score": perplexity_score
    }
