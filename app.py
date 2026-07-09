# app.py
from flask import Flask, jsonify
import os
import socket
from datetime import datetime
import psutil
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({
        "message": "SRE Demo App is running!",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "version": "1.0.0"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "code": 200}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness check endpoint"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        
        if cpu_percent > 90 or memory_info.percent > 90:
            return jsonify({"status": "not_ready", "reason": "High resource usage"}), 503
        
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Application metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        return jsonify({
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
            "memory_available_mb": memory_info.available / (1024 * 1024),
            "disk_percent": disk_info.percent,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/info', methods=['GET'])
def info():
    """System information"""
    return jsonify({
        "hostname": socket.gethostname(),
        "platform": os.uname().sysname,
        "cpu_count": os.cpu_count(),
        "pid": os.getpid()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
