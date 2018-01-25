FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/code/proj2004
ENV DJANGO_SETTINGS_MODULE proj2004.settings.deploy
RUN mkdir -p /opt/code
WORKDIR /opt/code
ADD requirements*.txt /opt/code/
RUN pip install -r requirements-deploy.txt
ADD . /opt/code/
RUN mkdir -p /var/www
RUN proj2004/manage.py collectstatic --noinput
RUN mkdir -p /var/www/media
VOLUME /var/www
