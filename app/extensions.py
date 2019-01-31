from flask_jwt_extended import JWTManager
from peewee import MySQLDatabase

db: MySQLDatabase = None
jwt = JWTManager()
