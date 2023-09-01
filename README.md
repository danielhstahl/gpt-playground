## use gpt4all to save money

`cd gpt_app_server`

`poetry run python gpt_app_server/download_filings.py`

`poetry run python gpt_app_server/extract_filing_langchain.py`

Not needed, but cool to explore: `poetry run python gpt_app_server/gpt.py`

`poetry run uvicorn gpt_app_server.main:app --reload`

`curl -X POST http://127.0.0.1:8000/question -d '{"question": "what was the loan loss allowance in March 2022 for Regions"}' -H 'Content-Type: application/json'`