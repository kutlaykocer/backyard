FROM ubuntu

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python3.7 python3-pip

# use pip caching (COPYs and ADDs in this order!)
COPY requirements.txt /
WORKDIR /
RUN pip3 install -r requirements.txt
# now add the rest
COPY app.py /
COPY index.html /
COPY analysis.py /
COPY master.py /
COPY worker.py /

ENTRYPOINT ["python3", "app.py"]

CMD [ "www.dockerfile.backend.example.de" ]
