FROM python:3
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/code \
    DJANGO_SETTINGS_MODULE=proj2004.settings.deploy
RUN mkdir -p /opt/code /var/www/media
WORKDIR /opt/code
ADD requirements*.txt ./
RUN pip install -r requirements-deploy.txt
ADD . .
RUN ./manage.py collectstatic --noinput
VOLUME /var/www
CMD ["uwsgi", "uwsgi.ini"]
