from oad.merge import dict_merge


class OpenAPIDoc:

    def __init__(self, documentation: dict = None, *args, **kwargs):
        """ OpenAPI documentation
        https://swagger.io/docs/specification/about/
        """

        self.paths = dict()
        self.schemas = dict()
        self.parameters = dict()
        self.responses = dict()
        self.security_schemes = dict()
        self.tags = list()

        self.components = dict(
            schemas=self.schemas,
            parameters=self.parameters,
            responses=self.responses,
            securitySchemes=self.security_schemes,
        )

        self.doc = dict_merge({
            'openapi': '3.0.0',
            'info': {
                'title': '',
                'description': '',
                'termsOfService': '',
                'contact': {
                    'name': '',
                    'url': '',
                    'email': '',
                },
                'license': {
                    'name': '',
                    'url': '',
                },
                'version': '',
            },
            'tags': self.tags,
            'paths': self.paths,
            'components': self.components,
        }, documentation or {})

    def add_tag(self, name: str, documentation: dict = None):
        """ Add tag info
        https://swagger.io/docs/specification/grouping-operations-with-tags/
        """

        self.tags.append(dict_merge({
            'name': name,
        }, documentation or {}))
        return self

    def add_security(self, name: str, type: str, documentation: dict = None):
        """ Add security
        https://swagger.io/docs/specification/authentication/
        """

        self.security_schemes[name] = dict_merge({
            'type': type,
        }, documentation or {})
        return self

    def add_server(self, url, documentation: dict = None):
        """ Add server info
        https://swagger.io/docs/specification/api-host-and-base-path/
        """

        self.doc = dict_merge(self.doc, {
            'servers': [dict_merge({
                'url': url,
            }, documentation or {})],
        })
        return self

    def add_parameter(self, name, documentation: dict = None):
        """ Add path parameters
        https://swagger.io/docs/specification/serialization/
        """

        self.parameters[name] = dict_merge({
            'name': name,
            'in': 'path',
            'required': True,
            'schema': {'type': 'string'},
        }, documentation or {})
        return self

    def add_path(self, url, method, documentation: dict):
        """ Add path
        https://swagger.io/docs/specification/paths-and-operations/
        """

        if url not in self.paths:
            self.paths[url] = dict()
        self.paths[url][method] = documentation
        return self

    def add_schema(self, name: str, documentation: dict):
        """ Add schema
        https://swagger.io/docs/specification/components/
        """

        self.schemas[name] = documentation
        return self

    def add_response(self, name: str, documentation: dict):
        """ Add response
        https://swagger.io/docs/specification/components/
        """

        self.responses[name] = documentation
        return self

    def to_dict(self, *args, **kwargs):
        return self.doc
