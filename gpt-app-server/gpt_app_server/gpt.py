from langchain.chains import RetrievalQA
from langchain.embeddings import GPT4AllEmbeddings
from gpt_app_server.extract_filing_langchain import (
    return_retriever_from_persistant_vector_db,
)
from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.vectorstores.base import VectorStoreRetriever
import os
from gpt_app_server.prompt import base_prompt
from typing import Callable, Tuple
from gpt_app_server.download_llm import DEFAULT_MODEL_LOCATION, DEFAULT_MODEL_NAME


def init_model(
    model_name: str = DEFAULT_MODEL_NAME,
    location_of_model: str = DEFAULT_MODEL_LOCATION,
) -> Tuple[GPT4All, VectorStoreRetriever]:
    model = os.path.join(location_of_model, model_name)
    embeddings = GPT4AllEmbeddings()
    return GPT4All(model=model), return_retriever_from_persistant_vector_db(embeddings)


def chat(
    llm,
    retriever: VectorStoreRetriever,
    prompt: Callable[[], PromptTemplate] = base_prompt,
):
    # embeddings = GPT4AllEmbeddings()
    # retriever = return_retriever_from_persistant_vector_db(embeddings)
    chain_type_kwargs = {"prompt": prompt()}
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )
    return qa_chain


if __name__ == "__main__":
    llm, retriever = init_model()
    chat_inst = chat(llm, retriever)
    while True:
        query = input("What's on your mind: ")
        if query == "exit":
            break
        result = chat_inst(query)
        answer, docs = result["result"], result["source_documents"]

        print(answer)

        print("#" * 30, "Sources", "#" * 30)
        for document in docs:
            print("\n> SOURCE: " + document.metadata["source"] + ":")
            print(document.page_content)
        print("#" * 30, "Sources", "#" * 30)
