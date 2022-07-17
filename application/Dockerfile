FROM python:3.10.4 AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


FROM base AS deps-stage
# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt 

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry export -f requirements.txt --without-hashes -o requirements.txt --dev ; else poetry export -f requirements.txt --without-hashes -o requirements.txt ; fi"

# Allow installing debug dependencies to debug in vscode
ARG INSTALL_DEBUG=false
RUN bash -c "if [ $INSTALL_DEBUG == 'true' ] ; then poetry export -f requirements.txt --without-hashes -o requirements.txt --dev --extras debug ; fi"

FROM python:3.10.4-slim AS build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=deps-stage /requirements.txt /requirements.txt
RUN pip install --no-cache --upgrade -r requirements.txt


FROM python:3.10.4-slim AS prod

#  Install curl for healthchecks
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    curl

# Copy environment from build
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Include application scripts
WORKDIR /application
COPY ./start.sh ./start.sh
RUN chmod +x ./start.sh
COPY ./start-reload.sh ./start-reload.sh
RUN chmod +x ./start-reload.sh
COPY ./start-debug.sh ./start-debug.sh
RUN chmod +x ./start-debug.sh

# Copy application code
COPY ./code code
COPY ./docs docs
COPY ./static static
ENV PYTHONPATH=/application/code

EXPOSE 80
CMD ["./start.sh"]