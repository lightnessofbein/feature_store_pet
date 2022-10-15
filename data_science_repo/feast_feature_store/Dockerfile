FROM python:3.9-slim

COPY . .
RUN apt-get update
RUN pip install "feast[redis]"

RUN ["chmod", "+x", "startup.sh"]

# default feature server port
EXPOSE 6566 6567

# start feature server
CMD ["/bin/bash","-c","./startup.sh"]
