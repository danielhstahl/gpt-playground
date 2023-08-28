from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from gpt_app_server.gpt import chat
from gpt_app_server.extract_filing_embeddings import upload_document
from typing_extensions import Annotated

app = FastAPI()


class Question(BaseModel):
    question: str


class Document(BaseModel):
    text: str


hold_chat = {}


@app.on_event("startup")
async def startup_event():
    hold_chat["chat"] = chat()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/question")
def ask_question(question: Question):
    result = hold_chat["chat"](question.question)
    answer, docs = result["result"], result["source_documents"]
    return {
        "answer": answer,
        "sources": [
            {"filename": doc.metadata["source"], "content": doc.page_content}
            for doc in docs
        ],
    }


@app.post("/question")
def submit_new_document(document: Document):
    result = hold_chat["chat"](document.text)
    answer, docs = result["result"], result["source_documents"]
    return {
        "answer": answer,
        "sources": [
            {"filename": doc.metadata["source"], "content": doc.page_content}
            for doc in docs
        ],
    }


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    upload_document(file.filename, file.file)
    return "success"
