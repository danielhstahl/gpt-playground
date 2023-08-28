import chromadb
import os
from gpt4all import Embed4All
from tempfile import SpooledTemporaryFile
import shutil

chroma_client = chromadb.PersistentClient(path="./chroma")
collection = chroma_client.get_or_create_collection(name="filings")

# use gpt4all embedding
embedder = Embed4All()

DEFAULT_FILE_STORAGE = "./filings"


def extract_text(directory: str = DEFAULT_FILE_STORAGE):
    for filename in os.scandir(directory):
        if filename.is_file():
            add_file_to_collection(filename.path)


def add_file_to_collection(file_path: str):
    f = open(file_path, "r")
    text = f.read()
    output = embedder.embed(text)
    collection.add(
        embeddings=output,
        documents=text,
        metadatas={"source": file_path},
        ids=file_path,
    )


def upload_document(
    file_name: str, file: SpooledTemporaryFile, directory: str = DEFAULT_FILE_STORAGE
):
    file_location = os.path.join(directory, file_name)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file, file_object)
    add_file_to_collection(file_location)
