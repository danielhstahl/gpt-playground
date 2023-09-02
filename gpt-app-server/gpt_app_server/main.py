from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile
from gpt_app_server.gpt import chat, init_model
from fastapi.staticfiles import StaticFiles
from gpt_app_server.extract_filing_langchain import upload_document
from gpt_app_server.prompt import prompt_generator, base_prompt
from uuid import uuid4

app = FastAPI()


class Question(BaseModel):
    question: str


class Document(BaseModel):
    text: str


class Prompt(BaseModel):
    prompt: str


hold_chat = {}

hold_session_data = {}  # hacky, not secure, but good enough for a demo


@app.on_event("startup")
async def startup_event():
    hold_chat["model"], hold_chat["retriever"] = init_model()


@app.get("/health")
def read_root():
    return {"Hello": "World"}


@app.post("/question")
def ask_question(session_id: str, question: Question):
    result = hold_session_data[session_id](question.question)
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
    upload_document(file.filename, file.file, hold_chat["retriever"])
    return "success"


@app.post("/session")
def create_session(
    prompt: Union[Prompt, None] = None, existing_uid: Union[str, None] = None
):
    if existing_uid not in hold_session_data:
        uid = str(uuid4())
    else:
        uid = existing_uid

    prompt_fn = (
        base_prompt if prompt is None else lambda: prompt_generator(prompt.prompt)
    )
    hold_session_data[uid] = chat(hold_chat["model"], hold_chat["retriever"], prompt_fn)
    return uid


app.mount("/", StaticFiles(directory="../gpt-app/build", html=True), name="static")
