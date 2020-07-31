#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
from flask import Flask
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for
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
        static_folder = "./dist/static",
        template_folder = "./dist/templates"
    )
    app.config.from_mapping(
        SECRET_KEY=b'\x09|\t\xe8V\xdb\x974{\x1aZz\xe9G\xea\x95\\xd6\xfa\xcf`\x7f\\*\n',
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(app.instance_path, f'{env}.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # JWT_ACCESS_TOKEN_EXPIRES=10
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
    from .config import create_module as config_create_module
    config_create_module(app)

    from .api.auth import create_module as api_auth_create_module
    from .api.main import create_module as api_main_create_module
    from .api.docker.templates import create_module as api_docker_templates_create_module
    from .api.docker.template_items import create_module as api_docker_template_items_create_module
    api_auth_create_module(app, url_prefix='/api')
    api_main_create_module(app, url_prefix='/api')
    api_docker_templates_create_module(app, url_prefix='/api/templates')
    api_docker_template_items_create_module(app, url_prefix='/api/apps')

def register_endpoints(app):
    @app.route('/')
    def index():
        return render_template('index.html')
