from langchain_huggingface import HuggingFaceEmbeddings
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Language Model
# --------------------------------------------------

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)


# --------------------------------------------------
# Generate Answer
# --------------------------------------------------

def generate_answer(prompt):
    """
    Generate an answer using Qwen.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a medicine information assistant. "
                "Use only the information provided in "
                "the context. "
                "Do not invent medical information. "
                "Do not diagnose or prescribe."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer