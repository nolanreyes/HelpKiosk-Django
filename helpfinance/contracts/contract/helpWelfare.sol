// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract helpWelfare {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public retailerBalances;

    function deposit(address user, uint256 amount) public {
        balances[user] += amount;
    }

    function getBalance(address user) public view returns (uint256) {
        return balances[user];
    }

    function spendFunds(address retailer, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance.");
        balances[msg.sender] -= amount;
        retailerBalances[retailer] += amount;
    }

    function getRetailerBalance(address retailer) public view returns (uint256) {
        return retailerBalances[retailer];
    }
}
