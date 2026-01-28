from flask import Flask
from flask_jwt_extended import JWTManager
from extensions import db
from server.routes import init_routes
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'agents.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # JWT uchun maxfiy kalit
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
