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


class User(flask_login.UserMixin, db.Model, DBClass):
    __tablename__ = "user"
    id = db.Column(db.String(400), primary_key=True)
    pw_hash = db.Column(db.String(400))
    budget = db.Column(db.Float)
    used_budget = db.Column(db.Float)
    api_key = db.Column(db.String(400))

    def __repr__(self):
        return f"<User id={self.id}, budget={self.budget}, used_budget={self.used_budget}>"
    
    
class LanguageModel(flask_login.UserMixin, db.Model, DBClass):
    __tablename__ = "model"
    name = db.Column(db.String(400), primary_key=True)
    encoding_model = db.Column(db.String(400))
    provider = db.Column(db.String(400))
    price_input_token = db.Column(db.Float)
    price_output_token = db.Column(db.Float)

    def __repr__(self):
        return f"<LanguageModel name={self.name}, encoding_model={self.encoding_model}, provider={self.provider}>"
    

