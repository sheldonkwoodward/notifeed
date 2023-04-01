FROM python:3.11.1-alpine3.17
ENV DOCKER_CONTAINER=1
RUN pip install pipenv
ARG UNAME=notifeed
ARG GNAME=notifeed
ARG UID=1000
ARG GID=1000
RUN addgroup -g $GID -S $GNAME
RUN adduser -u $UID -S $UNAME -G $GNAME
WORKDIR /home/$UNAME
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy
COPY schemas schemas
ENV CONFIG_SCHEMA_FILE=schemas/config.json.schema
COPY notifeed notifeed
USER $UNAME
CMD ["python", "-m", "notifeed"]
