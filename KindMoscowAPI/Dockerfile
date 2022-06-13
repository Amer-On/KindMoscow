FROM python:3.8-alpine


WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 


COPY ./src /code/src

CMD ["uvicorn", "src.sendler:app", "--host", "0.0.0.0", "--port", "80"]