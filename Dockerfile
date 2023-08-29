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
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --no-root
COPY --from=0 /src/gpt-app/build /server/gpt-app/

CMD [poetry, run, uvicorn, gpt_app_server.main:app]