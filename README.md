# Wallet API

A multi-chain wallet API service based on Flask, supporting wallet generation and balance query for Ethereum series chains and Solana chains.

## Features

- Generate Ethereum wallets
- Generate Solana wallets
- Query multi-chain balances (Ethereum, Polygon, BSC, etc.)
- Query Solana balances

## Quick Start

### Using Docker

1. Build image:
```bash
docker build -t wallet-api .
```

2. Run container:
```bash
docker run -p 8000:8000 wallet-api
```

### Using Docker Compose

1. Start service:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop service:
```bash
docker-compose down
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start service (development mode):
```bash
python app.py
```

3. Or use gunicorn (production mode):
```bash
gunicorn --config gunicorn.conf.py app:app
```

## API Endpoints

- `POST /generate_wallet` - Generate Ethereum wallets
- `POST /generate_solana_wallet` - 生成 Solana 钱包
- `GET /balance/<chain_id>/<address>` - 查询以太坊系列链余额
- `GET /solbalance/<address>` - 查询 Solana 余额

## Environment Variables

- `PRIVATE_KEY_DIR` - Wallet file storage directory (default: wallets)

## Supported Chains

- Ethereum (chain_id: 1)
- Sepolia (chain_id: 11155111)
- Polygon (chain_id: 137)
- BSC (chain_id: 56)
- Solana
