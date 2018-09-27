FROM python:3

ADD analysis.py /
ADD backend.py /
ADD storage /storage

# RUN pip install json

ENTRYPOINT ["python", "./backend.py"]

CMD [ "www.dockerfile.backend.example.de" ]
