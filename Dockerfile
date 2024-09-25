FROM python:3.8

RUN apt-get update && apt-get install -y \
	git \
	openjdk-17-jdk \
	openjdk-17-jre 
	
WORKDIR /workspace
ADD . /workspace

RUN pip install --upgrade pip
RUN pip install -U pip setuptools wheel
RUN pip install -r requirements

