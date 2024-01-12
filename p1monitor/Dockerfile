ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip py3-pyserial py3-aiohttp 

COPY run.sh /
COPY p1.py /

CMD ["/run.sh"]

