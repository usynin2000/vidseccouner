from web3 import Web3
from config import INFURA_API_KEY, PRIVATE_KEY
from typing import Any
import json


def transfer_token(
    contract_address: str,
    from_address: str,
    to_address: str,
    amount: int,
    private_key: str
) -> Any:
    """
    Функция для перевода токенов (ERC-20).

    :param contract_address: адрес контракта
    :param from_address: адрес отправителя
    :param to_address: адрес получателя
    :param amount: количество токенов для перевода
    :param private_key: приватный ключ отправителя
    :return: хеш транзакции или receipt (на ваше усмотрение)
    """

    # 1. Читаем скомпилированный ABI из файла
    with open("compiled.json", "r", encoding="utf-8") as f:
        res = json.load(f)

    # Предположим, что ваша структура compiled.json такая же, как и для get_balance:
    abi = res["contracts"]["SimpleToken.sol"]["SimpleToken"]["abi"]

    # 2. Инициализируем Web3
    w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))

    # 3. Создаём объект контракта
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # 4. Строим транзакцию для трансфера
    #    chainId для Sepolia = 11155111
    nonce = w3.eth.get_transaction_count(from_address)
    tx = contract.functions.transfer(to_address, amount).build_transaction({
        'chainId': 11155111,  # или используйте w3.eth.chain_id
        'from': from_address,
        'nonce': nonce,
        # При желании можно указать лимит газа принудительно.
        # Ниже - упрощённый пример с фиксированной ценой газа.
        'gas': 200000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })

    # 5. Подписываем транзакцию приватным ключом
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

    # 6. Отправляем подписанную транзакцию
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Транзакция отправлена")
    # print("Хеш:", tx_hash.hex())

    # 7. (Опционально) Ждём подтверждения транзакции и возвращаем receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


if __name__ == "__main__":
    contract_address = "0x40d87A3c7003A5A2dDA819721F998757fFcb65a8"
    from_address = "0xac0fDFfe0F1E474D41Dc14B745f0846CB2362e9F"
    to_address = "0x17dD57eaaF89aa437af2eE84Bd38c40AC99Ab7b2"
    amount = 100000000000000000000  # какое количество токенов хотите перевести
    private_key = PRIVATE_KEY

    receipt = transfer_token(contract_address, from_address, to_address, amount, private_key)
    print("Статус транзакции:", receipt["status"])  # 1 = успех, 0 = провал
