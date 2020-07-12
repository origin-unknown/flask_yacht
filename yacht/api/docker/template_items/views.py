from .... import db
from ...models import (
    TemplateItem
)
from ...schemes import (
    TemplateItemSchema,
    DeploySchema
)
from ..utils import conv_ports2dict

from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    jwt_required,
    jwt_optional
)
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


blueprint = Blueprint(
    'api.docker.template_items',
    __name__,
    url_prefix='/api/docker/template_items'
)


# endpoint: index
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@blueprint.route('/')
# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def index():
    template_items = TemplateItem.query.order_by(TemplateItem.title).all()
    template_items_schema = TemplateItemSchema(many=True)
    data = template_items_schema.dump(template_items, many=True)
    return jsonify({ 'data': data })

# endpoint: show
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@blueprint.route('/<int:id>')
def show(id):
    try:
        template_item = TemplateItem.query.get_or_404(id)
        template_item_schema = TemplateItemSchema()
        data = template_item_schema.dump(template_item)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

# ---

from webargs import fields, validate

@blueprint.route('/<int:id>/deploy', methods=['POST'])
@use_args(DeploySchema(), location='json')
def deploy(args, id):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"title":"Untitled", "image":"my:image", "ports":[{"proto": "tcp", "hport":2020}]}' \
    http://127.0.0.1:5000/api/apps/1/deploy
    '''
    print(args, id)
    # print(id, title, image)
    # print(args, kwargs)
    return jsonify(data = '')
