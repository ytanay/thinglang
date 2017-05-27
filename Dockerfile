FROM ubuntu

RUN apt-get update
RUN apt-get install -y build-essential software-properties-common


ADD https://cmake.org/files/v3.8/cmake-3.8.1-Linux-x86_64.sh cmake-install.sh
RUN chmod +x ./cmake-install.sh
RUN ./cmake-install.sh --skip-license

ADD . app-src
WORKDIR /app-src
CMD ./build.sh