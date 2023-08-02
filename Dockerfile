ARG PYTHON_VERSION=3.10.5-alpine

FROM python:${PYTHON_VERSION} as base-image

RUN \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    pip install pipenv

FROM base-image as compile-image

ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1

COPY Pipfile Pipfile.lock /

RUN \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pipenv install --python 3.10 --skip-lock && \
    apk --purge del .build-deps

FROM base-image as runtime

ENV PYTHONUNBUFFERED 1

COPY --from=compile-image /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . /app/

RUN \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
