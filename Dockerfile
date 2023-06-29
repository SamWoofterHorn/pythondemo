###########
# BUILD ENV
###########

FROM ubuntu:22.04 AS backend-build-env
LABEL maintainer Brad Wells <bwells@altalang.com>

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-dev \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-setuptools

RUN pip install --upgrade setuptools wheel

RUN mkdir -p /build/wheels
WORKDIR /build/wheels

COPY requirements.txt /build/wheels/requirements.txt

RUN pip wheel -w /build/wheels -r requirements.txt

# and build a wheel for uWSGI
RUN pip wheel -w /build/wheels uwsgi==2.0.20

#############
# FINAL IMAGE
#############

FROM altalang/python3:22.04
LABEL maintainer Brad Wells <bwells@altalang.com>

RUN echo "US/Eastern" > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        libpython3.10 \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -M --system --shell /usr/sbin/login --uid 101 web

RUN mkdir -p /app && chown web /app
WORKDIR /app

# install pip requirements before the codebase itself
# to avoid busting the docker cache
COPY requirements.txt /app/requirements.txt

# copy in the wheel cache from the build env image
RUN mkdir -p /wheels
COPY --from=backend-build-env /build/wheels /wheels

# install all dependencies from the wheel cache
RUN pip install --no-index --find-links /wheels --src /env -r requirements.txt

# install uWSGI from the wheel cache
RUN pip install --no-index --find-links /wheels uwsgi && chmod +x /usr/local/bin/uwsgi

# add application source
COPY --chown=web . /app/

# remove the wheel files
RUN rm -rf /wheels

USER web

EXPOSE 5001

CMD ["python3", "app.py", "server"]
