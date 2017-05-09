FROM hyalx/centos
MAINTAINER Indexyz <r18@indexes.nu>

RUN mkdir /usr/app

COPY . /usr/app

RUN yum install epel-release -y && \
    yum install python-setuptools python-devel openssl-devel -y && \
    easy_install pip && \
    pip install --upgrade requests && \
    pip install requests[security] && \
    pip install -r /usr/app/requirements.txt && \
    mkdir db 

WORKDIR "/usr/app/db"
ENTRYPOINT ["python"]
CMD ["/usr/app/main.py"]
