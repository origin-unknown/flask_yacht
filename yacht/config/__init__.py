
import os
from flask import (
    current_app,
    redirect,
    request,
    url_for
)

def before_request():
    # Check whether the application has already been configured.
    cfg_available = current_app.config.get('CONFIGURED', False)
    cfg_endpoints = ('config.index', 'config.setup', 'static')
    if not cfg_available and request.endpoint not in cfg_endpoints:
        return redirect(url_for('config.index'))

def create_module(app, **kwargs):
    from .views import blueprint
    app.config.from_pyfile(os.path.join(app.instance_path, 'base.cfg'), silent=True)
    if not app.config.get('CONFIGURED', False):
        app.before_request(before_request)
        app.register_blueprint(blueprint, **kwargs)
