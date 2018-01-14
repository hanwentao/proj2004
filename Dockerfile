FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/code
WORKDIR /opt/code
ADD requirements.txt /opt/code/
RUN pip install -r requirements.txt
ADD . /opt/code/
