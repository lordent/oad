import marshmallow
import copy


FIELD_MAPPING = {
    marshmallow.fields.Integer: ('integer', 'int64'),
    marshmallow.fields.Number: ('number', None),
    marshmallow.fields.Float: ('number', 'float'),
    marshmallow.fields.Decimal: ('double', None),
    marshmallow.fields.String: ('string', None),
    marshmallow.fields.Boolean: ('boolean', None),
    marshmallow.fields.UUID: ('string', 'uuid'),
    marshmallow.fields.DateTime: ('string', 'date-time'),
    marshmallow.fields.Date: ('string', 'date'),
    marshmallow.fields.Time: ('string', None),
    marshmallow.fields.Email: ('string', 'email'),
    marshmallow.fields.URL: ('string', 'url'),
    marshmallow.fields.Dict: ('object', None),
    # Assume base Field and Raw are strings
    marshmallow.fields.Field: ('string', None),
    marshmallow.fields.Raw: ('string', None),
    marshmallow.fields.List: ('array', None),
}


def schema_to_dict(schema: marshmallow.Schema):
    """
    required:
        - id
        - name
    properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        tag:
          type: string
    :param schema:
    :param relations:
    """
    required = list()
    properties = dict()

    if hasattr(schema, 'fields'):
        fields = schema.fields
    elif hasattr(schema, '_declared_fields'):
        fields = copy.deepcopy(schema._declared_fields)
    else:
        raise ValueError(
            "{0!r} doesn't have either `fields` or `_declared_fields`".format(schema)
        )

    exclude_fields = getattr(getattr(schema, 'Meta', None), 'exclude', [])
    dump_only_fields = getattr(getattr(schema, 'Meta', None), 'dump_only', [])

    for field_name, field_obj in fields.items():
        if (
            field_name in exclude_fields
            or field_obj.dump_only
            or field_name in dump_only_fields
        ):
            continue

        meta = field_obj.metadata.get('openapi', dict())

        properties[field_name] = {}

        if 'description' in meta:
            properties[field_name]['description'] = meta['description']

        if 'deprecated' in meta:
            properties[field_name]['deprecated'] = meta['deprecated']

        if field_obj.required:
            required.append(field_name)

        if isinstance(field_obj, marshmallow.fields.Nested):
            ref = schema_to_dict(field_obj.nested)

            if field_obj.many:
                properties[field_name].update(**{
                    'type': 'array',
                    'items': ref,
                })
            else:
                properties[field_name].update(**ref)

            continue

        if isinstance(field_obj, marshmallow.fields.List):
            type_, format_ = FIELD_MAPPING.get(
                type(field_obj.container), ('string', None))

            properties[field_name].update(**{
                'type': 'array',
                'items': {
                    'type': type_,
                    'format': meta.get('format', '') or format_,
                },
            })

            continue

        type_, format_ = FIELD_MAPPING.get(type(field_obj), ('string', None))

        properties[field_name].update(**{
            'type': type_,
            'format': meta.get('format', '') or format_,
        })

    return dict(required=required, properties=properties)


def schema_to_ref(schema: marshmallow.Schema):
    ref = {
        '$ref': '#/components/schemas/%s' %
                schema.__class__.__name__,
    }
    if schema.many:
        return {'type': 'array', 'items': ref}
    return ref
