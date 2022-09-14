FROM python:3.8

WORKDIR /app

COPY ./ ./

EXPOSE 8080

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
