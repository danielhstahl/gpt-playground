ARG PYTHON_MINOR_VERSION=3.10
FROM node:20-alpine3.17
WORKDIR /ui
COPY gpt-app /ui/gpt-app
WORKDIR /ui/gpt-app 
RUN npm ci 
RUN npm run build

#FROM ghcr.io/abetlen/llama-cpp-python:latest@sha256:cb8e231c02242df745a3f68b18aff054aaa152ee7afdeac2f65d7ad5e203910f
#RUN make build
FROM python:${PYTHON_MINOR_VERSION}-bullseye
ARG PYTHON_MINOR_VERSION
RUN apt-get update && apt-get install -y software-properties-common cmake sqlite3

# need new version of sqlite
#RUN curl https://www.sqlite.org/2023/sqlite-autoconf-3430000.tar.gz -o sqlite.tar.gz \
#    && tar xvfz sqlite.tar.gz \
#    && cd sqlite-autoconf-3430000 \
#    && ./configure && make sqlite3.c

WORKDIR /server
RUN mkdir gpt-app
COPY gpt-app-server /server/gpt-app-server
WORKDIR /server/gpt-app-server
#USER 1001
RUN python3 -m pip install "poetry==1.6.1"
RUN poetry install
# build c backend
#RUN apt-get update && apt-get install -y git
RUN git clone --recurse-submodules https://github.com/nomic-ai/gpt4all.git
RUN cd gpt4all && git reset d55cbbee3280ffbbe7570aae0ac2aad3994e7711 --hard 
RUN cd gpt4all/gpt4all-backend/ && mkdir build && cd build && cmake .. && cmake --build . --parallel --config Release
#RUN cp -a /app/llama_cpp/. /server/gpt-app-server/.venv/lib/python3.11/site-packages/gpt4all/llmodel_DO_NOT_MODIFY/build/
RUN cp -a /server/gpt-app-server/gpt4all/gpt4all-backend/build/. /server/gpt-app-server/.venv/lib/python${PYTHON_MINOR_VERSION}/site-packages/gpt4all/llmodel_DO_NOT_MODIFY/build/
RUN rm -rf gpt4all
RUN poetry run python gpt_app_server/download_filings.py
RUN poetry run python gpt_app_server/extract_filing_langchain.py
COPY --from=0 /ui/gpt-app/build /server/gpt-app/build

CMD ["poetry", "run", "uvicorn", "gpt_app_server.main:app"]


#CMD []


#docker run -v $PWD/gpt_app_server/model:/models -ti --entrypoint /bin/bash quay.io/go-skynet/local-ai:v1.25.0 --models-path /models 

#docker run -v $PWD/gpt_app_server/model:/models -ti --entrypoint /bin/bash quay.io/go-skynet/local-ai:v1.25.0 

#docker run -it --entrypoint /bin/bash ghcr.io/ggerganov/llama.cpp:light 

# docker run -it --entrypoint /bin/sh ghcr.io/abetlen/llama-cpp-python:latest