from web.static_html.blueprints.static_html import static_html_bp


def static_html_register_blueprints(app):
    app.register_blueprint(static_html_bp)