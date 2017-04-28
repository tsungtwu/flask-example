# This dockerfile use to dockerize flask application
# VERSION 1
# MAINTAINER tsungtwu jtrmn.wu@gmail.com

FROM python:2.7-onbuild

ARG CONFIG=development
ENV FLASK_CONFIG ${CONFIG}


# RUN mkdir /flask
WORKDIR /flask

# Install lib 
COPY ./requirements.txt ./
COPY ./webapp /flask

RUN pip install -r requirements.txt



ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "-b", "0.0.0.0:5000","run:app"]