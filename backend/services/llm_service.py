def generate_answer(query, results):

    print("LLM received query:", query)
    print("LLM received results count:", len(results))

    combined_text = ""

    for r in results[:5]:

        combined_text += r["content"] + " "

    if combined_text.strip() == "":

        return "LLM received empty content."

    return combined_text[:500]