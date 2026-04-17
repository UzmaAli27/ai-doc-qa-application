def generate_answer(question, context):

    # safety check
    if not context or len(context.strip()) == 0:
        return "No relevant information found in the document."

    # 🔥 Proper prompt (USED INSIDE FUNCTION)
    prompt = f"""
You are an expert report analysis assistant.

Rules:
- Write COMPLETE answers (never cut sentences)
- Do NOT stop mid-sentence
- Do NOT repeat context
- Do NOT show Q/A format
- Organize answer with proper structure if needed

If the context is incomplete, still try to reconstruct meaning.

Context:
{context}

Question:
{question}

Answer:
"""


# -------------------------------
# Dummy placeholder (YOU MUST replace this)
# -------------------------------
def call_llm(prompt: str):
    """
    Replace this with:
    - OpenAI API call OR
    - HuggingFace model OR
    - your local LLM
    """

    # TEMP fallback (so code doesn't break)
    return "LLM not connected. Please integrate model in call_llm()."