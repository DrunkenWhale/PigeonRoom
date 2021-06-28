from flask import Blueprint, request
from web.extensions import login_check, make_json_response
from web.model import Note

get_note_bp = Blueprint("get_note", __name__, url_prefix='/note')


@get_note_bp.route('/', methods=["GET"])
@login_check
def get_note(id):
    user_id = id
    return make_json_response(
        status=1,
        message="Succeed",
        data=[{"time": i.time, "text": i.body} for i in Note.get_all(user_id=user_id)]
    )
