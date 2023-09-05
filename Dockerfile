# pull official base image
FROM python:3.11.4-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get -y install vim unzip curl netcat gcc && apt-get clean


WORKDIR /workdir/dmtoolv1

#WORKDIR /app

ARG USERNAME=agaitske
ARG USER_UID=1001
ARG USER_GID=1002 ## dm group

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME


#RUN chmod g+s /app

RUN mkdir /env
RUN chown $USER_UID:$USER_GID /env
RUN chmod g+s /env

#COPY app/ /app/

#RUN chown -R $USER_UID:$USER_GID /app

#RUN ls -la /app/*

USER $USERNAME

ENV VIRTUAL_ENV=/env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN /env/bin/python3 -m pip install --upgrade pip
RUN . /env/bin/activate
RUN /env/bin/python3 --version
RUN whereis python3
RUN whereis pip3

COPY ./requirements.txt /env/requirements.txt
RUN /env/bin/pip3 install -r /env/requirements.txt
RUN /env/bin/pip3 freeze

RUN /env/bin/python3 -m pip install --upgrade build
WORKDIR /workdir/dmtoolv1/dmtool/
RUN /env/bin/python3 -m build
RUN ls -la /workdir/dmtoolv1/dist/*


