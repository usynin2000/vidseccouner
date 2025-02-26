from web3 import Web3
from config import INFURA_API_KEY, PRIVATE_KEY
from datetime import datetime


def collect_fee():
    # === 1) Подключаемся к Sepolia через Infura ===
    w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))
    account = w3.eth.account.from_key(PRIVATE_KEY)
    account_address = account.address

    print(f"Connected to Sepolia as: {account_address}")

    # === 2) Адреса контрактов ===
    SUB_TOKEN_ADDRESS = "0xCd33e6504dB957dcC70E99305CBa5a655Fa0c3Df"
    SUBSCRIPTION_CONTRACT_ADDRESS = "0xD01E201b6815918eaB868dc17Fd69a599A028678"

    # === 3) ABI контрактов ===
    SUBSCRIPTION_ABI = [
        {"inputs":[{"internalType":"address","name":"subscriber","type":"address"}],
         "name":"collectFee","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address","name":"","type":"address"}],
         "name":"subscriptionEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
         "stateMutability":"view","type":"function"}
    ]

    SUB_TOKEN_ABI = [
        {"inputs":[{"internalType":"address","name":"owner","type":"address"},
                   {"internalType":"address","name":"spender","type":"address"}],
         "name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
         "stateMutability":"view","type":"function"},
        {"inputs":[{"internalType":"address","name":"","type":"address"}],
         "name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
         "stateMutability":"view","type":"function"}
    ]

    # === 4) Инициализация контрактов ===
    subscription_contract = w3.eth.contract(address=SUBSCRIPTION_CONTRACT_ADDRESS, abi=SUBSCRIPTION_ABI)
    sub_token = w3.eth.contract(address=SUB_TOKEN_ADDRESS, abi=SUB_TOKEN_ABI)

    # === 5) Кого будем списывать? ===
    user_address = "0x7666B64D68705F52A6786C047E200a74c212A526"  # Тот, кто дал approve

    # === 6) Проверяем подписку пользователя ===
    sub_end = subscription_contract.functions.subscriptionEnd(user_address).call()
    if sub_end == 0:
        print(f"❌ User {user_address} is NOT subscribed!")
        exit(1)

    sub_end_date = datetime.utcfromtimestamp(sub_end).strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ User {user_address} has an active subscription until {sub_end_date}")

    # === 7) Проверяем баланс перед списанием ===
    balance_before = sub_token.functions.balanceOf(user_address).call()
    allowance = sub_token.functions.allowance(user_address, SUBSCRIPTION_CONTRACT_ADDRESS).call()

    print(f"💰 User balance: {Web3.from_wei(balance_before, 'ether')} SUB")
    print(f"🔓 Approved allowance: {Web3.from_wei(allowance, 'ether')} SUB")

    if allowance == 0:
        print(f"❌ ERROR: User has no approved tokens for {SUBSCRIPTION_CONTRACT_ADDRESS}!")
        exit(1)

    # === 8) Вызываем collectFee ===
    print(f"⏳ Calling collectFee({user_address}) ...")

    nonce = w3.eth.get_transaction_count(account_address)
    tx = subscription_contract.functions.collectFee(user_address).build_transaction({
        "chainId": 11155111,  # Sepolia
        "gasPrice": w3.eth.gas_price,
        "gas": 3000000,
        "from": account_address,
        "nonce": nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Transaction sent: {tx_hash.hex()}")

    # Ждем подтверждения
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Transaction mined! Block: {tx_receipt.blockNumber}")

    # === 9) Проверяем баланс после списания ===
    balance_after = sub_token.functions.balanceOf(user_address).call()
    print(f"💰 New user balance: {Web3.from_wei(balance_after, 'ether')} SUB")

    print("\n✅ Fee successfully collected!")

if __name__ == "__main__":
    collect_fee()
