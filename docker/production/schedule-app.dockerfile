#FROM python:3.11.9-alpine
FROM python:3.12
# ENV TZ="Europe/Moscow"

# set work directory
WORKDIR /app

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
# RUN apt-get install -y netcat
RUN apt-get update && apt-get install -y netcat-traditional

## install psycopg2 dependencies
#RUN apt install postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml .
RUN poetry install

#RUN apt install -y netcat

# copy entrypoint.sh
#COPY ./app/docker/entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/r2-en-bot-app/entrypoint.sh
#RUN chmod +x /usr/src/r2-en-bot-app/entrypoint.sh

# copy app
COPY . .
#COPY main.py .

# RUN alembic upgrade d2f971e1de0e

# run entrypoint.sh
#ENTRYPOINT ["python3", "main.py"]
#ENTRYPOINT ["ping", "8.8.8.8", "-t"]
#ENTRYPOINT ["ls", "-lah"]

# RUN echo "Europe/Stockholm" > /etc/timezone

ENTRYPOINT ["/app/entrypoint_schedule.sh"]