
from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)

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
