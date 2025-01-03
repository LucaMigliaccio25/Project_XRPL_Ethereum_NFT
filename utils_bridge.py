from web3 import Web3
import os
from dotenv import load_dotenv
import json

# Caricamento delle variabili d'ambiente
load_dotenv(dotenv_path="private_data.env")

# Configurazione di QuickNode (Ethereum)
quicknode_url = os.getenv("QUICKNODE_URL")
web3 = Web3(Web3.HTTPProvider(quicknode_url))
if not web3.isConnected():
    raise Exception("--- Connessione a QuickNode fallita! ---")

contract_address = os.getenv("CONTRACT_ADDRESS")
with open("dynamic_nft_abi.json", "r") as abi_file:
    contract_abi = json.load(abi_file)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
private_key = os.getenv("PRIVATE_KEY_METAMASK")

def trigger_ethereum_nft(uri, owner_address):
    """
    Trigger the Ethereum smart contract to create a dynamic NFT.
    """
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.getTransactionCount(account.address)

    # Creazione dell'NFT su Ethereum
    txn = contract.functions.createNFT(owner_address, uri).buildTransaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': web3.toWei('10', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"Transazione inviata su Ethereum: {web3.toHex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transazione confermata: {receipt}")
    return receipt