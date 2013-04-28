from app.people.models import Person
from app.util import to_json
from app import app, login_manager, db
from flask import Blueprint, request, Response, flash, jsonify, session, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user

mod = Blueprint('api', __name__, url_prefix="/api")

@login_required
@mod.route("/people/managed_by_current_user")
def get_people_managed_by_current_user():
    current_person_id = current_user.person.id
    people = Person.query.filter(Person.managed_by_id == current_person_id).all()
    people = [to_json(p, Person) for p in people]
    return jsonify(results=people)
