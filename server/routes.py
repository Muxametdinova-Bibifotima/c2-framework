from flask import request, jsonify
from extensions import db
from server.models import Agent

def init_routes(app):
    @app.route('/agents', methods=['GET', 'POST'])
    def handle_agents():
        if request.method == 'GET':
            agents = Agent.query.all()
            return jsonify([{"id": agent.id, "name": agent.name, "ip": agent.ip} for agent in agents])
        elif request.method == 'POST':
            data = request.json
            new_agent = Agent(name=data['name'], ip=data['ip'])
            db.session.add(new_agent)
            db.session.commit()
            return jsonify({"id": new_agent.id, "name": new_agent.name, "ip": new_agent.ip}), 201

    @app.route('/agents/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_agent(id):
        agent = Agent.query.get_or_404(id)
        
        if request.method == 'GET':
            return jsonify({"id": agent.id, "name": agent.name, "ip": agent.ip})
        
        elif request.method == 'PUT':
            data = request.json
            agent.name = data.get('name', agent.name)
            agent.ip = data.get('ip', agent.ip)
            db.session.commit()
            return jsonify({"id": agent.id, "name": agent.name, "ip": agent.ip})
        
        elif request.method == 'DELETE':
            db.session.delete(agent)
            db.session.commit()
            return jsonify({"message": "Agent deleted successfully"}), 200

    @app.route('/agents/search', methods=['GET'])
    def search_agents():
        name = request.args.get('name', '')
        ip = request.args.get('ip', '')
        
        query = Agent.query
        if name:
            query = query.filter(Agent.name.ilike(f'%{name}%'))
        if ip:
            query = query.filter(Agent.ip.ilike(f'%{ip}%'))
            
        agents = query.all()
        return jsonify([{"id": agent.id, "name": agent.name, "ip": agent.ip} for agent in agents])
