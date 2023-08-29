from langchain.prompts import PromptTemplate


def base_prompt():
    prompt_template = """Answer the question from the following context.
        
        {context}
        
        Question: {question}
    """
    return prompt_generator(prompt_template)


def prompt_generator(template: str) -> PromptTemplate:
    return PromptTemplate(template=template, input_variables=["context", "question"])
