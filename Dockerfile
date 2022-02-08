FROM unixorn/debian-py3

RUN mkdir -p /usr/local/bin && \
  mkdir -p /code && \
  mkdir -p /data

# COPY test/* /usr/local/bin/
COPY dist/*whl /data
RUN pip3 install --no-cache-dir /data/*.whl

ENTRYPOINT ["/usr/local/bin/docker-entrypoint"]
