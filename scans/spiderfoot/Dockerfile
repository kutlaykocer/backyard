FROM python:2.7

# use pip caching (COPYs and ADDs in this order!)
COPY requirements.txt /
WORKDIR /
RUN pip install -r requirements.txt

# now add the rest
ENV TZ=Europe/Berlin

COPY app.py /
COPY download/sfcli.py /

CMD ["python", "app.py"]
