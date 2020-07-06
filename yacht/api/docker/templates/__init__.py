
def create_module(app, **kwargs):
    from ..errors import register_errorhandlers
    from .views import blueprint
    register_errorhandlers(blueprint)
    app.register_blueprint(blueprint, **kwargs)
