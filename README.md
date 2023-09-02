## Gpt4all, chroma for vector database, langchain for ease of use

### Setup by downloading from SEC website.  

First, you need to get an API key from the SEC website and put it in a `.env` file within the `gpt_app_server` directory.

`cd gpt_app_server`

`poetry run python gpt_app_server/download_filings.py`

`poetry run python gpt_app_server/extract_filing_langchain.py`

`poetry run python gpt_app_server/download_llm.py`

Not needed, but cool to explore: `poetry run python gpt_app_server/gpt.py`

`poetry run uvicorn gpt_app_server.main:app --reload`

`curl -X POST http://127.0.0.1:8000/question -d '{"question": "what was the loan loss allowance in March 2022 for Regions"}' -H 'Content-Type: application/json'`

## Goals
* Enhance an LLM with relevant documents and retrieve information embedded within those documents
* Allow for chat history within session
* Allow for prompt creation and selection of different prompts
* Do all this with a simple UI

## Limitations

* Currently does not use chat history; can be made to do so by updating the chain_type_kwargs in [gpt.py](gpt-app-server/gpt.py).  

## Docker

`docker build . -t gpt-app`
`docker run -p 8000:8000 gpt-app`
