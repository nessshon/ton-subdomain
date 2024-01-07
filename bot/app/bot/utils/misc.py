import re


def validate_domain(domain: str):
    if len(domain) > 128:
        return False
    pattern = re.compile(r'^[a-zA-Z0-9-]*$')
    return bool(pattern.match(domain))


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
