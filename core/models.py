import logging
import flask_login

from core import db


class DBClass:
    def save(self):
        db.session.add(self)
        db.session.commit()
        logging.info("Successfully saved %r", self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        logging.info("Successfully deleted %r", self)


# Beispiel Userklasse, muss entsprechend angepasst werden
class User(flask_login.UserMixin, db.Model, DBClass):
    __tablename__ = "user"
    id = db.Column(db.String(200), primary_key=True)
    pw_hash = db.Column(db.String(200))


    def __repr__(self):
        return f"<User id={self.id} >"