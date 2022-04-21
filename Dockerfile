FROM ubuntu:focal

RUN apt update && apt install --no-install-recommends -y nginx

RUN rm -f /etc/nginx/sites-available/*

RUN rm -f /etc/nginx/sites-enabled/*

WORKDIR /dockerfile_generator

ADD . .



RUN chmod +x startup.sh

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ./dockerfileGen-nginx /etc/nginx/sites-available/dockerfileGen-nginx

RUN ln -s /etc/nginx/sites-available/dockerfileGen-nginx /etc/nginx/sites-enabled/

EXPOSE 80

CMD ["./startup.sh"]

