
from ... import ma
from marshmallow.validate import (
    Length
)

class TemplateItemSchema(ma.SQLAlchemySchema):
    id = ma.Int(
        dump_only=True)

    template_id=ma.Int(
        required=True)
    type = ma.Int()
    title = ma.Str(
        validate=Length(min=1, max=255))
    platform = ma.Str(
        validate=Length(min=1, max=255))
    description = ma.Str()
    name = ma.Str(
        validate=Length(min=1, max=255))
    logo = ma.Str(
        validate=Length(min=1, max=255))
    notes = ma.Str()
    categories = ma.List(ma.Str())
    # configuration data
    restart_policy = ma.Str()
    ports = ma.Raw()
    volumes = ma.Raw()
    env = ma.Raw()


class TemplateSchema(ma.SQLAlchemySchema):
    # perhapse use auto_field
    id = ma.Int(
        dump_only=True)
    created_at = ma.DateTime(
        dump_only=True)
    updated_at = ma.DateTime(
        dump_only=True)
    title = ma.Str(
        required=True,
        validate=Length(min=1, max=255))
    url = ma.Url(
        required=True)
    items = ma.Nested(
        TemplateItemSchema, many=True,
        exclude=('template_id','restart_policy','ports','volumes','env'))
