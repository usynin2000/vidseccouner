from flask import Flask, request
from transfer import transfer_token
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
    amount = 100000000000000000000 * float(data['time'])
    logger.info(f"amount = {amount}")

    res = transfer_token(
        contract_address="0x40d87A3c7003A5A2dDA819721F998757fFcb65a8",
        from_address=data['from'],
        to_address="0x17dD57eaaF89aa437af2eE84Bd38c40AC99Ab7b2",
        amount=int(amount),
        private_key=PRIVATE_KEY
    )
    logger.info(f"All done {res["status"]}")
    return "All done", 200





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
