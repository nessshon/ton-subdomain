from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class BotConfig:
    TOKEN: str
    DEV_ID: int


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int

    def dsn(self) -> str:
        """
        Generates a Redis connection DSN (Data Source Name) using the provided host, port, and database.

        :return: The generated DSN.
        """
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


@dataclass
class TONConnectConfig:
    KEY: str
    MANIFEST_URL: str


@dataclass
class TONAPIConfig:
    API_KEY: str
    MAX_RETRIES: int


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    tonapi: TONAPIConfig
    tonconnect: TONConnectConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("BOT_DEV_ID"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        tonapi=TONAPIConfig(
            API_KEY=env.str("TONAPI_KEY"),
            MAX_RETRIES=env.int("TONAPI_MAX_RETRIES"),
        ),
        tonconnect=TONConnectConfig(
            KEY=env.str("TON_CONNECT_KEY"),
            MANIFEST_URL=env.str("TON_CONNECT_MANIFEST_URL"),
        )
    )


TON_DNS_COLLECTION = "0:b774d95eb20543f186c06b371ab88ad704f7e256130caf96189368a7d0cb6ccf"  # noqa
TON_DNS_TESTNET_COLLECTION = "0:e33ed33a42eb2032059f97d90c706f8400bb256d32139ca707f1564ad699c7dd"  # noqa
TELEGRAM_USERNAMES_COLLECTION = "0:80d78a35f955a14b679faa887ff4cd5bfc0f43b4a4eea2a7e6927f3701b273c2"  # noqa


def get_dns_collections(is_testnet: bool = False) -> List[str]:
    if is_testnet:
        return [TON_DNS_TESTNET_COLLECTION]
    return [TON_DNS_COLLECTION, TELEGRAM_USERNAMES_COLLECTION]
