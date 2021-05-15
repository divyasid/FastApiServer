FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./blog /app
COPY ./requirements.txt /app


RUN pip3 install -r requirements.txt

CMD ["uvicorn", "blog.main:app", "--host=0.0.0.0", "--reload"]

