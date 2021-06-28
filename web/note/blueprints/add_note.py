from flask import Blueprint, request
from web.extensions import login_check, make_json_response
from web.model import Note
add_note_bp = Blueprint("add_note",__name__,url_prefix='/note')


@add_note_bp.route('', methods=["POST"])
@login_check
def add_note(id):
    text = request.form.get('text')  # headers带token text放在表单内
    if len(text) <= 7:
        return make_json_response(
            status=1,
            message="ToShort",
            data=None,
        )
    user_id = id
    if Note.add(user_id=user_id, body=text):
        return make_json_response(
            status=1,
            message="Succeed",
            data=None
        )
    else:
        return make_json_response(
            status=0,
            message="OddWrong",
            data="I'm sorry for this wrong"
        )