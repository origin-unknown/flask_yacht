from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_module(app, **kwargs):
    from ..errors import register_errorhandlers
    from .views import blueprint

    jwt.init_app(app)

    register_errorhandlers(blueprint)
    app.register_blueprint(blueprint, **kwargs)
