FROM debian:buster-slim
USER root

RUN apt-get update && \
  apt-get install -y ca-certificates --no-install-recommends && \
  apt-get install -y zsh python3-pip

RUN mkdir -p /usr/local/bin

COPY test/* /usr/local/bin/

RUN chmod 755 /usr/local/bin/*

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
