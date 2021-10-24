#!/usr/bin/env python

from os import environ
from time import sleep
from smtplib import SMTP
from requests import get
from jsonpath_ng import parse


# read environment variables
url = environ['STREAM_METADATA_URL']
sleep_time = int(environ.get('WATCH_SLEEP_TIME_SECONDS') or 60)
track_json_path = environ['TRACK_JSON_PATH']
track_match_string = environ['TRACK_MATCH_STRING'].lower()
smtp_host = environ['SMTP_HOST']
smtp_port = int(environ['SMTP_PORT'])
smtp_tls = environ.get('SMTP_TLS') is not None
smtp_username = environ['SMTP_USERNAME']
smtp_password = environ['SMTP_PASSWORD']
smtp_from_addr = environ['SMTP_FROM_ADDR']
smtp_to_addrs = environ['SMTP_TO_ADDR'].split(',')


def send_email(track):
    print("Sending email")
    smtp_obj = SMTP(host=smtp_host, port=smtp_port)
    if smtp_tls:
        smtp_obj.starttls()
    smtp_obj.login(user=smtp_username, password=smtp_password)
    msg="""From: {}
To: {}
MIME-Version: 1.0
Content-type: text/plain
Subject: Now playing: {}
""".format(smtp_from_addr, ', '.join(smtp_to_addrs), track)
    smtp_obj.sendmail(
        from_addr=smtp_from_addr,
        to_addrs=smtp_to_addrs,
        msg=msg)
    smtp_obj.quit()


def watch_stream():
    print("Watching stream at URL: {}".format(url))

    jsonpath_expression = parse('${}'.format(track_json_path))
    found = False

    while True:
        try:
            response = get(url)
            if response.status_code == 200:
                body = response.json()
                match = jsonpath_expression.find(body)
                if match:
                    match = match[0].value
                    print("Track data: {}".format(match))
                    if match.lower().find(track_match_string) != -1:
                        print("Track data matches '{}'!".format(track_match_string))
                        if not found:
                            found = True
                            send_email(match)
                    else:
                        print("Track does not match '{}'".format(track_match_string))
                        found = False
                else:
                    print("Metadata does not contain the json path for the track")
            else:
                print("Error: {}".format(response.status_code))
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            print("Sleeping for {} seconds...".format(sleep_time))
            sleep(sleep_time)


watch_stream()