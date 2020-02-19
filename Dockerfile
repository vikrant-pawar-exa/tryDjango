FROM python:3.8.1-slim-buster

WORKDIR /home/

COPY ./requirements.txt /home/requirements.txt

RUN pip3 install -r requirements.txt
COPY . /home/.


#ENTRYPOINT ["tail", "-f", "/dev/null"]

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]
