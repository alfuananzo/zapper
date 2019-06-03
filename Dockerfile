FROM ubuntu
RUN apt update && apt upgrade -y
RUN apt install -y git python3 python3-pip
RUN pip3 install virtualenv
RUN git clone https://github.com/alfuananzo/zapper.git
WORKDIR zapper/
RUN mkdir -p /opt/zapper/
RUN cp -r ./zapper /opt/zapper/zapper && cp ./zapper.py /opt/zapper/ && cp ./Requirements.txt /opt/zapper/
RUN cd /opt/zapper/ && virtualenv env && . env/bin/activate && pip3 install -r Requirements.txt && chmod +x /opt/zapper/zapper.py
RUN chmod -R 755 /opt/zapper
RUN mkdir -p /etc/zapper/
RUN cp ./zap.config /etc/zapper/zapper.config
RUN chmod -R 755 /etc/zapper
RUN ln -sf /opt/zapper/zapper.py /bin/zapper
