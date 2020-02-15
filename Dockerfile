FROM python:3.7

ENV PYTHONNINBUFFERED 1

# Create and set working directory for our source code
RUN mkdir /backend -p -v
WORKDIR /backend
COPY . .

RUN chmod +x entrypoint.sh

# Install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["/backend/entrypoint.sh"]