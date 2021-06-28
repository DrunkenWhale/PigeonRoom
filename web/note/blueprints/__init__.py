from .add_note import add_note_bp
from .get_note import get_note_bp


def note_register_blueprints(app):
    app.register_blueprint(add_note_bp)
    app.register_blueprint(get_note_bp)
