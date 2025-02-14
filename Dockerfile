FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY src/* /app/

RUN apt update \
    && apt install -y clang clangd mingw-w64 python3-pip \
    && pip3 install flask --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 4444
ENTRYPOINT [ "python3", "app.py"]