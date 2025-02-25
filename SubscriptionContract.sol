// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ISubToken {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
}

/**
 * Контракт «Подписки», использует ISubToken (наш SUB токен).
 *  - Можно подписаться на год (subscribeOneYear).
 *  - Хранит время окончания подписки: subscriptionEnd[user].
 *  - Владелец (owner) может collectFee(...) у подписчика, если подписка активна.
 */
contract SubscriptionContract {
    ISubToken public token;
    address public owner;
    uint256 public feePerPeriod;

    mapping(address => uint256) public subscriptionEnd;

    constructor(address _token, uint256 _feePerPeriod) {
        token = ISubToken(_token);
        owner = msg.sender;
        feePerPeriod = _feePerPeriod;
    }

    // Подписка на год
    function subscribeOneYear() external {
        subscriptionEnd[msg.sender] = block.timestamp + 365 days;
    }

    // Изменить размер периодической платы
    function setFeePerPeriod(uint256 newFee) external {
        require(msg.sender == owner, "Only owner can set fee");
        feePerPeriod = newFee;
    }

    // Списать плату у subscriber, если подписка не истекла
    function collectFee(address subscriber) external {
        require(msg.sender == owner, "Only owner can collect fees");
        require(block.timestamp <= subscriptionEnd[subscriber], "Subscription expired");

        bool success = token.transferFrom(subscriber, owner, feePerPeriod);
        require(success, "transferFrom failed");
    }
}
