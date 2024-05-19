FROM python:3.12.3-alpine as builder

RUN apk add python3-dev build-base linux-headers pcre-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12.3-alpine

RUN apk add nginx supervisor

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

RUN rm /etc/nginx/nginx.conf

COPY webserver/nginx.conf /etc/nginx/nginx.conf
COPY webserver/bitsky.conf /etc/nginx/conf.d/bitsky.conf
COPY webserver/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY webserver/supervisord.conf /etc/supervisor/supervisord.conf

COPY src /project/src

WORKDIR /project

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
