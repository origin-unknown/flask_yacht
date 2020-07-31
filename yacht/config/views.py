from .. import db
from ..api.models import User
from .schemes import ConfigSchema

import base64, os
from flask import Blueprint
from flask import (
    current_app,
    redirect,
    render_template,
    request,
    url_for
)
from functools import wraps
from webargs.flaskparser import use_kwargs


def not_configured(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # TODO: better use '/' instead of url_for here
        if current_app.config.get('CONFIGURED', False):
            return redirect(url_for('index'), code=303)
        return f(*args, **kwargs)
    return wrapper


blueprint = Blueprint(
    'config',
    __name__,
    url_prefix='/config'
)

@blueprint.route('/')
@not_configured
def index():
    return render_template('config/index.html')

# ---
# curl -d "username=user&password=pass&confirm=pass" -X POST http://localhost:5000/config/setup

@blueprint.route("/setup", methods=['POST'])
@use_kwargs(ConfigSchema(), location='form')
@not_configured
def setup(username, password, confirm):

    # dev only
    # user = User.query.filter_by(username=username).first()
    # db.session.delete(user)
    # db.session.commit()
    # end only dev

    cfg_data = {
        'CONFIGURED': True,
        'SECRET_KEY': base64.b64encode(os.urandom(64)),
    }

    # Write configuration here and create a root user.
    # Should be a POST request and redirect to index or login.
    conf_path = os.path.join(current_app.instance_path, 'base.cfg')
    with open(conf_path, 'w') as fd:
        for k,v in cfg_data.items():
            fd.write(f'{k}={v!r}\r\n')

    user = User(
        username=username,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    current_app.config.from_pyfile(conf_path, silent=True)

    return redirect(url_for('index'))
