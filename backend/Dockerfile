FROM python:3

ADD analysis.py /
ADD master.py /
ADD storage /storage

# RUN pip install json

ENTRYPOINT ["python", "./master.py"]

CMD [ "www.dockerfile.backend.example.de" ]
