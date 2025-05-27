from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config


import markdown
from flask import Markup

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    mongo.init_app(app)
    login_manager.init_app(app)
    
    from app.auth.routes import auth
    from app.ai.routes import ai
    from app.tracker.routes import tracker
    from app.dashboard.routes import dashboard
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(ai, url_prefix='/ai')
    app.register_blueprint(tracker, url_prefix='/tracker')
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    app.jinja_env.filters['markdown'] = lambda text: Markup(markdown.markdown(text))
    
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app