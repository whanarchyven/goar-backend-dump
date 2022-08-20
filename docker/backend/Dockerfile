# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers make cmake
RUN apk add --no-cache libffi-dev openssl-dev gdal-dev  gdal geos geos-dev
RUN apk add zsh curl wget git

RUN pip install --upgrade pip setuptools wheel
RUN pip install Pillow
RUN python -m pip install daphne
#zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
RUN zsh
RUN make --version
# install dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt /app/backend/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./docker/backend/entrypoint.sh /usr/src/entrypoint.sh

# copy project
COPY ./backend/ /app/backend/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]