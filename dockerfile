FROM python:3.12.0

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install prompt_toolkit

COPY ./src/ /app/

CMD ["python", "adress_book_abstract.py"]