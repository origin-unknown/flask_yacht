
from ... import ma

class TemplateSchema(ma.SQLAlchemySchema):
    # perhapse use auto_field
    id = ma.Int(dump_only=True)
    title = ma.Str()
    url = ma.Url()
