FROM ubuntu:18.04

LABEL maintainer="rrgasymov"

RUN apt-get update \
 && apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev \
zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev \
libncursesw5-dev libffi-dev uuid-dev wget -y

WORKDIR /

RUN cd /tmp \
    && wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz \
    && tar xzf Python-3.9.9.tgz \
    && cd Python-3.9.9 \
    && ./configure --enable-optimizations \
    && make altinstall

COPY static ./static
COPY templates ./templates
COPY parse_multilink.py ./parse_multilink.py
COPY main.py ./main.py
COPY statistic_plots.py ./statistic_plots.py
COPY requirements.txt ./requirements.txt

RUN pip3.9 install --upgrade -r requirements.txt

CMD ["python3.9", "./main.py"]