FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/local.txt /code/
ADD requirements/base.txt /code/
RUN pip install -r local.txt
ADD . /code/
CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8000
