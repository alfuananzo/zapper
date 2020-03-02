from zapper.helpers import report_to_cli, store
from urllib.parse import urlparse

class report:
    def __init__(self, api):
        self.api = api

    def alerts(self, target):
        report_to_cli("The following alerts were found for target %s:" % target)

        alerts = []
        for target_site in self.target_sites(target):
            alerts += self.api.call('POST', 'JSON/core/view/alerts',  {'zapapiformat': 'JSON', 'formMethod': 'POST', 'baseurl': target_site}).json()['alerts']

        alert_dict = {'High': [], 'Medium': [], 'Low': [], 'Informational': []}
        for alert in alerts:
            print(" -", "%s (CONFIDENCE: %s) - %s)" % (alert['risk'], alert['confidence'], alert['alert']))
            alert_dict[alert['risk']].append(alert)

        self.build_html_header(target, alert_dict)
        if len(alert_dict['High']) > 0:
            store('     <h3 id="high"> High findings </h3>', 'report.html', 'a')
        for alert in alert_dict['High']:
            self.build_html_alert(alert)

        if len(alert_dict['Medium']) > 0:
            store('     <h3 id="medium"> Medium findings </h3>', 'report.html', 'a')
        for alert in alert_dict['Medium']:
            self.build_html_alert(alert)

        if len(alert_dict['Low']) > 0:
            store('     <h3 id="low"> Low findings </h3>', 'report.html', 'a')
        for alert in alert_dict['Low']:
            self.build_html_alert(alert)

        if len(alert_dict['Informational']) > 0:
            store('     <h3 id="info"> Informational findings </h3>', 'report.html', 'a')
        for alert in alert_dict['Informational']:
            self.build_html_alert(alert)
        self.build_html_footer()

    def build_html_header(self, target, alert_dict):
        store("""<html>
    <head>
        <META http-equiv='Content-Type' content='text/html; charset=UTF-8'>
        <title>ZAP scan report</title>
        <style>
            body{
              font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
              color: #000;
              font-size: 13px;
            }
            h1{
              text-align: center;
              font-weight: bold;
              font-size: 32px;
            }
            h2{
              font-size: 24px;
            }
            h3{
              font-size: 16px;
            }
            table{
              border: none;
              font-size: 13px;
            }
            td, th {
              padding: 3px 4px;
            }
            th{
              font-weight: bold;
            }
            .results th{
              text-align: left;
            }
            .spacer{
              margin: 10px;
            }
            .spacer-lg{
              margin: 40px;
            }
            .indent1{
              padding: 4px 20px;
            }
            .indent2{
              padding: 4px 40px;
            }
            .risk-high{
              background-color: red;
              color: #FFF;
            }
            .risk-medium{
              background-color: orange;
              color: #FFF;
            }
            .risk-low{
              background-color: yellow;
              color: #000;
            }
            .risk-info{
              background-color: blue;
              color: #FFF;
            }
            .summary th{
              color: #FFF;
            }
        </style>
    </head>
    <body>
        <h1> Zapper scan report for %s </h1>
        <p></p>
        <h3> Scan summary </h3>
        <table width='45%%' class='summary'>
            <tr bgcolor='#666666'><th width='45%%' height="24">Risk Level</th><th width='55%%' align='center'>Number of Alerts</th><tr>
            <tr bgcolor='#e8e8e8'><td><a href='#high'>High</a></td><td align='center'>%i</td></tr>
            <tr bgcolor='#e8e8e8'><td><a href='#medium'>medium</a></td><td align='center'>%i</td></tr>
            <tr bgcolor='#e8e8e8'><td><a href='#low'>low</a></td><td align='center'>%i</td></tr>
            <tr bgcolor='#e8e8e8'><td><a href='#info'>info</a></td><td align='center'>%i</td></tr>
        </table>
        <h2> Alert details </h2>""" % (target, len(alert_dict['High']), len(alert_dict['Medium']), len(alert_dict['Low']), len(alert_dict['Informational'])), 'report.html')

    def build_html_footer(self):
        store("""
    </body>
</html>""", 'report.html', 'a')

    def build_html_alert(self, alert):
        store("""
        <div class='spacer'></div>
        <table width='100%%' class='results'>
            <tr height='24' class='risk-%s'><a name='%s'></a><th width='20%%'>%s (Confidence: %s)</th><th width='80%%'>%s</th></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%'>Description</td><td width='80%%'><p>%s</p></td></tr>
            <tr vAlign='top'><td colspan='2'></td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%' class='indent1'>URL</td><td width='80%%'>%s</td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%' class='indent2'>Method</td><td width='80%%'>%s</td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%' class='indent2'>Parameter</td><td width='80%%'>%s</td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%'>Solution</td><td width='80%%'><p>%s</p></td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%'>Reference</td><td width='80%%'><p>%s</p></td></tr>
            <tr bgcolor='#e8e8e8'><td width='20%%'>CWE Id</td><td width='80%%'>525</td></tr>
        </table>""" % (alert['risk'], alert['risk'], alert['risk'], alert['confidence'].replace('\n', '<br>'), alert['name'], alert['description'].replace('\n', '<br>'), alert['url'].replace('\n', '<br>'), alert['method'].replace('\n', '<br>'), alert['param'].replace('\n', '<br>'), alert['solution'].replace('\n', '<br>'), alert['reference'].replace('\n', '<br>')), 'report.html', 'a')

    def target_sites(self, target):
        target_host = urlparse(target).netloc
        sites = self.api.call('POST', 'JSON/core/view/sites', {'zapapiformat': 'JSON', 'formMethod': 'POST'}).json()['sites']
        return [site for site in sites if urlparse(site).netloc == target_host]
