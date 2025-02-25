from solcx import compile_standard, install_solc
import json
from web3 import Web3
from config import INFURA_API_KEY, PRIVATE_KEY

# 1) Устанавливаем версию компилятора (при первом запуске)
install_solc("0.8.0")

# 2) Считываем исходники
with open("SubToken.sol", "r", encoding="utf-8") as f:
    subtoken_source = f.read()

with open("SubscriptionContract.sol", "r", encoding="utf-8") as f:
    subscription_source = f.read()

# 3) Компилируем
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SubToken.sol": {
                "content": subtoken_source
            },
            "SubscriptionContract.sol": {
                "content": subscription_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            },
        },
    },
    solc_version="0.8.0",
)

# 4) Сохраняем результат в файл, чтобы было удобнее смотреть
with open("compiled.json", "w", encoding="utf-8") as f:
    json.dump(compiled_sol, f, ensure_ascii=False, indent=4)

# 5) Достаём ABI и Bytecode для SubToken
subtoken_abi = compiled_sol["contracts"]["SubToken.sol"]["SubToken"]["abi"]
subtoken_bytecode = compiled_sol["contracts"]["SubToken.sol"]["SubToken"]["evm"]["bytecode"]["object"]

# 6) Достаём ABI и Bytecode для SubscriptionContract
subscription_abi = compiled_sol["contracts"]["SubscriptionContract.sol"]["SubscriptionContract"]["abi"]
subscription_bytecode = compiled_sol["contracts"]["SubscriptionContract.sol"]["SubscriptionContract"]["evm"]["bytecode"]["object"]

# 7) Подключаемся к сети (Sepolia) через Infura
w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))

# 8) Готовим аккаунт
account = w3.eth.account.from_key(PRIVATE_KEY)
account_address = account.address

print("Using account:", account_address, "on chainId:", w3.eth.chain_id)

# 9) Деплоим SubToken
print("\nDeploying SubToken...")

nonce = w3.eth.get_transaction_count(account_address)

SubTokenContract = w3.eth.contract(abi=subtoken_abi, bytecode=subtoken_bytecode)

tx_deploy_subtoken = SubTokenContract.constructor().build_transaction({
    "chainId": w3.eth.chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": account_address,
    "nonce": nonce
})

signed_subtoken = account.sign_transaction(tx_deploy_subtoken)
tx_hash_subtoken = w3.eth.send_raw_transaction(signed_subtoken.raw_transaction)
print("SubToken deploy tx sent:", tx_hash_subtoken.hex())

tx_receipt_subtoken = w3.eth.wait_for_transaction_receipt(tx_hash_subtoken)
subtoken_address = tx_receipt_subtoken.contractAddress

print("SubToken deployed at:", subtoken_address)


# 10) Деплоим SubscriptionContract (передаём адрес токена и желаемый fee)
#     Допустим, feePerPeriod = 10 * 10^18 (10 SUB)
fee_per_period = 10 * 10**18

nonce += 1  # увеличиваем nonce для следующей транзакции

SubscriptionContract = w3.eth.contract(abi=subscription_abi, bytecode=subscription_bytecode)

tx_deploy_subscription = SubscriptionContract.constructor(
    subtoken_address,
    fee_per_period
).build_transaction({
    "chainId": w3.eth.chain_id,
    "gas": 3000000,
    "maxPriorityFeePerGas": w3.to_wei('2', 'gwei'),
    "gasPrice": w3.eth.gas_price,
    "from": account_address,
    "nonce": nonce
})

signed_subscription = account.sign_transaction(tx_deploy_subscription)
tx_hash_subscription = w3.eth.send_raw_transaction(signed_subscription.raw_transaction)
print("SubscriptionContract deploy tx sent:", tx_hash_subscription.hex())

tx_receipt_subscription = w3.eth.wait_for_transaction_receipt(tx_hash_subscription)
subscription_address = tx_receipt_subscription.contractAddress

print("SubscriptionContract deployed at:", subscription_address)

print("\nDone!")
