FROM python:3.8-alpine3.11
LABEL maintainer="Hossam Hammady <github@hammady.net>"
WORKDIR /home

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

HEALTHCHECK --interval=20s --timeout=3s --start-period=5s --retries=3 CMD [ "/home/healthz.sh" ]

CMD [ "/home/watch-stream.py" ]
