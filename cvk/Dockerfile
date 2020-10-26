FROM python:3.7.7-slim

ENV CHROMEDRIVER=/usr/local/bin/chromedriver \
    OPENSSL_CONF=/etc/ssl/

# CHROME DRIVER SETUP
RUN apt-get update && apt-get install -y \
        curl \
        unzip \
        libglib2.0-dev \
        libnss3=2:3.26.2-1.1+deb9u1 \
        libgconf-2-4=3.2.6-4+b1 \
        libfontconfig1=2.11.0-6.7+b1 \
        xvfb && \
    curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb && \
    dpkg -i /chrome.deb || apt-get install -yf && \
    rm /chrome.deb && \
    curl https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/chromedriver && \
    unzip /usr/local/chromedriver -d /usr/local/bin && \
    chmod u+x /usr/local/bin/chromedriver

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /cvk
WORKDIR /cvk

EXPOSE $PORT
