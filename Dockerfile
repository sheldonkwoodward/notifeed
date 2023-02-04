FROM python:3.11.1-alpine3.17
RUN pip install pipenv
RUN adduser -S rss
WORKDIR /home/rss
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY rss_notify.py rss_notify.py
RUN pipenv install --system --deploy
ENV DOCKER_CONTAINER=1
USER rss
CMD ["python", "/home/rss/rss_notify.py"]
