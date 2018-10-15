FROM python:2.7

# use pip caching (COPYs and ADDs in this order!)
COPY requirements.txt /
WORKDIR /
RUN pip install -r requirements.txt

# now add the rest
COPY app.py /
COPY download/sfcli.py /

# CMD ["python", "sfcli.py", "-s", "http://172.17.0.2:5001"]
CMD ["python", "app.py"]
# CMD ["bash"]
