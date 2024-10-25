# __init__.py
from flask import Blueprint
from .match_routes import match_routes


# Register all route blueprints
def register_routes(app):
    app.register_blueprint(match_routes)
