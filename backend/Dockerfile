FROM python:3

COPY analysis.py /
COPY master.py /
COPY worker.py /

RUN pip install tqdm

ENTRYPOINT ["python", "./master.py"]

CMD [ "www.dockerfile.backend.example.de" ]
