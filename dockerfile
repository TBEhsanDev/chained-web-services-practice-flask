FROM python:3.9
WORKDIR /usr/src
COPY . ./
RUN if [ -d "./venv" ]; then rm -rf "./venv" ;fi
RUN python3 -m venv venv
RUN . ./venv/bin/activate
RUN pip install setuptools==57.5.0 httpie
RUN pip install --no-cache-dir -r requirements
RUN apt-get update
RUN apt-get install -y nginx
COPY default /etc/nginx/sites-available
RUN  apt-get update && apt-get install -y redis-server
CMD  service nginx start && service redis-server start && ./run.sh && sleep infinity