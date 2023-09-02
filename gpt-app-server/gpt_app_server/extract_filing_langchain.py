import os
from typing import Optional, List, Callable
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from tempfile import SpooledTemporaryFile
import shutil
from html2text import html2text

DEFAULT_VECTOR_LOCATION = "./chroma"
DEFAULT_FILE_STORAGE = "./filings"
TARGET_SOURCE_CHUNKS = 4


# only used for bulk loading; not through the UI/app
def extract_filings(directory: str) -> List[Document]:
    # instantiate the DirectoryLoader class

    loader = DirectoryLoader(directory)
    loaded_filings = loader.load()
    return loaded_filings


# extract individual document, used by the UI/app when uploading file
def extract_document(file_path: str) -> List[Document]:
    loader = TextLoader(file_path)
    loaded_filings = loader.load()
    return loaded_filings


# https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter
def split_documents(
    loaded_filings: List[Document],
    chunk_size: Optional[int] = 1000,
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


def convert_document_to_embeddings(chunked_docs: List[Document], vector_db: Chroma):
    # this will automatically persist once close of app
    vector_db.add_documents(chunked_docs)


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
    )

    # used the returned embedding function to provide the retriver object
    # with number of relevant chunks to return will be = 4
    # based on the one we set inside our settings

    return vector_db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})


# only used for bulk loading; not through the UI/app
def extract_embeddings(
    location_of_filings: str = DEFAULT_FILE_STORAGE,
    vector_location: str = DEFAULT_VECTOR_LOCATION,
):
    chunked_documents = split_documents(
        loaded_filings=extract_filings(location_of_filings)
    )

    print("=> loading and chunking done.")

    embeddings = GPT4AllEmbeddings()
    vector_db = Chroma(
        persist_directory=vector_location,
        embedding_function=embeddings,
    )

    convert_document_to_embeddings(
        chunked_documents,
        vector_db,
    )
    print("=> vector db initialised and created.")
    print("All done")


def upload_document(
    file_name: str,
    file: SpooledTemporaryFile,
    vector_db: Chroma,
    directory: str = DEFAULT_FILE_STORAGE,
):
    file_location = os.path.join(directory, file_name)
    with open(file_location, "wb+") as file_object:  # write the basic values
        shutil.copyfileobj(file, file_object)
    with open(file_location, "r") as file_object:  # read and remove html tags
        text_without_html_tags = html2text(file_object.read())
    with open(
        file_location, "w"
    ) as file_object:  # will overwrite file; write non-html back
        file_object.write(text_without_html_tags)
    chunked_documents = split_documents(loaded_filings=extract_document(file_location))
    vector_db = convert_document_to_embeddings(chunked_documents, vector_db)
    print("=> vector db updated.")
    print("Finished processing document")


if __name__ == "__main__":
    extract_embeddings()
