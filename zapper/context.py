from helpers import report_to_cli

class context:
    def __init__(self, target, scope, api, force):
        # Set the context name
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
                    self.delete_context()
                else:
                    report_to_cli('ZAP is already scanning %s, exiting.' % self.context)
                    exit(1)

            context_info = self.api.call('POST', 'JSON/context/action/newContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context}).json()
            self.context_id = context_info['contextId']
            report_to_cli("Created new ZAP context %s with context ID %s" % (self.context, self.context_id))

            # Include the domain(s) into the context
            for scope_url in self.scope:
                self.api.call('POST', 'JSON/context/action/includeInContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context, 'regex': ".*" + scope_url + ".*"})

    def delete_context(self):
        self.api.call('POST', 'JSON/context/action/removeContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context})
        report_to_cli("Removed ZAP context %s" % self.context)

    def get_context(self):
        return self.context

    def get_context_id(self):
        return self.context_id

    def store_context(self):
        self.api.report('Storing context %s' % self.context)
        report_to_cli('POST', 'JSON/context/action/exportContext', {'zapapiformat': 'JSON', 'formMethod': 'POST', 'contextName': self.context, 'contextFile': '%s.context' % self.context})
