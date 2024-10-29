# syntax=docker/dockerfile:1.4
# Enable here-documents:
# https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md#here-documents
FROM python:3.12.1 AS python

RUN set -x && \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --yes \
    supervisor

WORKDIR /app

# Only reinstall pip requirements when the file changes.
COPY requirements/base.txt requirements/base.txt
RUN pip install --requirement requirements/base.txt

COPY . .

RUN cat <<'EOF' > /etc/supervisor/conf.d/supervisord.conf
[supervisord]
logfile=/dev/null
logfile_maxbytes=0
loglevel=debug
pidfile=/tmp/supervisord.pid
nodaemon=true
user=root

[unix_http_server]
file=/var/run/supervisor.sock

[program:example]
directory=/app
command=gunicorn
  --bind 0.0.0.0:8000
  --capture-output
  --log-file -
  --log-level debug
  example.wsgi:application
redirect_stderr=true
stdout_logfile=/dev/null
stdout_logfile_maxbytes=0
autorestart=true
EOF

ENTRYPOINT [ "/app/scripts/docker_entrypoint" ]
