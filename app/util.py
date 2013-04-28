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

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d
