from time import sleep
from helpers import report_to_cli

class scanner:
    def __init__(self, api):
        self.api = api
        return

    def active_scan(self, target, context_id):
        #report_to_cli_urls()
        report_to_cli("Starting active scan")
        scan_id = self.api.call('POST', 'JSON/ascan/action/scan/', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextId': context_id}).json()['scan']
        progress = self.get_active_scan_progress(scan_id)
        while progress != 100:
            print("Active scan %i%% completed" % progress, end="\r")
            sleep(10)
            progress = self.get_active_scan_progress(scan_id)
        print("Active scan %i%% completed" % progress)
        report_to_cli("Active scan complete")

    def spider_scan(self, target, context):
        report_to_cli("Starting spider")
        spider = self.api.call('POST', 'JSON/spider/action/scan', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': context, 'url': target}).json()
        spider_id = spider['scan']

        progress = self.get_spider_status(spider_id)
        while progress != 100:
            print("Spider %i%% completed" % progress, end="\r")
            sleep(10)
            progress = self.get_spider_status(spider_id)
        print("Spider %i%% completed" % progress)
        report_to_cli("Spider complete")

    def passive_scan(self):
        report_to_cli("Starting passive scan")
        passive_scan_items_remaining = self.get_passive_scan_progress()
        i = 0

        # Give the passive scan time to pop things in queue
        if not passive_scan_items_remaining:
            sleep(30)

        # While there are items to scan and ~10 minutes have not elapsed yet
        while passive_scan_items_remaining and i < 60:
            print("%i items remaining to scan" % passive_scan_items_remaining, end="\r")
            i+=1
            sleep(10)
            passive_scan_items_remaining = self.get_passive_scan_progress()
        print("0 items remaining to scan")
        report_to_cli("Passive scan complete")

    def get_spider_status(self, id):
        spider = self.api.call('POST', 'JSON/spider/view/status', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'scanId': id}).json()
        return int(spider['status'])

    def get_passive_scan_progress(self):
        scan = self.api.call('POST', 'JSON/pscan/view/recordsToScan', {'zapapiformat': 'JSON', 'formMethod': 'POST'}).json()
        return int(scan['recordsToScan'])

    def get_active_scan_progress(self, id):
        scan = self.api.call('POST', 'JSON/ascan/view/status', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'scanId': id}).json()
        return int(scan['status'])
