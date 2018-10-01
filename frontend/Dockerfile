FROM ubuntu

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python-all python-pip

ADD app.py /
ADD index.html /

RUN pip install Flask

EXPOSE 8888
CMD ["python", "app.py"]
