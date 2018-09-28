FROM python:3

ADD analysis.py /
ADD master.py /
ADD worker.py /

RUN pip install tqdm

ENTRYPOINT ["python", "./master.py"]

CMD [ "www.dockerfile.backend.example.de" ]
