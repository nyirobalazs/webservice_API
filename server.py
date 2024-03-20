from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
print(getenv(DATABASE_URL))


