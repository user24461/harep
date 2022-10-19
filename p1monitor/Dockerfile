ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
        python3 

COPY run.sh /
COPY p1.py /

CMD ["/run.sh"]

