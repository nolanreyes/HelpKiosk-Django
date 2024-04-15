// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HELPToken is ERC20 {
    mapping(address => uint256) public retailerBalances;

    constructor() ERC20("HELP Token", "hTKN") {
        _mint(msg.sender, 1000000000000000000000000);
    }

    function deposit(address user, uint256 amount) public {
        _mint(user, amount);
    }

    function getBalance(address user) public view returns (uint256) {
        return balanceOf(user);
    }

    function spendFunds(address retailer, uint256 amount) public {
        require(balanceOf(msg.sender) >= amount, "Insufficient balance.");
        _transfer(msg.sender, retailer, amount);
        retailerBalances[retailer] += amount;
    }

    function getRetailerBalance(address retailer) public view returns (uint256) {
        return retailerBalances[retailer];
    }
}