# stream-watcher

Watch a radio stream metadata URL and notify subscribers by email each time
a matching track is observed.

## Build

```bash
docker build . -t stream-watcher:1
```

## Configure and Run

```bash
docker run -d \
    -e STREAM_METADATA_URL="https://control.internet-radio.com:2199/external/rpc.php?m=streaminfo.get&username=mnnexus" \
    -e WATCH_SLEEP_TIME_SECONDS=60 \
    -e EXIT_AFTER_SLEEP_COUNT=100 \
    -e TRACK_JSON_PATH=.data[0].song \
    -e TRACK_MATCH_STRING=live \
    -e SMTP_HOST=smtp.gmail.com \
    -e SMTP_PORT=587 \
    -e SMTP_TLS=1 \
    -e SMTP_USERNAME=USERNAME_HERE \
    -e SMTP_PASSWORD="PASSWORD_HERE" \
    -e SMTP_FROM_ADDR="Sender Name <sender@example.com>" \
    -e SMTP_TO_ADDR=email1@example.com,email2@example.com  \
    --restart always \
    stream-watcher:1
```

The above will run forever and will check the URL every 60 seconds for a matching
string (`live`) in the returned JSON at path (`.data[0].song`). When it matches the
string for the first time, it will send an email using the configured SMTP server
to the list of emails: email1@example.com and email2@example.com.
It will not send again unless the track has changed to a non-match then matches
again, and so on.
It will exit after it reaches `EXIT_AFTER_SLEEP_COUNT=100` sleeps (60 seconds each).
Note that it will automatically restart. If set to 0 or unset, it will run forever.