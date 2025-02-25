# backend/app/services/story_service.py

from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.services.rouge_service import compute_rouge  # New import

# Global variable for the Hugging Face pipeline; initially None.
_hf_pipeline = None

def get_hf_pipeline():
    """
    Lazily load and return the Hugging Face pipeline.
    This ensures the heavy model is only loaded upon the first request.
    """
    global _hf_pipeline
    if _hf_pipeline is None:
        _hf_pipeline = pipeline(
            "text-generation",
            model="ajibawa-2023/Young-Children-Storyteller-Mistral-7B",
            trust_remote_code=True  # required for this model
        )
    return _hf_pipeline

def retrieve_context(query: str, vector_store) -> str:
    """
    Retrieve context from the vector store based on the query.
    """
    docs = vector_store.similarity_search(query, k=3)
    return " ".join([doc.page_content for doc in docs])

def story_generator(scenario: str, model_choice: str, vector_store=None) -> str:
    """
    Generate a story based on the given scenario and model choice.
    """
    if model_choice == "OpenAI (GPT-3.5)":
        template = (
            "You are an expert kids' storyteller who can turn simple descriptions into magical, engaging tales.\n"
            "Create a captivating story with characters, dialogue, and a clear beginning, middle, and end.\n"
            "Use very simple language, short sentences, and vocabulary appropriate for 3rd-grade readers.\n"
            "Make sure the story is easy to understand and fun.\n"
            "Add emotions, adventures, and a moral lesson at the end.\n\n"
            "IMAGE DESCRIPTION: {scenario}\n"
            "STORY:\n"
        )
        prompt_template = PromptTemplate(template=template, input_variables=["scenario"])
        story_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)
        
        if vector_store:
            context = retrieve_context(scenario, vector_store)
            prompt_with_context = f"{context}\n\n{scenario}"
        else:
            prompt_with_context = scenario

        formatted_prompt = prompt_template.format(scenario=prompt_with_context)
        generated_story = story_llm.invoke(formatted_prompt)
        story_text = getattr(generated_story, "content", str(generated_story))
        return story_text.strip()

    elif model_choice == "Hugging Face (Alternative)":
        # Use the ChatML prompt format as recommended by the model documentation.
        prompt_text = (
            "<|im_start|>system\n"
            "You are a Helpful Assistant who writes educational stories for young children using very simple language, short sentences, "
            "and vocabulary appropriate for 3rd-grade readers. Make sure the story is very easy to understand and fun.\n"
            "<|im_end|>\n"
            "<|im_start|>user\n"
            f"{scenario}\n"
            "<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        pipeline_instance = get_hf_pipeline()
        generated_text = pipeline_instance(
            prompt_text,
            max_length=800,
            temperature=0.9,
            top_p=0.95,
            do_sample=True
        )[0]['generated_text']
        return generated_text.strip()

    else:
        raise ValueError("Unsupported model choice. Please select a valid model.")