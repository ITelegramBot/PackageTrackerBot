FROM hyalx/centos:centos6
MAINTAINER Indexyz <r18@indexes.nu>

RUN mkdir /usr/app

COPY . /usr/app

RUN yum install epel-release -y && \
    yum install python-setuptools -y && \
    easy_install pip && \
    pip install -r /usr/app/requirements.txt

WORKDIR "/usr/app"
ENTRYPOINT ["python"]
CMD ["/usr/app/main.py"]