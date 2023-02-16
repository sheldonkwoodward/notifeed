FROM python:3.11.1-alpine3.17
ENV DOCKER_CONTAINER=1
RUN pip install pipenv
RUN adduser -S notifeed
WORKDIR /home/notifeed
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy
COPY schemas schemas
ENV CONFIG_SCHEMA_FILE=schemas/config.json.schema
COPY notifeed notifeed
USER notifeed
CMD ["python", "-m", "notifeed"]
