FROM python:alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src src

ENTRYPOINT ["python", "src/Processor.py"]
