FROM python:3.7

# use pip caching (COPYs and ADDs in this order!)
COPY requirements.txt /
WORKDIR /
RUN pip install -r requirements.txt

# now add the rest
ENV TZ=Europe/Berlin

COPY app.py /
COPY index.html /
COPY analysis.py /
COPY master.py /
COPY scanner.py /
COPY storage.py /
COPY job_mng.py /
COPY env.py /

CMD ["python", "app.py"]
