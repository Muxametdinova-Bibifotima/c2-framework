from extensions import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Agent {self.name}>'
