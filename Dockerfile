FROM python:3.9.0a3-alpine3.10

ENV PYTHONNINBUFFERED 1

# Create and set working directory for our source code
RUN mkdir /backend -p -v
WORKDIR /backend
COPY . .

RUN chmod +x ./wait-for

# For psycopg2 pip package
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install requirements
RUN pip3 install -r requirements.txt
