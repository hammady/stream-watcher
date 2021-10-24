FROM python:3.8-alpine3.11
LABEL maintainer="Hossam Hammady <github@hammady.net>"
WORKDIR /home

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "/home/watch-stream.py" ]