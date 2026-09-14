FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY docker/entrypoint.sh ./docker/entrypoint.sh
# Collect public assets without injecting deployment secrets into the build.
RUN python backend/manage.py collectstatic --noinput --settings=msu_qvs.settings \
    && useradd --uid 10001 --create-home qvs \
    && mkdir -p /app/backend/media \
    && chown -R qvs:qvs /app/backend/media \
    && chmod +x /app/docker/entrypoint.sh

ARG APP_REVISION=unknown
ENV APP_REVISION=${APP_REVISION} DJANGO_SETTINGS_MODULE=msu_qvs.production
LABEL org.opencontainers.image.revision=${APP_REVISION}
USER qvs
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=60s --retries=6 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health/ready/', timeout=3)"
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "--chdir", "backend", "msu_qvs.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
