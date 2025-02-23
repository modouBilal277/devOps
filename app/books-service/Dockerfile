FROM python:3.10.8

WORKDIR "/code"

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./books_service.py /code/books_service.py
COPY ./models.py /code/models.py
COPY ./docs.py /code/docs.py

ENV MONGO_HOST 172.17.0.2

CMD ["uvicorn", "books_service:app", "--host", "0.0.0.0", "--port", "80"]

