cdfrom flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "ATLES Demo Server is running! "

if __name__ == '__main__':
    print(" ATLES Demo Server starting...")
    app.run(host='0.0.0.0', port=5000, debug=True)
