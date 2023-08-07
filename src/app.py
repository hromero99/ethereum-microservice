from fastapi import FastAPI, HTTPException
from .schemas.sumary_data import SummaryData
import solcx
from web3 import Web3
import json

app = FastAPI()


@app.post("/")
async def write_data(data: SummaryData):

    with open("device_data.sol", "r") as contract_data:
        contract_data = contract_data.read()
    solcx.install_solc("0.8.0")
    compiled = solcx.compile_standard({
        "language": "Solidity",
        "sources": {"device_data.sol": {"content": contract_data}},
        "settings": {
            "outputSelection": {
                "*": {
                    # output needed to interact with and deploy contract
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
        solc_version="0.8.0",
    )

    with open("compiled.json", "w") as compiled_file:
        json.dump(compiled, compiled_file)

    bytecode = compiled["contracts"]["device_data.sol"]["Information"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled["contracts"]["device_data.sol"]
                     ["Information"]["metadata"])["output"]["abi"]

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    chain_id = 1337
    address = "0xb191ABe295943C6e575fd1eFb91Ec7bB8B43b085"
    private_key = "0x462914dc9ae465d094b2e9fb28c5cb39f824e1e5a42ffa3a3ae71232baa2cd73"

    device_data = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(address)

    transaction = device_data.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )

    sign_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(
        sign_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

    # At this point need the address of the contract to interact
    contact_list = w3.eth.contract(
        address=transaction_receipt.contractAddress, abi=abi)

    store_contact = contact_list.functions.store_data(
        data.device_id,
        data.measure_type,
        data.whole_value,
        data.decimal_value
    ).build_transaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(
        store_contact, private_key=private_key
    )
    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(
        sign_store_contact.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(
        send_store_contact)

    return contact_list.functions.retrieve().call()
