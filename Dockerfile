FROM python:2.7.13
MAINTAINER Indexyz <r18@indexes.nu>

RUN mkdir /usr/app

COPY . /usr/app

RUN pip install requests[security] && \
    pip install -r /usr/app/requirements.txt && \
    mkdir db 

WORKDIR "/usr/app/db"
ENTRYPOINT ["python"]
CMD ["/usr/app/main.py"]
