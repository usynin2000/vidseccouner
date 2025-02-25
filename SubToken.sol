// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Пример очень простого ERC-20 токена «SUB».
 * - totalSupply = 10_000 * 10^18
 * - всё у deployer
 * - умеет transfer, approve, transferFrom, balanceOf, allowance, etc.
 */
contract SubToken {
    string public name = "Subscription Token";
    string public symbol = "SUB";
    uint8 public decimals = 18;
    uint256 public totalSupply = 10_000 * (10 ** uint256(decimals));

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(balanceOf[msg.sender] >= _amount, "Not enough balance");
        balanceOf[msg.sender] -= _amount;
        balanceOf[_to] += _amount;
        return true;
    }

    function approve(address _spender, uint256 _amount) public returns (bool success) {
        allowance[msg.sender][_spender] = _amount;
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _amount) public returns (bool success) {
        require(balanceOf[_from] >= _amount, "Not enough balance");
        require(allowance[_from][msg.sender] >= _amount, "Not enough allowance");

        balanceOf[_from] -= _amount;
        balanceOf[_to] += _amount;

        allowance[_from][msg.sender] -= _amount;
        return true;
    }
}
