
from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
    jwt_optional
)
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


blueprint = Blueprint(
    'api.main',
    __name__,
    url_prefix='/api/main'
)

@blueprint.route('/')
def index():
    return jsonify({ 'message': 'Hello API.'})

@blueprint.route('/sample')
def sample():
    return jsonify({ 'message': 'Hello from Flask API.'})


@blueprint.route('/login', methods=['POST'])
@use_kwargs(
    {
        'username': fields.Str(required=True),
        'password': fields.Str(required=True),
    },
    location='json'
)
def login(username, password):
    '''curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"user", "password":"pass"}' http://127.0.0.1:5000/api/login'''

    if username != 'user' or password != 'pass':
        # TODO Must go shorter!
        abort(401, 'Invalid authentication credentials',
            make_response(jsonify(message='Invalid authentication credentials'), 401))

    acc_token = create_access_token(identity=username, fresh=True)
    ref_token = create_refresh_token(identity=username)

    # TODO Store the tokens to database

    return jsonify({'access_token': acc_token, 'refresh_token': ref_token}), 200