FROM ubuntu:rolling

RUN apt-get update
RUN apt-get install -y build-essential software-properties-common python3.6 python3.6-venv wget


RUN wget https://cmake.org/files/v3.8/cmake-3.8.1-Linux-x86_64.sh
RUN chmod +x ./cmake-3.8.1-Linux-x86_64.sh
RUN ./cmake-3.8.1-Linux-x86_64.sh --skip-license

ADD . app-src
WORKDIR /app-src
CMD ./build.sh