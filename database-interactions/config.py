import os
import dotenv

dotenv.load_dotenv(".env")

SECRET_KEY = os.environ["SECRET_KEY"]
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
