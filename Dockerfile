FROM ubuntu:latest

RUN echo Updating existing packages, installing and upgrading python and pip.
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN pip3 install --upgrade pip
RUN echo Copying the ADSC chart service into a service directory.
COPY ./ms /bookie
WORKDIR /bookie
ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo Installing Python packages listed in requirements.txt
RUN pip3 install -r requirements.txt
RUN echo Executing job
ENTRYPOINT ["python3"]
CMD [ "app.py" ]