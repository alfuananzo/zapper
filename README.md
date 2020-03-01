## Current status: ALPHA
# Zapper
Zap is a nice tool for DAST scanning in a CI/CD pipeline. However, it lacks functionality for larges scale scanning. There is no option to report findings based on the URL of the target, many (official) plugins like Jenkins plugins force the user to run ZAP locally instead of using a single ZAP instance for multiple targets. By centralising ZAP, you can increase the scalability and the manageability of the tool.

In comes Zapper, a pure python3 wrapper for the ZAP api that allows users to use a central ZAP instance and creates abstraction for every step of the ZAP scanning process. By simply calling Zapper a user can start a scan on a given scope without having to click through the UI, build your own API calls for scanning or changing / rewriting plugins.

## Installation

### Docker

Coming soon

### Install locally

Currently, OSx and any Linux version is supported. Windows will be added at some point.

```sh
git clone https://github.com/alfuananzo/zapper.git
cd zapper
make
make install
```


### Contribute

Download the source code using

```sh
git clone https://github.com/alfuananzo/zapper.git
cd zapper
pip3 install -r Requirements.txt
```

## Configuration

The makefile installs the configuration of zapper in `/etc/zapper/zapper.conf`.

## usage

Starting off a basic scan can be done by invoking Zapper using

```sh
$ zapper --target http://google.com
```
