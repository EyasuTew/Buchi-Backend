#FROM python:3.10-slim AS base
#RUN apt-get update \
#    && apt-get upgrade -y \
#    && apt-get install -y --no-install-recommends curl git build-essential \
#    && apt-get autoremove -y
#ENV POETRY_HOME="/opt/poetry"
#RUN curl -sSL https://install.python-poetry.org | python3 -
#
#FROM base AS install
#WORKDIR /home/code
#
## allow controlling the poetry installation of dependencies via external args
#ARG INSTALL_ARGS="--no-root --only main"
#ENV POETRY_HOME="/opt/poetry"
#ENV PATH="$POETRY_HOME/bin:$PATH"
#COPY pyproject.toml poetry.lock ./
#
## install without virtualenv, since we are inside a container
#RUN poetry config virtualenvs.create false \
#    && poetry install $INSTALL_ARGS
#
## cleanup
#RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
#RUN apt-get purge -y curl git build-essential \
#    && apt-get clean -y \
#    && rm -rf /root/.cache \
#    && rm -rf /var/apt/lists/* \
#    && rm -rf /var/cache/apt/*
#
#FROM install as app-image
#
#COPY app app
#COPY tests tests
#COPY .env ./
#
## create a non-root user and switch to it, for security.
#RUN addgroup --system --gid 1001 "buchi-eleven"
#RUN adduser --system --uid 1001 "buchi-eleven"
#USER "buchi-eleven"

#
FROM python:3.11.5

#
WORKDIR /app

#
#COPY ./requirements.txt /app/requirements.txt
COPY . /app

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000
#
#COPY . /app

RUN #chmod +x /app
#CMD ["RUN", "chmod +x", "./app"].....  "--host", "0.0.0.0",
#
#CMD ["gunicorn", "-b", "0.0.0.0:8000","app.main:app", "-w", "6", "-k", "uvicorn.workers.UvicornWorker"]
CMD ["uvicorn", "app.main:app","--host", "0.0.0.0","--port", "8000"]
#ENTRYPOINT ["uvicorn app.main:app", "--host 0.0.0.0", "--port 8000"]
#exec uvicorn app.main:app --host 0.0.0.0 --port 8080"]