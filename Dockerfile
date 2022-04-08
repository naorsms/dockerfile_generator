FROM ubuntu:focal

RUN apt update && apt install --no-install-recommends -y \
#   python3.8 \
#	python3-pip\
#	python3-venv\
#   curl\
#   vim\
#   ping\
#   traceroute\
#   wget\
	nginx
	
RUN rm -f /etc/nginx/sites-available/*

RUN rm -f /etc/nginx/sites-enabled/* 

WORKDIR /dockerfile_generator

ADD . .

#RUN python3 -m venv /dockerfileGen

#ENV PATH="/dockerfileGen/bin:$PATH"


#RUN pip3 install --no-cache-dir -r requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ./dockerfileGen-nginx /etc/nginx/sites-available/dockerfileGen-nginx

RUN ln -s /etc/nginx/sites-available/dockerfileGen-nginx /etc/nginx/sites-enabled/



EXPOSE 80

CMD ["./startup.sh"]
