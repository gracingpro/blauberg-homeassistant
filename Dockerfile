FROM python:3.11.0-bullseye
RUN apt-get update -y && apt-get install -y apt-utils
RUN apt-get update -y && apt-get install -y libev-dev build-essential libssl-dev libevdev2 python3-dev
RUN apt-get update && apt-get install -y supervisor
WORKDIR /opt/blauberg
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./Data ./Data
COPY ./References ./References
COPY ./Services ./Services
COPY ./setup.py .
RUN pip3 install .
CMD ["/usr/bin/supervisord"]
