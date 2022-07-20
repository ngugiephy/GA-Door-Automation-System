from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

db.drop_all()
db.create_all()

@app.route('/')
@app.route('/home')
def home_page():
    button_data = db.session.query(Communication).all()
    column_headings = Communication.__table__.columns.keys()
    return render_template('index.html', column_headings=column_headings, button_data=button_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
