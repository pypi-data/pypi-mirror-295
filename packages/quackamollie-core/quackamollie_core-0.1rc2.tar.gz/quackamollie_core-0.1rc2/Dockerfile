ARG PROXY_REGISTRY=
FROM ${PROXY_REGISTRY}python:3.10-alpine AS base


### Builder ###
FROM base AS builder

RUN mkdir /install
WORKDIR /install

COPY ./dist/* /dist/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-warn-script-location --prefix=/install /dist/*.whl


### Release ###
FROM base

ENV QUACKAMOLLIE_DATA_DIR="/quackamollie/data"
ENV QUACKAMOLLIE_LOG_DIR="/quackamollie/logs"

COPY --from=builder /install /usr/local
RUN mkdir -p "${QUACKAMOLLIE_DATA_DIR}" "${QUACKAMOLLIE_LOG_DIR}"

WORKDIR /quackamollie-core
COPY ./migrations/env.py ./migrations/script.py.mako /quackamollie-core/migrations/
COPY ./migrations/versions/*.py /quackamollie-core/migrations/versions/
COPY alembic.ini /quackamollie-core/
COPY ./scripts/docker/docker-entrypoint.sh /quackamollie-core/

ENTRYPOINT ["/bin/sh", "docker-entrypoint.sh"]
CMD ["quackamollie", "-vv", "serve"]
