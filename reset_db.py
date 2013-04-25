#!/usr/bin/env python
from app import db
from app.users.models import User
from app.people.models import Person

db.drop_all()
db.create_all()

u = User("a@c.com", "tytych")
db.session.add(u)
db.session.commit()

u = User("a@b.com", "tytych")
db.session.add(u)
db.session.commit()

p = Person(u.id, "Eli", "Goodman")
db.session.add(p)
db.session.commit()

p = Person(None, "Sally", "Foobar", p.id)
db.session.add(p)
db.session.commit()

p = Person(None, "Billy", "Foobar", p.id)
db.session.add(p)
db.session.commit()
