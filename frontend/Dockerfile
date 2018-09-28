FROM ubuntu

RUN apt-get update
RUN apt-get upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all python-pip

ADD app.py /
ADD requirements.txt /

RUN pip install Flask

EXPOSE 5000
CMD ["python", "app.py"]
