# Python library for generate valid OpenAPI v3 specification

[
![travis](https://api.travis-ci.org/lordent/oad.svg?branch=master)
](https://travis-ci.org/lordent/oad)

Read OpenAPI specification:
- [swagger](https://swagger.io/specification/)
- [github](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md)

Usage example:

```python
import asyncio
from oad import openapi, OpenAPIDoc


info = {
    'title': 'Test',
    'description': 'Test api description',
    'termsOfService': 'Test terms',
    'contact': {
        'name': 'Tester',
        'url': 'http://example.com',
        'email': 'test@example.com'
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    },
    'version': '1.0'
}

error_schema = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string'},
        'message': {'type': 'string'},
        'errors': {'type': 'object'}
    },
}

error_response = {
    'description': 'Error response',
    'content': {
        'application/json': {
            'schema': {
                '$ref': '#/components/schemas/Error'
            }
        }
    }
}

@openapi.doc({
    'summary': 'Test summary text',
    'description': 'Test description',
    'tags': ['test'],
    'parameters': [{
        '$ref': '#/components/parameters/TestParameter'
    }],
})
@openapi.request({
    'description': 'Test description',
}, content_documentation={
    'example': {
        'id': '4',
    },
}, schema={
    'type': 'object',
    'properties': {
        'id': {
            'type': 'integer',
            'format': 'int64',
            'example': '4',
        },
    },
})
@openapi.response()
@openapi.response(
    status=400, schema={'$ref': '#/components/schemas/Error'})
async def test_handler(*args, **kwargs):
    await asyncio.sleep(0)
    return 'Ok!', args, kwargs


doc = (
    OpenAPIDoc({
        'info': info,
    })
    .add_parameter('TestParameter')
    .add_tag('test', {'description': 'Test tag description'})
    .add_path(
        '/test/{TestParameter}', 'post',
        test_handler.__openapi__.documentation)
    .add_schema('Error', error_schema)
    .add_response('Error', error_response)
    .add_security('ApiKey', 'apiKey', {
        'in': 'header',
        'name': 'X-API-Key',
    })
    .to_dict()
)
```
