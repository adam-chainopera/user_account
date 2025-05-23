from flask import Flask, jsonify, request
from web3 import Web3
from eth_account import Account
import os
import json
from dotenv import load_dotenv
load_dotenv()
from base64 import b64encode
from nacl.signing import SigningKey
import base58
import requests
import json

app = Flask(__name__)

# ✅ 1. dir
PRIVATE_KEY_DIR = os.getenv('PRIVATE_KEY_DIR', 'wallets')
os.makedirs(PRIVATE_KEY_DIR, exist_ok=True)

# ✅ 2. id and rpc
CHAIN_RPC_MAPPING = {
    '1': 'https://eth.llamarpc.com',       # Ethereum
    '11155111': 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID', # Sepolia
    '137': 'https://polygon-rpc.com',                                  # Polygon
    '56': 'https://binance.llamarpc.com'                          # BSC
}


@app.route('/generate_wallet', methods=['POST'])
def generate_wallet():
    acct = Account.create()

    wallet_info = {
        'address': acct.address,
        'private_key': acct.key.hex()
    }

    file_path = os.path.join(PRIVATE_KEY_DIR, f'{acct.address}.json')
    with open(file_path, 'w') as f:
        json.dump(wallet_info, f)

    return jsonify({
        'message': 'Wallet generated successfully',
        'address': acct.address
    })


@app.route('/solbalance/<address>', methods=['GET'])
def get_my_sol_balance(address):
    try:
        return jsonify({
            'chain_id': 'solana',
            'address': address,
            'balance_ether': get_solana_bal(address)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/balance/<chain_id>/<address>', methods=['GET'])
def get_balance(chain_id, address):
    rpc_url = CHAIN_RPC_MAPPING.get(chain_id)
    if not rpc_url:
        return jsonify({'error': f'Unsupported chain_id: {chain_id}'}), 400

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_address(address):
        return jsonify({'error': 'Invalid Ethereum address'}), 400

    try:
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return jsonify({
            'chain_id': chain_id,
            'address': address,
            'balance_ether': str(balance_eth)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_solana_wallet', methods=['POST'])
def generate_solana_wallet():
    signing=SigningKey.generate()
    public_key=base58.b58encode(signing.verify_key.encode()).decode('utf-8') 
    private_key=base58.b58encode(signing._signing_key).decode('utf-8')

    # save as JSON
    wallet_info = {
        'public_key': public_key,
        'private_key': private_key
    }

    file_path = os.path.join(PRIVATE_KEY_DIR, f'solana_{public_key}.json')
    with open(file_path, 'w') as f:
        json.dump(wallet_info, f)

    return jsonify({
        'message': 'Solana wallet generated successfully',
        'public_key': public_key
    })


def generate_solana_wallet_nacl():
    signing=SigningKey.generate()
    public_key=base58.b58encode(signing.verify_key.encode()).decode('utf-8') 
    private_key=base58.b58encode(signing._signing_key).decode('utf-8')
    print("public:{}".format(public_key))
    print("private_key:{}".format(private_key))


def get_solana_bal(WALLET_ADDRESS):
    RPC_URL = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [WALLET_ADDRESS]
    }

    response = requests.post(RPC_URL, json=payload)
    data = response.json()
    # 
    sol = 0
    if 'result' in data and data['result']:
        lamports = data['result']['value']
        sol = lamports / 1_000_000_000  # 1 SOL = 10^9 lamports
        print(f"wallet balance: {sol} SOL")
    else:
        print("fail :", data)
    
    return sol

if __name__ == '__main__':
    # get_solana_bal()
    app.run(debug=True)
