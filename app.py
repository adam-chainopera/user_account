from flask import Flask, jsonify, request
from web3 import Web3
from eth_account import Account
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# ✅ 1. 私钥保存目录（可配置）
PRIVATE_KEY_DIR = os.getenv('PRIVATE_KEY_DIR', 'wallets')
os.makedirs(PRIVATE_KEY_DIR, exist_ok=True)

# ✅ 2. 链ID 和 RPC URL 映射配置（你可以随时修改或从文件加载）
CHAIN_RPC_MAPPING = {
    '1': 'https://eth.llamarpc.com',       # Ethereum 主网
    '11155111': 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID', # Sepolia 测试网
    '137': 'https://polygon-rpc.com',                                  # Polygon 主网
    '56': 'https://binance.llamarpc.com'                          # BSC 主网
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


if __name__ == '__main__':
    app.run(debug=True)
