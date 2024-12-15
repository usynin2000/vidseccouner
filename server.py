from flask import Flask, request

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    logger.info(f"Request: {data}")
    return "Received", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
