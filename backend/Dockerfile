# Fetching official base image for python
FROM python:3.12.5
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /backend


RUN apt-get update
RUN apt-get install -y curl \
  gnupg \
  gnupg2 \
  build-essential \
  default-libmysqlclient-dev \
  pkg-config \
  unixodbc \
  unixodbc-dev \
  libpq-dev \
  tzdata \
  cron \
  nano \
  iputils-ping \
  apt-transport-https \
  redis

# RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc -o /etc/apt/trusted.gpg.d/microsoft.asc.gpg \
#   && curl -sSL https://packages.microsoft.com/config/debian/10/prod.list -o /etc/apt/sources.list.d/mssql-release.list

RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl -sSL https://packages.microsoft.com/config/debian/10/prod.list -o /etc/apt/sources.list.d/mssql-release.list

# RUN apt update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
RUN apt update && ACCEPT_EULA=Y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the timezone
ENV TZ=America/Los_Angeles
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt /backend
RUN pip install -r requirements.txt --no-cache-dir
COPY . /backend