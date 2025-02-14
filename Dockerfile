FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y clang clangd mingw-w64 python3-pip \
    && pip3 install flask --break-system-packages \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/* /app/

EXPOSE 4444
ENTRYPOINT [ "python3", "app.py"]
