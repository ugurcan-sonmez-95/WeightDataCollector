from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from email_system import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
### Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://username:password@localhost/database_name'
db = SQLAlchemy(app)

### Database table
class Data(db.Model):

    __tablename__ = "email_weight_data"
    id = db.Column(db.Integer, primary_key=True)
    email_col = db.Column(db.String(100), unique=True)
    weight_col = db.Column(db.Integer)

    def __init__(self, email_col, weight_col):
        self.email_col = email_col
        self.weight_col = weight_col

### Routes to home page and result page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['post'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        weight = request.form["weight_name"]
        if db.session.query(Data).filter(Data.email_col == email).count() == 0:
            data = Data(email, weight)
            db.session.add(data)
            db.session.commit()
            avg_weight = db.session.query(func.avg(Data.weight_col)).scalar()
            avg_weight = round(avg_weight, 1)
            count = db.session.query(Data.weight_col).count()
            send_email(email, weight, avg_weight, count)
            return render_template("success.html")
    return render_template("index.html", text="The e-mail you entered already exists!")

if __name__ == '__main__':
    #app.debug = True
    app.run()