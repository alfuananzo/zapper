#TODO: Kill scans if overwrite is set.

from zapper.helpers import report_to_cli

class context:
    def __init__(self, target, scope, api, force=False):
        """
        Control one Context entry of ZAP. A context has the following properties:

        Attributes:
            target: The target of the scan
            scope: The scope that is allowed to scan
            api: The ZAP api that it can call. Expectes the zapper.api class
            force: Overwrite the context if a current scan is going
        """

        # Remove special chars from target so it can be set as context name
        self.context = target.replace('/', '')

        self.scope = scope
        self.api = api
        self.force = force

        try:
            self.api.call('POST', 'JSON/context/action/importContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextFile': '%s.context' % self.context})
            report_to_cli("Found existing context %s, importing" % self.context)
            self.context_id = context_info['contextId']
            return True

        except:
            contexts = self.api.call('GET', 'JSON/context/view/contextList/?zapapiformat=JSON&formMethod=GET').json()
            if self.context in contexts['contextList']:
                if self.force:
                    self.delete()
                else:
                    report_to_cli('ZAP is already scanning %s, exiting.' % self.context)
                    exit(1)

            context_info = self.api.call('POST', 'JSON/context/action/newContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context}).json()
            self.context_id = context_info['contextId']
            report_to_cli("Created new ZAP context %s with context ID %s" % (self.context, self.context_id))

            # Include the domain(s) into the context
            for scope_url in self.scope:
                self.api.call('POST', 'JSON/context/action/includeInContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context, 'regex': ".*" + scope_url + ".*"})

    def delete(self):
        self.api.call('POST', 'JSON/context/action/removeContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context})
        report_to_cli("Removed ZAP context %s" % self.context)

    def name(self):
        return self.context

    def id(self):
        return self.context_id

    def store(self):
        report_to_cli('Storing context %s' % self.context)
        self.api.call('POST', 'JSON/context/action/exportContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context, 'contextFile': '%s.context' % self.context})
