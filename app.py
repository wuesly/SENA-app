from flask import Flask
from mongoengine import connect  # 
from flask_login import LoginManager
from config import Config
from flask_login import login_manager
from models import Instructor 

login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Instructor.objects(id=user_id).first()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Conexión directa con MongoDB local usando mongoengine puro
    connect(
        db=app.config['MONGODB_SETTINGS']['db'],
        host=app.config['MONGODB_SETTINGS']['host'],
        port=app.config['MONGODB_SETTINGS']['port']
    )

    login_manager.init_app(app)

    from routes import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=3000, host="0.0.0.0", debug=True)

