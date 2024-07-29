FROM python:3.12

ENV PYTHONPATH=/edgeconnect/src
ENTRYPOINT ["/usr/local/bin/python"]
CMD ["-m", "edgeconnect.http"]

RUN mkdir /edgeconnect
WORKDIR /edgeconnect
EXPOSE 8000

COPY ./requirements ./requirements
RUN /usr/local/bin/pip install -r ./requirements/base.txt

COPY ./src /edgeconnect/src
