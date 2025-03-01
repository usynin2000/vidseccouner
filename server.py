from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    logger.info(f"[LOG] Event: {data}")
    return "Received", 200

@app.route('/wallet-connect', methods=['POST'])
def wallet_connect():
    data = request.get_json()
    wallet = data.get("wallet")
    if wallet:
        logger.info(f"[WALLET] Connected: {wallet}")
        return {"message": "Wallet connection logged"}, 200
    else:
        logger.warning("[WALLET] No wallet address provided")
        return {"error": "No wallet address provided"}, 400

@app.route("/withdraw", methods=['POST'])
def withdraw_tokens():
    logger.info(f"Starting to withdraw tokens:")
    data = request.get_json()
    logger.info(f"amount = {data['time']}")
    logger.info("All done")
    return "All done", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
