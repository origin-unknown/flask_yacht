from ..models import User

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
    fresh_jwt_required,
    jwt_optional,
    jwt_required,
    jwt_refresh_token_required
)
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


blueprint = Blueprint(
    'api.auth',
    __name__,
    url_prefix='/api/auth'
)

# @blueprint.route('/')
# def index():
#     return jsonify({ 'message': 'Welcome to Yacht API.'})


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
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        data = {
            'access_token': create_access_token(identity=user.username),
            'refresh_token': create_refresh_token(identity=user.username)
        }
        return jsonify(data), 200
    return abort(401)

@blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    '''curl -H "Authorization: Bearer $REFRESH" -X POST http://127.0.0.1:5000/api/refresh'''
    current_user = get_jwt_identity()
    data = { 'access_token': create_access_token(identity=current_user) }
    return jsonify(data), 200

@blueprint.route('/secure')
@jwt_required
def secure():
    '''curl -H "Authorization: Bearer $ACCESS_TOKEN" http://127.0.0.1:5000/api/secure'''
    current_user = get_jwt_identity()
    return jsonify(logged_as=current_user), 200

@blueprint.route('/secure-opt')
@jwt_optional
def secure_opt():
    '''curl http://127.0.0.1:5000/api/secure-opt'''
    current_user = get_jwt_identity()
    if current_user: return jsonify(identity=current_user), 200
    return jsonify(identity='anonymous'), 200
