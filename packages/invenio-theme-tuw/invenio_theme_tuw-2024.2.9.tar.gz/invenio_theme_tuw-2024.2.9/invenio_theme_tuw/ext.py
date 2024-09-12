# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing the theme for TU Wien."""


from flask_session_captcha import FlaskSessionCaptcha

from . import config
from .views import create_blueprint


def override_bp_order(app):
    """Rearrange the order of registered blueprints.

    This ensures that jinja templates are loaded from Theme-TUW rather than other
    modules, which enables overriding of core templates (cf. `flask.render_template()`).
    This operation needs to be performed after all the blueprints have been registered.
    """
    bps = {}
    theme_tuw_bp = None
    for name, bp in app.blueprints.items():
        if name == "invenio_theme_tuw":
            theme_tuw_bp = bp
        else:
            bps[name] = bp

    app.blueprints = {"invenio_theme_tuw": theme_tuw_bp, **bps}


class InvenioThemeTUW:
    """Invenio-Theme-TUW extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_blueprint(app)
        self.init_captcha_extension(app)
        app.extensions["invenio-theme-tuw"] = self

    def init_captcha_extension(self, app):
        """Initialize the Flask-Session-Captcha extension."""
        self.captcha = FlaskSessionCaptcha()
        app.extensions["flask-session-captcha"] = self.captcha

        try:
            self.captcha.init_app(app)
        except RuntimeWarning as w:
            app.logger.warn(w)

    def init_blueprint(self, app):
        """Initialize blueprint."""
        self.blueprint = blueprint = create_blueprint(app)
        app.register_blueprint(blueprint)

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            app.config.setdefault(k, getattr(config, k))
