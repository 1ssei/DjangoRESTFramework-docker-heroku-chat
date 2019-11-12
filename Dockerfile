FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
ADD requirements.txt /api
COPY ./api/ .
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:$PORT api.wsgi
