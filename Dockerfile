FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./blog /app
COPY ./requirements.txt /app

WORKDIR /
RUN pip3 install -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

