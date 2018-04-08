from typing import List
from marshmallow import Schema
from oad.schema import schema_to_dict, schema_to_ref
from oad.merge import dict_merge


class OpenAPI:
    def __init__(self):
        self.documentation = dict()
        self.schemas = dict()

    def add_documentation(self, documentation: dict):
        self.documentation = dict_merge(
            self.documentation, documentation)

    def add_schemas(self, schemas: List[Schema]):
        for schema in schemas:
            self.schemas[schema.__class__.__name__] = schema_to_dict(schema)


def doc(documentation: dict, schemas: List[Schema] = None):
    def inner(func):
        if not hasattr(func, '__openapi__'):
            func.__openapi__ = OpenAPI()

        func.__openapi__.add_documentation(documentation)

        if schemas:
            func.__openapi__.add_schemas(schemas)

        return func
    return inner


def request(
    documentation: dict = None,
    content_documentation: dict = None,
    content_type='application/json',
    schema=None
):
    def inner(func):
        schemas = []
        if isinstance(schema, Schema):
            schemas.append(schema)
            schema_ = schema_to_ref(schema)
        else:
            schema_ = schema or {'type': 'string'}

        return doc({
            'requestBody': dict_merge({
                'content': {
                    content_type: dict_merge({
                        'schema': schema_,
                    }, content_documentation or dict()),
                },
            }, documentation or dict()),
        }, schemas=schemas)(func)
    return inner


def response(
    documentation: dict = None,
    content_documentation: dict = None,
    status=200,
    content_type='application/json',
    schema=None
):
    def inner(func):
        schemas = []
        if isinstance(schema, Schema):
            schemas.append(schema)
            schema_ = schema_to_ref(schema)
        else:
            schema_ = schema or {'type': 'string'}

        return doc({
            'responses': {
                str(status): dict_merge({
                    'description': '',
                    'content': {
                        content_type: dict_merge({
                            'schema': schema_
                        }, content_documentation or dict()),
                    },
                }, documentation or dict()),
            },
        }, schemas=schemas)(func)
    return inner
