from flask import request, jsonify
from extensions import db
from .models import Agent

def init_routes(app):
    @app.route('/agents', methods=['GET'])
    def get_agents():
        agents = Agent.query.all()
        return jsonify([{"id": agent.id, "name": agent.name, "ip": agent.ip} for agent in agents])

    @app.route('/agents', methods=['POST'])
    def add_agent():
        data = request.json
        new_agent = Agent(name=data['name'], ip=data['ip'])
        db.session.add(new_agent)
        db.session.commit()
        return jsonify({"id": new_agent.id, "name": new_agent.name, "ip": new_agent.ip}), 201

    @app.route('/agents/<int:id>', methods=['PUT'])
    def update_agent(id):
        data = request.json
        agent = Agent.query.get_or_404(id)
        agent.name = data.get('name', agent.name)
        agent.ip = data.get('ip', agent.ip)
        db.session.commit()
        return jsonify({"id": agent.id, "name": agent.name, "ip": agent.ip})

    @app.route('/agents/<int:id>', methods=['DELETE'])
    def delete_agent(id):
        agent = Agent.query.get_or_404(id)
        db.session.delete(agent)
        db.session.commit()
        return jsonify({"message": "Agent deleted successfully"}), 200
