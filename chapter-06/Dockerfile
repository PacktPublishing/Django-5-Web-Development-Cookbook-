FROM python:3.12-slim-bookworm as build

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# Copy the poetry lock file and the pyproject file
COPY ./poetry.lock pyproject.toml /app/

# install peetry and native dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential \
    && pip install --upgrade pip \
    && pip install poetry \
    && poetry env info

ARG INSTALL_DEV=false
RUN echo "Install development dependencies: ${INSTALL_DEV}"

RUN if [ "${INSTALL_DEV}" = "true" ]; then poetry  export -o requirements.txt --dev --without-hashes ; else  poetry export -o requirements.txt --without-hashes;  fi

RUN pip wheel --wheel-dir /app/wheels -r requirements.txt

RUN pip install -r requirements.txt 

# Copy the rest of the application files
COPY conduit /app

FROM python:3.12-slim-bookworm

RUN useradd -ms /bin/bash appuser

WORKDIR /app

COPY --from=build /app/wheels /wheels/
COPY --from=build --chown=appuser:appuser /app /app

RUN pip install --no-cache-dir --no-index --find-links=/wheels/* /wheels/*

EXPOSE 8000

# Set environment variable for the application
ENV HOST 0.0.0.0
ENV PORT 8000

# Run the application using gunicorn using uvicorn worker
# CMD ["gunicorn", "conduit.asgi:application", "--bind", "${HOST}:${PORT}", "--worker-class", "uvicorn.workers.UvicornWorker"]

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]  

LABEL maintainer="Bogdan Veliscu" \
    version="1.0" \
    description="Django Application with Poetry and Slim image"