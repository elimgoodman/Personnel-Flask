from app.people.models import Person

from flask import render_template
from flask_login import current_user

def common_render(tmpl_name, **kwargs):

    #TODO: this is a prime candidate for caching
    if not current_user.is_anonymous():
        current_person_id = current_user.person.id
        people = Person.query.filter(Person.managed_by_id == current_person_id).all()
    else:
        people = []

    common_args = {
        "user": current_user,
        #"config": app.config,
        "people": people
    }

    kwargs.update(common_args)
    return render_template(tmpl_name, **kwargs)

