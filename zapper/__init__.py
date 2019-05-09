from zapper.helpers import report_to_cli, check_args
from zapper.api import api
from zapper.scanner import scanner
from zapper.context import context
from zapper.report import report

import configparser
import argparse
from urllib.parse import urlparse

def init():
    """
    The initialisation of the Zapper automated scanning process.
    """
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

    zap_url = "%s://%s:%s" % (args.proto, args.host, args.port)
    zapper_api =  api(zap_url)
    zapper_scanner = scanner(zapper_api)
    zapper_report = report(zapper_api)

    report_to_cli("Starting zap scan using ZAP host %s" % zap_url)

    target_host = urlparse(args.target).netloc
    target_sub_dir = urlparse(args.target).path
    if args.report:
        zapper_report.alerts(args.target)
    else:
        scan_context = context(args.target, args.scope, zapper_api, args.overwrite)

        if not args.no_spider:
            zapper_scanner.spider(args.target, scan_context.name())
        if not args.no_passivescan:
            zapper_scanner.passive()
        if not args.no_activescan:
            zapper_scanner.active(args.target, scan_context.id())
        scan_context.store()
        scan_context.delete()
    report_to_cli("Zapper finished, exiting.")
