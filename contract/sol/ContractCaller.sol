pragma solidity ^0.8.0;

contract ContractCaller {

    event ContractAddressCreated(address indexed creator);

    address public immutable creator;

    modifier onlyCreator() {
        require(creator == msg.sender, "Not Creator");
        _;
    }

    constructor() {
        creator = msg.sender;
        emit ContractAddressCreated(msg.sender);
    }

    function callFunc(address _target, bytes calldata _data) public payable {
        (bool success, ) = _target.call{value: msg.value}(_data);
        require(success, "Call Failed");
    }

    function claimETH() public onlyCreator {
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {

    }
}