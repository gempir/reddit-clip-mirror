FROM debian:buster

RUN apt-get update && apt-get install python3 python3-pip curl gnupg2 -y && \
curl https://mega.nz/linux/MEGAsync/Debian_10.0/amd64/megacmd-Debian_10.0_amd64.deb --output megacmd.deb && \
echo path-include /usr/share/doc/megacmd/* > /etc/dpkg/dpkg.cfg.d/docker && \
apt install ./megacmd.deb -y

COPY "requirements.txt" "/requirements.txt"

RUN python3 -m pip install -r /requirements.txt

COPY "entrypoint.sh" "/entrypoint.sh"
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]