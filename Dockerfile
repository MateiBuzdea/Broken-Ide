# base image
FROM ubuntu:22.04

ENV AppDir=/app/

# envs for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y --upgrade pip && apt-get install -y libcap2-bin

# copy the server-setup.sh file in root
COPY server-setup.sh /root/
COPY flag.txt /root/

# create webapp directory
RUN mkdir -p $AppDir
COPY app $AppDir
WORKDIR $AppDir

# install deps
RUN pip install -r requirements.txt

WORKDIR /

# final setup
RUN useradd server-adm && chown -R server-adm:server-adm /app
RUN chmod 500 /root/server-setup.sh
RUN find /app -name *.py -exec chmod 555 {} \;
RUN setcap cap_sys_chroot+eip /usr/bin/python3.10

EXPOSE 8000

CMD /root/server-setup.sh
