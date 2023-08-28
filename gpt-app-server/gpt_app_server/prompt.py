from langchain.prompts import PromptTemplate


def base_prompt():
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    """
    return PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
