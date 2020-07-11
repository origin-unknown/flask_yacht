import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

import flask_migrate

import pytest
from yacht import create_app
from yacht import db as _db

@pytest.fixture
def app():
    app = create_app('testing')
    app.testing = True
    # with app.app_context():
    #     flask_migrate.upgrade()
    yield app
    # os.remove(os.path.join(app.instance_path, 'testing.sqlite'))

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db(app, request):
    with app.app_context():
        _db.app = app
        _db.create_all()
        yield _db
        _db.drop_all()
