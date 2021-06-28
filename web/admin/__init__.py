"""

⑧多说了
特权就完事了
爷就是要自己写

"""
from .get_data_from_db import get_data_from_db_bp


def admin_register_blueprints(app):
    app.register_blueprint(get_data_from_db_bp)
