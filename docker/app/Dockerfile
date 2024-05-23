#FROM python:3.11.9-alpine
FROM python:3.12

# set work directory
WORKDIR /app

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

#RUN apt-get update && apt-get install -y \
#    python3.11 \
#    python3-pip

# install psycopg2 dependencies
# RUN apt install postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
RUN poetry install

# copy entrypoint.sh
#COPY ./app/docker/entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/r2-en-bot-app/entrypoint.sh
#RUN chmod +x /usr/src/r2-en-bot-app/entrypoint.sh

# copy project
#COPY .env .
#COPY main.py .

# run entrypoint.sh
ENTRYPOINT ["python3", "main.py"]