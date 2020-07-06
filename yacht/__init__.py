#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
from flask import Flask
from flask import (
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(env=os.getenv('FLASK_ENV', 'production')):
    app = Flask(__name__,
        instance_relative_config=True,
    )
    app.config.from_mapping(
        SECRET_KEY=b'\x09|\t\xe8V\xdb\x974{\x1aZz\xe9G\xea\x95\\xd6\xfa\xcf`\x7f\\*\n',
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.instance_path, f'{env}.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    register_endpoints(app)

    return app

def register_blueprints(app):
    from .api.auth import create_module as api_auth_create_module
    from .api.main import create_module as api_main_create_module
    from .api.docker.templates import create_module as api_docker_templates_create_module
    api_auth_create_module(app, url_prefix='/api')
    api_main_create_module(app, url_prefix='/api')
    api_docker_templates_create_module(app, url_prefix='/api/templates')

def register_endpoints(app):
    @app.route('/')
    def index():
        return '<center><a href="http://127.0.0.1:8080/">Vue-Yacht</a></center><iframe src="http://127.0.0.1:8080/" style="display: block; background: #000; border: none; height: 100vh; width: 100vw;"></iframe>'
