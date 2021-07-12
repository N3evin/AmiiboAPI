FROM busybox
COPY . /amiiboapi
RUN [ "rm", "-rf", "/amiiboapi/.git" ]
RUN [ "rm", "-rf", "/amiiboapi/images" ]
RUN [ "rm", "-rf", "/amiiboapi/gameinfo_generator" ]

FROM python:3
EXPOSE 5000/tcp

WORKDIR /usr/src/app

COPY --from=0 /amiiboapi .
RUN [ "find", "." ]
RUN pip install --no-cache-dir -r requirements.txt
RUN [ "python", "./last_updated.py" ]

CMD [ "python", "./app.py" ]
