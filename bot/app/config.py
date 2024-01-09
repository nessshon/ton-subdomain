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
            MANIFEST_URL=env.str("TON_CONNECT_MANIFEST_URL"),
        )
    )


def get_dns_collections(is_testnet: bool = False) -> List[str]:
    ton_dns_collection = "EQC3dNlesgVD8YbAazcauIrXBPfiVhMMr5YYk2in0Mtsz0Bz"  # noqa
    testnet_ton_dns_collection = "EQDjPtM6QusgMgWfl9kMcG-EALslbTITnKcH8VZK1pnH3UZA"  # noqa
    telegram_username_collection = "EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi"  # noqa

    if is_testnet:
        return [testnet_ton_dns_collection]
    return [ton_dns_collection, telegram_username_collection]
