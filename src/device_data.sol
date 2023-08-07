pragma solidity 0.8.0;

contract Information {
    string public device_id;
    string public measure_type;
    uint public whole_part;
    uint public decimal_part;

    function store_data(
        string memory _device_id,
        string memory _measure_type,
        uint _whole_part,
        uint _decimal_part
    ) public {
        device_id = _device_id;
        measure_type = _measure_type;
        whole_part = _whole_part;
        decimal_part = _decimal_part;
    }

    function retrieve() public view returns (
        string memory, string memory, uint, uint
    ) {
        return (device_id, measure_type, whole_part, decimal_part);
    }
}
