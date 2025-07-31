from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from dotenv import load_dotenv
import cloudinary

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

# 👇 IMPORTANT: This variable must be named `app`
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)

cloudinary.config(
    cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
    api_key=app.config['CLOUDINARY_API_KEY'],
    api_secret=app.config['CLOUDINARY_API_SECRET']
)

from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager.login_view = 'main.login'

from app.routes import init_routes
app.register_blueprint(init_routes)

