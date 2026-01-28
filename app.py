from flask import Flask
from extensions import db
from server.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agents.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # SQLAlchemy ni Flask ilovasi bilan bog'lash
    db.init_app(app)
    
    # API endpointlarini qo'shish
    init_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Database tuzilmalarini yaratish
    app.run(debug=True, port=5001)
