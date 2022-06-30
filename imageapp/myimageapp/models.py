from myimageapp import db, login_manager, bcrypt
import datetime
from datetime import timedelta
from flask_login import UserMixin

# --
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# --
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)

    # will add hashing functionality later
    @property
    def password(self):
        return self.password

    @password.setter # This setter when called will store the password provided as encrypted
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # this function will check if password provided matches the one in db
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    image_name = db.Column(db.String(50), nullable=False)