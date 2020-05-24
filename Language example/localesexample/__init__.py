from flask import Flask
from localesexample.config import Config
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config.from_object(Config)
import localesexample.routes