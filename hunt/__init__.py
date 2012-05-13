

from flask import Flask

from hunt.extensions import db
from hunt.views import frontend, account, job


DEFAULT_APP_NAME = 'hunt'

DEFAULT_MODULES = (
    (frontend, ''),
    (account, '/account'),
    (job, '/job'),
)


def create_app(configure=None, modules=None):
    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(DEFAULT_APP_NAME)
    app.config.from_pyfile(configure)

    configure_extensions(app)
    configure_modules(app, modules)
    return app



def configure_extensions(app):
    db.init_app(app)


def configure_modules(app, modules):
    
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

