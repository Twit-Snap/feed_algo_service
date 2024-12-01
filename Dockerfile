#
FROM python:3.8-slim

#
WORKDIR /code

#
COPY requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
RUN pip install faiss-cpu

#

COPY newrelic.ini /code/newrelic.ini
COPY app /code/app

#
EXPOSE $PORT

#
CMD if [ "$MODE" = "test" ]; then pytest; else python app/main.py; fi