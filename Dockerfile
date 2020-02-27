FROM openjdk:15-oraclelinux7

WORKDIR /home/

RUN curl https://bintray.com/sbt/rpm/rpm | tee /etc/yum.repos.d/bintray-sbt-rpm.repo
RUN yum install -y sbt 

RUN sbt test
# RUN yum install o

RUN yum install -y python3

# RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python2.7 get-pip.py

RUN pip install pandas
#WORKDIR /home/

COPY requirements.txt /home/requirements.txt

RUN pip3 install -r requirements.txt


COPY . /home/.

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]

# ENTRYPOINT ["tail", "-f", "/dev/null"]
