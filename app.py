import os 
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify(message = 'Hello, World!')

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(host = '0.0.0.0', port = port)

