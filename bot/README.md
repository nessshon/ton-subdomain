# 🤖 TON Subdomain Manager Bot

This bot provides a convenient and intuitive interface for creating, managing and configuring .ton subdomains in the TON
network.

* Bot example: [@TONSubdomainBot](https://t.me/TONSubdomainBot)

## Features

* **Main:** Deploying a smart contract and setting up a TON site, storage and wallet address.

* **TON-Connect Integration:** Seamless integration with TON-Connect for a secure and user-friendly experience.

* **Multilingual Support:** The bot is available in both Russian and English, allowing users to interact in their
  preferred language.

* **Testnet and Mainnet Support:** The bot supports both testnet and mainnet environments, providing flexibility for
  testing and deployment.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/tonmendon/ton-subdomain.git
    ```

2. Change into the bot directory:

    ```bash
    cd ton-subdomain/bot
    ```
3. Clone environment variables file:

   ```bash
   cp .env.example .env
   ```

4. Configure [environment variables](#environment-variables-reference) variables file:

   ```bash
   nano .env
   ```

5. Running a bot in a docker container:

   ```bash
   docker-compose up --build
   ```

## Environment Variables Reference

Here is a reference guide for the environment variables used in the project:

| Variable                 | Type | Description                                                    | Example         |
|--------------------------|------|----------------------------------------------------------------|-----------------|
| BOT_TOKEN                | str  | Bot token, obtained from [@BotFather](https://t.me/BotFather)  | 123456:qweRTY   | 
| BOT_DEV_ID               | int  | User ID of the bot developer or admin                          | 123456789       |
| TON_CONNECT_MANIFEST_URL | str  | tonconnect manifest URL                                        | https://...json |
| REDIS_HOST               | str  | The hostname or IP address of the Redis server                 | redis           |
| REDIS_PORT               | int  | The port number on which the Redis server is running           | 6379            |
| REDIS_DB                 | int  | The Redis database number                                      | 1               |
| TONAPI_KEY               | str  | TONAPI API key from tonconsole.com                             | AE33EX..ASD32   |
| TONAPI_MAX_RETRIES       | int  | Maximum number of retries per request if rate limit is reached | 5               |
