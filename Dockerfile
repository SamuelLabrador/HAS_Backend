FROM python:3.7
ENV PYTHONNINBUFFERED 1

# Create and set working directory for our source code
RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/