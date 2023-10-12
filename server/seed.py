from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Cake_Bakeries, Cake_Bakeries, Bakeries

with app.app_context():
    pass