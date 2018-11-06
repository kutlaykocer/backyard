FROM kalilinux/kali-linux-docker

RUN apt-get update
RUN apt-get install -y python3 python3-pip nmap
RUN wget -O /usr/share/nmap/scripts/vulners.nse https://raw.githubusercontent.com/vulnersCom/nmap-vulners/master/vulners.nse

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
