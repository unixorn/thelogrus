FROM unixorn/debian-py3
USER root

RUN apt-get update && \
  apt-get install -y ca-certificates less vim zsh --no-install-recommends && \
  apt-get install -y python3-pip git

RUN mkdir -p /usr/local/bin && \
  mkdir -p /code && \
  mkdir -p /data

# COPY test/* /usr/local/bin/
COPY dist/*whl /data
RUN pip3 install --no-cache-dir /data/*.whl

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
