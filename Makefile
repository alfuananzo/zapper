PYTHON3_OK := $(shell type -P python3)
ifeq ('$(PYTHON3_OK)','')
$(error package 'python3' not found)
endif
PIP3_OK := $(shell type -P pip3)
ifeq ('$(PIP3_OK)','')
$(error package 'pip3' not found)
endif
BASE_OS := $(shell uname)
ifeq ($(BASE_OS), Darwin)
link_loc = /usr/local/bin
else
link_loc = /usr/bin
endif


init:
	pip3 install virtualenv

install:
	# Installation
	mkdir -p /opt/zapper/
	cp -r ./zapper /opt/zapper/zapper && cp ./zapper.py /opt/zapper/ && cp ./Requirements.txt /opt/zapper/
	cd /opt/zapper/ && virtualenv env && source env/bin/activate && pip3 install -r Requirements.txt && chmod +x /opt/zapper/zapper.py
	chmod -R 755 /opt/zapper
	mkdir -p /etc/zapper/
	cp ./zap.config /etc/zapper/zapper.config
	chmod -R 755 /etc/zapper
	ln -sf /opt/zapper/zapper.py $(link_loc)/zapper

.PHONY: init install
