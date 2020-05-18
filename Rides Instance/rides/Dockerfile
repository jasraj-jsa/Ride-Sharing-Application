FROM python:3.7-slim-stretch
RUN mkdir -p /code
COPY . /code
ENV TEAM_NAME="CC_0085_0133_0171_0289"
WORKDIR /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install -r requirements.txt