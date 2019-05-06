
class report:
    def __init__(self, api):
        self.api = api

    def report_alerts(self):
        self.report("The following alerts were found for target %s:" % self.target)

        alerts = []
        for target_site in self.get_target_sites(self.target):
            alerts += self.call('POST', 'JSON/core/view/alerts',  {'zapapiformat': 'JSON', 'formMethod': 'POST', 'baseurl': target_site}).json()['alerts']

        for alert in alerts:
            print(" -", "%s (CONFIDENCE: %s) - %s)" % (alert['risk'], alert['confidence'], alert['alert']))

    def report_urls(self):
        self.report("The following URLs were found for target %s:" % self.target)

        urls = []
        for target_site in self.get_target_sites(self.target):
            urls += self.call('POST', 'JSON/core/view/urls',  {'zapapiformat': 'JSON', 'formMethod': 'POST', 'baseurl': target_site}).json()['urls']

        for url in urls:
            print(" -", url)

    def report_target_sites(self, target):
        sites = self.call('POST', 'JSON/core/view/sites', {'zapapiformat': 'JSON', 'formMethod': 'POST'}).json()['sites']
        return [site for site in sites if site[-len(self.target_host):] == self.target_host]
