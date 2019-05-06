#!/opt/zapper/env/bin/python

from helpers import report_to_cli, check_args
from scanner import scanner
from context import context
from api import zap_api
import configparser
import argparse
from urllib.parse import urlparse
from sys import argv

class zap:
    def __init__(self, zap_url):
        self.api = zap_api(zap_url)
        self.scanner = scanner(self.api)
        report_to_cli("Starting zap scan using ZAP host %s" % zap_url)

    def scan(self, target):
        self.target_host = urlparse(target).netloc
        self.target_sub_dir = urlparse(target).path
        self.target = target
        self.context = context(self.target, args.scope, self.api, args.overwrite)
        if args.report:
            self.report_alerts()
            exit()

        if not args.no_spider:
            self.scanner.spider_scan(target, self.context.get_context())
        if not args.no_passivescan:
            self.scanner.passive_scan()
        if not args.no_activescan:
            self.scanner.active_scan(target, self.context.get_context_id())
        self.report_alerts()
        self.download_report()
        self.store_context()
        self.delete_context()

    def download_report(self):
        report = self.call('GET', 'OTHER/core/other/htmlreport/')
        f = open('report.html', 'w')
        f.write(report.text)
        f.close()

    def report_alerts(self):
        self.report("The following alerts were found for target %s:" % self.target)

        alerts = []
        for target_site in self.get_target_sites(self.target):
            alerts += self.call('POST', 'JSON/core/view/alerts',  {'zapapiformat': 'JSON', 'formMethod': 'POST', 'baseurl': target_site}).json()['alerts']

        for alert in alerts:
            print(" -", "%s (CONFIDENCE: %s) - %s)" % (alert['risk'], alert['confidence'], alert['alert']))

parser = argparse.ArgumentParser(description='ZAP control unit for DAST scanning')
config = configparser.ConfigParser()

parser.add_argument('--config', help='Path to ZAP config', default='/etc/zapper/zapper.config')
parser.add_argument('--target', help='ZAP target (full URL. Example: https://google.nl)')
parser.add_argument('--host', help='ZAP host (Hostname only. Example: localhost)')
parser.add_argument('--port', help='ZAP port')
parser.add_argument('--proto', help='ZAP protocol (Either HTTP or HTTPS)')
parser.add_argument('--scope', nargs='+', help='URLS in scope of attack. Only the target will be attacked, but if URLS in scope are found at the target, these will also be scanned. By default, only the target is in scope.')
parser.add_argument('--overwrite', help="Force overwrite of sessions. This forces ZAP to start a scan even if another scan on the same target is already running.", action='store_true', default=False)
parser.add_argument('--no-passivescan', help="Dont run the passive scan. Use this if you dont proxy traffic through ZAP before running the scans.", action='store_true', default=False)
parser.add_argument('--no-activescan', help="Dont run the active scan. ZAP will not interact with the server and only interpet traffic proxied through it", action='store_true', default=False)
parser.add_argument('--no-spider', help="Dont run the spider. This will prevent ZAP from trying to find new URLs on the web page it has not seen before through the proxy", action='store_true', default=False)
parser.add_argument('--report', help="Dont scan just report the outcome of a previous scan", action='store_true', default=False)

args = parser.parse_args()
optional_args = ['scope', ]
config.read(args.config)

for arg in vars(args):
    if getattr(args, arg) is None and  arg not in optional_args:
        setattr(args, arg, config['zap'][arg])

if not args.scope:
    args.scope = [ urlparse(args.target).netloc ] if not config['zap']['scope'] else set([urlparse(args.target).netloc] + [ x.strip().lower() for x in config['zap']['scope'].split(',') ])
else:
    args.scope = set([urlparse(args.target).netloc] + [x.lower() for x in args.target ])





if not check_args(parser, args, 'host', 'port', 'proto', 'target'):
    exit(1)

zapper = zap("%s://%s:%s" % (args.proto, args.host, args.port))

zapper.scan(args.target)
