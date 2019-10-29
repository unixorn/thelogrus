FROM debian:buster-slim
USER root

RUN apt-get update && \
  apt-get install -y ca-certificates less vim zsh --no-install-recommends && \
  apt-get install -y python3-pip git

RUN pip3 install pylint

RUN mkdir -p /usr/local/bin

COPY pylintrc /etc/pylintrc
COPY test/* /usr/local/bin/

RUN chmod 755 /usr/local/bin/*

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
