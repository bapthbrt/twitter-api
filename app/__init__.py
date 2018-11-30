from flask import Flask
from flask_login import LoginManager
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.models import User

    @login_manager.request_loader
    def load_user_from_header(request):
        if request.headers.get('Authorization'):
            header_val = request.headers.get('Authorization').replace('Bearer ', '', 1)
            return db.session.query(User).filter_by(api_key=header_val).first()
        return None

    @app.route('/hello')
    def hello():
        return "Goodbye World!"

    from .apis.tweets import api as tweets
    from .apis.users import api as users
    api = Api()
    api.add_namespace(tweets)
    api.add_namespace(users)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
