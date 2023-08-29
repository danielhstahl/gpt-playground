FROM node:20-alpine3.17
WORKDIR /src
ADD gpt-app /src/
WORKDIR /src/gpt-app 
RUN npm ci 
RUN npm run build

FROM python:3.10-bookworm
WORKDIR /server
ADD gpt-app-server /server/
WORKDIR /server/gpt-app-server 
RUN pip install "poetry==1.6.1"
RUN poetry install
RUN poetry run python gpt_app_server/download_filings.py
RUN poetry run python gpt_app_server/extract_filing_langchain.py
COPY --from=0 /src/gpt-app/build /server/gpt-app/

CMD ["poetry", "run", "uvicorn", "gpt_app_server.main:app"]