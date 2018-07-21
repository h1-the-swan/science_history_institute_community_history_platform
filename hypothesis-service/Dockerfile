FROM ubuntu:latest

ARG DEVELOPMENT

ENV NODE_ENV production

WORKDIR /var/lib/hypothesis

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libevent-dev \
    libffi-dev \
    libfontconfig \
    libpq-dev \
    libssl-dev \
    python-dev \
    python-setuptools \
    python-pip \
    python-virtualenv \
    curl \
    openssl \
    gnupg2

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt-get install -y nodejs

# Copy minimal data to allow installation of dependencies.
COPY requirements.txt ./
COPY requirements-dev.in ./

# Install build deps, build, and then clean up.
# RUN pip install -r requirements.txt
RUN echo "$DEVELOPMENT"
RUN if [ "$DEVELOPMENT" = "true" ]; then echo "installing python dependencies for development"; else echo "installing python dependencies"; fi
RUN if [ "$DEVELOPMENT" = "true" ]; then pip install -r requirements-dev.in ; else pip install -r requirements.txt; fi

# Copy collectd config
COPY conf/collectd.conf /etc/collectd/collectd.conf
RUN mkdir /etc/collectd/collectd.conf.d

COPY . .

# Expose the default port.
EXPOSE 5000

ENV CLIENT_OAUTH_ID $HYPOTHESIS_CLIENT_ID
ENV CLIENT_URL http://localhost:3001/hypothesis

# Set the application environment
ENV PATH /var/lib/hypothesis/bin:$PATH
ENV PYTHONIOENCODING utf_8
ENV PYTHONPATH /var/lib/hypothesis:$PYTHONPATH

# Start the web server by default
RUN npm install -g gulp-cli
RUN make clean
ENTRYPOINT ["make", "dev"]
