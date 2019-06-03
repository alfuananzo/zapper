import requests, errno, json

class api:
    def __init__(self, url, api_key=None):
        self.zap_url = url
        self.s = requests.Session()
        if 'localhost' in self.zap_url or '127.0.0.1' in self.zap_url:
            self.s.trust_env = False

        # Test connection
        self.call('GET', '/')

    def call(self, request_type, api_endpoint, data={}, headers={}):
        try:
            r = self.s.request(request_type, "%s/%s" % (self.zap_url, api_endpoint), data=data, headers=headers, allow_redirects=True)
        except (ConnectionRefusedError, requests.exceptions.ConnectionError):
            print("ERROR: Couldnt connect to server, please make sure ZAP is running on %s" % self.zap_url)
            exit(errno.ENETUNREACH)
        if r.status_code != 200:
            try:
                print("ERROR: %s when calling %s" % (r.json()['message'], api_endpoint))
            except json.decoder.JSONDecodeError:
                print("ERROR %s when calling %s" % (r.text, api_endpoint))
            exit(1)
        return r
