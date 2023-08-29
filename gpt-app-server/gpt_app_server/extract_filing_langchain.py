import os
from typing import Optional, List, Callable
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from tempfile import SpooledTemporaryFile
import shutil
from gpt4all import GPT4All
from pathlib import Path

DEFAULT_VECTOR_LOCATION = "./chroma"
DEFAULT_MODEL_LOCATION = "./model"
DEFAULT_FILE_STORAGE = "./filings"
DEFAULT_MODEL_NAME = "orca-mini-3b.ggmlv3.q4_0.bin"
TARGET_SOURCE_CHUNKS = 4


def extract_filings(directory: str) -> List[Document]:
    # instantiate the DirectoryLoader class

    loader = DirectoryLoader(directory)
    loaded_filings = loader.load()
    return loaded_filings


def extract_document(file_path: str) -> List[Document]:
    loader = TextLoader(file_path)
    loaded_filings = loader.load()
    return loaded_filings


def split_documents(
    loaded_filings: List[Document],
    chunk_size: Optional[int] = 500,
    chunk_overlap: Optional[int] = 20,
) -> List[Document]:
    # instantiate the RecursiveCharacterTextSplitter class
    # by providing the chunk_size and chunk_overlap

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Now split the documents into chunks and return
    chunked_docs = splitter.split_documents(loaded_filings)
    return chunked_docs


def convert_document_to_embeddings(
    chunked_docs: List[Document],
    embedder: Callable[[str], List[float]],
    vector_location: str = DEFAULT_VECTOR_LOCATION,
):
    # instantiate the Chroma db python client
    # embedder will be our embedding function that will map our chunked
    # documents to embeddings

    vector_db = Chroma(
        persist_directory=vector_location,
        embedding_function=embedder,
        # client_settings=CHROMA_SETTINGS,
    )

    # now once instantiated we tell our db to inject the chunks
    # and save all inside the db directory
    vector_db.add_documents(chunked_docs)
    vector_db.persist()

    # finally return the vector db client object
    return vector_db


def return_retriever_from_persistant_vector_db(
    embedder: Callable[[str], List[float]],
    vector_location: str = DEFAULT_VECTOR_LOCATION,
):
    # first check whether the database is created or not
    # if not then throw error
    # because if the database is not instantiated then
    # we can not get the retriever

    if not os.path.isdir(vector_location):
        raise NotADirectoryError("Please load your vector database first.")

    vector_db = Chroma(
        persist_directory=vector_location,
        embedding_function=embedder,
        # client_settings=CHROMA_SETTINGS,
    )

    # used the returned embedding function to provide the retriver object
    # with number of relevant chunks to return will be = 4
    # based on the one we set inside our settings

    return vector_db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})


def extract_embeddings(
    location_of_filings: str = DEFAULT_FILE_STORAGE,
):
    chunked_documents = split_documents(
        loaded_filings=extract_filings(location_of_filings)
    )

    print("=> loading and chunking done.")

    embeddings = GPT4AllEmbeddings()
    vector_db = convert_document_to_embeddings(
        chunked_docs=chunked_documents, embedder=embeddings
    )
    print("=> vector db initialised and created.")
    print("All done")


def download_gpt_model(
    model_name: str = DEFAULT_MODEL_NAME,
    location_of_model: str = DEFAULT_MODEL_LOCATION,
):
    folder = Path(location_of_model)
    folder.mkdir(parents=True, exist_ok=True)  # create the folder if it doesnt exist
    model = GPT4All(model_name, model_path=location_of_model)


def upload_document(
    file_name: str, file: SpooledTemporaryFile, directory: str = DEFAULT_FILE_STORAGE
):
    file_location = os.path.join(directory, file_name)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file, file_object)
    chunked_documents = split_documents(loaded_filings=extract_document(file_location))
    embeddings = GPT4AllEmbeddings()
    vector_db = convert_document_to_embeddings(
        chunked_docs=chunked_documents, embedder=embeddings
    )
    print("=> vector db initialised and updated.")
    print("Finished processing document")


if __name__ == "__main__":
    extract_embeddings()
    download_gpt_model()
