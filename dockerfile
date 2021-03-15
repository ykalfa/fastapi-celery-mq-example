FROM python:3.8.3-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /application
COPY poetry.lock pyproject.toml /application/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY app.py /application/app.py
COPY worker.py /application/worker.py