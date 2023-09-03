ARG PYTHON_MINOR_VERSION=3.10
FROM node:20-alpine3.17
WORKDIR /ui
COPY gpt-app /ui/gpt-app
WORKDIR /ui/gpt-app 
RUN npm ci 
RUN npm run build

FROM python:${PYTHON_MINOR_VERSION}-bullseye
ARG PYTHON_MINOR_VERSION
RUN apt-get update && apt-get install -y software-properties-common cmake sqlite3
WORKDIR /server
RUN mkdir gpt-app
COPY gpt-app-server /server/gpt-app-server
WORKDIR /server/gpt-app-server
# or useradd?
RUN adduser user1 
RUN chown -R user1: /server
RUN chmod 755 /server
USER user1
RUN python3 -m pip install "poetry==1.6.1"
RUN $HOME/.local/bin/poetry install
# build c backend
RUN git clone --recurse-submodules https://github.com/nomic-ai/gpt4all.git
RUN cd gpt4all && git reset d55cbbee3280ffbbe7570aae0ac2aad3994e7711 --hard 
RUN cd gpt4all/gpt4all-backend/ && mkdir build && cd build && cmake .. && cmake --build . --parallel --config Release
RUN cp -a /server/gpt-app-server/gpt4all/gpt4all-backend/build/. $($HOME/.local/bin/poetry run python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')/gpt4all/llmodel_DO_NOT_MODIFY/build/
RUN rm -rf gpt4all
RUN mkdir chroma && mkdir filings && mkdir model
RUN $HOME/.local/bin/poetry run python gpt_app_server/download_llm.py
COPY --from=0 /ui/gpt-app/build /server/gpt-app/build

CMD ["sh", "-c", "$HOME/.local/bin/poetry run uvicorn --host 0.0.0.0 gpt_app_server.main:app"]