import re
from typing import Union

from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIError

from app.config import TELEGRAM_USERNAMES_COLLECTION


def validate_domain(domain: str):
    if len(domain) > 128:
        return False
    pattern = re.compile(r'^[a-zA-Z0-9-]*$')
    return bool(pattern.match(domain))


def resolve_domain(domain_string: str) -> str:
    """
    Resolve domain string to its original form.

    This function takes domain string and performs the reverse
    process to obtain the original domain string.

    :param domain_string: The domain string.
    :return: The resolved domain string.
    """
    parts = domain_string.encode().split(b'\x00')
    decoded_parts = [part.decode('utf-8') for part in parts if part]
    resolved_domain = '.'.join(decoded_parts[::-1])

    return resolved_domain


async def get_domain_name(tonapi: AsyncTonapi, nft_address: str, collection_address: str) -> Union[str, None]:
    method_name = "get_full_domain" if collection_address == TELEGRAM_USERNAMES_COLLECTION else "get_domain"
    execute_result = await tonapi.blockchain.execute_get_method(nft_address, method_name)
    domain_string = execute_result.decoded.get("domain", None)

    if domain_string is None:
        return None

    if collection_address == TELEGRAM_USERNAMES_COLLECTION:
        return resolve_domain(domain_string)

    return resolve_domain(domain_string) + ".ton"


async def get_next_resolver(tonapi: AsyncTonapi, domain_name: Union[str, None]) -> Union[str, None]:
    try:
        dns_record = await tonapi.dns.resolve(domain_name)
    except TONAPIError:
        return None
    return dns_record.next_resolver


class StorageBagId:

    @staticmethod
    def is_valid(any_form):
        try:
            StorageBagId(any_form)
        except (Exception,):
            return False
        return True

    def __init__(self, any_form):
        if any_form is None:
            raise ValueError("Invalid address")

        if isinstance(any_form, StorageBagId):
            self.bytes = any_form.bytes
        elif isinstance(any_form, bytes):
            if len(any_form) != 32:
                raise ValueError('Invalid bag id bytes length')
            self.bytes = any_form
        elif isinstance(any_form, str):
            if len(any_form) != 64:
                raise ValueError('Invalid bag id hex length')
            self.bytes = bytes.fromhex(any_form)
        else:
            raise ValueError('Unsupported type')

    def to_hex(self):
        hex_string = self.bytes.hex()
        while len(hex_string) < 64:
            hex_string = '0' + hex_string
        return hex_string


class AdnlAddress:

    @staticmethod
    def is_valid(any_form):
        try:
            AdnlAddress(any_form)
        except (Exception,):
            return False
        return True

    def __init__(self, any_form):
        if any_form is None:
            raise ValueError("Invalid address")

        if isinstance(any_form, AdnlAddress):
            self.bytes = any_form.bytes
        elif isinstance(any_form, bytes):
            if len(any_form) != 32:
                raise ValueError('Invalid adnl bytes length')
            self.bytes = any_form
        elif isinstance(any_form, str):
            if len(any_form) != 64:
                raise ValueError('Invalid adnl hex length')
            self.bytes = bytes.fromhex(any_form)
        else:
            raise ValueError('Unsupported type')

    def to_hex(self):
        hex_string = self.bytes.hex()
        while len(hex_string) < 64:
            hex_string = '0' + hex_string
        return hex_string
