ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 
RUN pip install serial

COPY run.sh /
COPY p1.py /

CMD ["/run.sh"]

