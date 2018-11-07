FROM kalilinux/kali-linux-docker

RUN apt-get update --fix-missing
RUN apt-get install -y python3 python3-pip wapiti

# use pip caching (COPYs and ADDs in this order!)
COPY requirements.txt /
WORKDIR /
RUN pip3 install -r requirements.txt

# now add the rest
ENV TZ=Europe/Berlin

COPY app.py /

# Run the application.
# CMD ["theharvester", "--help"]
CMD ["python3", "app.py"]
