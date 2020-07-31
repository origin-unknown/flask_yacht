from .. import ma
from marshmallow import validates_schema, ValidationError
from marshmallow import fields, validate

class ConfigSchema(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(
        required=True,
        validate=validate.Length(min=4)
    )
    confirm = ma.Str(
        required=True,
        validate=(
            validate.Length(min=4),
        )
    )
    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data['password'] != data['confirm']:
            raise ValidationError("Passwords must match")
