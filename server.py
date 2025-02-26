from flask import Flask, request
from config import PRIVATE_KEY

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    logger.info(f"Request: {data}")
    return "Received", 200


@app.route("/withdraw", methods=['POST'])
def withdraw_tokens():
    logger.info(f"Starting to withdraw tokens:")
    data = request.get_json()
    ### cost of 1 second multipy for time was consumed
    logger.info(f"amount = {data['time']}")

    logger.info("All done}")
    return "All done", 200





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
