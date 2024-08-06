import os 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)

