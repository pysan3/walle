FROM python:3.8 as poetry

RUN apt-get update && apt-get install --no-install-recommends -y \
        default-libmysqlclient-dev inotify-tools tree protobuf-compiler \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /www

ENV PYTHONUNBUFFERED 1

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY command.sh edit.py .env ./
COPY alembic.ini ./
COPY protobuf/ ./protobuf/
COPY app/ ./app/
COPY utils/ ./utils/
COPY migration/ ./migration/
COPY src/ ./src/

RUN ./command.sh --protoc -i

# RUN python manage.py -d init -y
RUN alembic upgrade head

FROM node as vue

WORKDIR /www

ENV NODE_OPTIONS --openssl-legacy-provider

COPY package.json package-lock.json ./
RUN npm install

COPY *.js *.json .eslint* .prettier* ./
COPY --from=poetry /www/src/ ./src/
COPY public/ ./public/

RUN ls -la

RUN npm run build

RUN ls ./

FROM poetry as final
WORKDIR /www

COPY --from=vue /www/static/ ./static/
COPY --from=poetry /www/protobuf/ ./protobuf/
COPY app/ ./app/
RUN true
COPY . .

EXPOSE 5042

CMD gunicorn \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:5042 \
    --access-logfile - \
    --error-logfile - \
    run:api
