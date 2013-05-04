from app.people.models import Person, Note, Feedback
from app.util import to_json
from app import app, login_manager, db
from flask import Blueprint, request, Response, flash, jsonify, session, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user

mod = Blueprint('api', __name__, url_prefix="/api")

@login_required
@mod.route("/notes", methods=["PUT"])
def update_note():
    current_person_id = current_user.person.id
    note = Note.query.filter(Note.id == request.json['id']).one()
    
    note.is_pinned = request.json['is_pinned']
    db.session.add(note)
    db.session.commit()

    return jsonify(success=True)

@login_required
@mod.route("/feedback", methods=["PUT"])
def update_note():
    feedback = Feedback.query.filter(Feedback.id == request.json['id']).one()
    
    feedback.has_communicated = request.json['has_communicated']
    db.session.add(feedback)
    db.session.commit()

    return jsonify(success=True)
