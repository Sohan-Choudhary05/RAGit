from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy import Column,String,Integer,Text

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app,db)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database Created!")

@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("Database dropped successfully")

# =====================================
# ✅ RAG API ROUTES
# =====================================



import routes