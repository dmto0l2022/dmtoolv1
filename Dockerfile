
#ARG BUILD_ENV_MARIADB_DATABASE
#ENV ENV_USERNAME=$BUILD_ENV_USERNAME

#TWINE_USERNAME - the username to use for authentication to the repository.
#TWINE_PASSWORD - the password to use for authentication to the repository.
#TWINE_REPOSITORY - the repository configuration, either defined as a section in .pypirc or provided as a full URL.
#TWINE_REPOSITORY_URL - the repository URL to use.
#TWINE_CERT - custom CA certificate to use for repositories with self-signed or untrusted certificates.
#TWINE_NON_INTERACTIVE - Do not interactively prompt for username/password if the required credentials are missing.

ARG BUILD_TWINE_USERNAME
ENV TWINE_USERNAME=$BUILD_ENV_USERNAME

ARG BUILD_TWINE_PASSWORD
ENV TWINE_PASSWORD=$BUILD_TWINE_PASSWORD

ARG BUILD_TWINE_REPOSITORY
ENV TWINE_REPOSITORY=$BUILD_TWINE_REPOSITORY

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

COPY dmtool/ /workdir/dmtool/

RUN chown -R $USER_UID:$USER_GID /workdir/dmtool/

RUN ls -la /workdir/dmtool/*

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

COPY ./requirements.txt /env/requirements.txt
RUN /env/bin/python3 -m pip install --upgrade build
WORKDIR /workdir/dmtool/
RUN /env/bin/python3 -m build
RUN ls -la /workdir/dmtool/dist/*

RUN /env/bin/python3 -m pip install --upgrade twine
RUN /env/bin/python3 -m twine upload --repository testpypi dist/*

