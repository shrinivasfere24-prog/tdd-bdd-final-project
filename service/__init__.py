"""Product Catalog Service."""

from flask import Flask
from service.models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TESTING"] = True
app.config["SQLALCHEMY_SESSION_OPTIONS"] = {
    "expire_on_commit": False
}
db.init_app(app)

with app.app_context():
    db.create_all()

from service import routes  # noqa: E402,F401
