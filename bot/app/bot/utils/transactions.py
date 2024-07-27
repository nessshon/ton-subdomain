import time
from base64 import urlsafe_b64encode
from uuid import uuid4

from aiogram_tonconnect.tonconnect.models import Transaction, TransactionMessage
from pytoniq_core import begin_cell, Cell, StateInit, Address


class DeploySubdomainManagerTransaction(Transaction):

    def __init__(
            self,
            owner_address: str,
            domain_address: str,
    ) -> None:
        SUBDOMAIN_MANAGER_CONTRACT_CODE = "te6cckECCgEAAR0AART/APSkE/S88sgLAQIBYgIDAgLOBAUA06HGGEOukkFScAWAAeXAjEWuFg+AASoE8a5CBbwF4Aeuk+ACA/IF8IUGD+ge30JgQ4QBHEcF4DPgSIPcsR+2TdxJZK0boGuHkkDcI1cvN8xcqqsUOi/+Z7ygZ0JDgAEkYgPABQYP6B7fQmECASAGBwIBIAgJALsMzHQdNch+kAw8AH4QccF8uH1IMcAkTDg0x8BghBTejSRuo421AHQIPkC+EKDB/QPb6EwAtP/0wABwAGY1DBAE4MH9BeXMFiDB/RbMOIB+QL4QoMH9Bf4YvACkTDigABs7UTQ+kAB+GH0BDD4YoAAZPhCyPhBzxb0AMntVIAAdCCT0wcBkOgg10kS1yMBgxq1s4Q=="  # noqa

        state_init = StateInit(
            code=Cell.one_from_boc(SUBDOMAIN_MANAGER_CONTRACT_CODE),
            data=(
                begin_cell()
                .store_address(owner_address)
                .store_maybe_ref(None)
                .store_uint(uuid4().int & (2 ** 64 - 1), 64)
                .end_cell()
            )
        )
        subdomain_manager_address = Address((0, state_init.serialize().hash))
        messages = [
            TransactionMessage(
                address=subdomain_manager_address.to_str(),
                amount=str(int(0.05 * (10 ** 9))),
                payload=urlsafe_b64encode(
                    begin_cell()
                    .end_cell()
                    .to_boc()
                ).decode(),
                stateInit=urlsafe_b64encode(
                    state_init.serialize().to_boc()
                ).decode()
            ),
            TransactionMessage(
                address=domain_address,
                amount=str(int(0.02 * (10 ** 9))),
                payload=urlsafe_b64encode(
                    begin_cell()
                    .store_uint(0x4eb1f0f9, 32)
                    .store_uint(0, 64)
                    .store_uint(0x19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff, 256)
                    .store_maybe_ref(
                        begin_cell()
                        .store_uint(0xba93, 16)
                        .store_address(subdomain_manager_address.to_str())
                        .store_uint(0, 8)
                        .end_cell()
                    )
                    .end_cell()
                    .to_boc()
                ).decode(),
            )
        ]
        super().__init__(messages=messages, valid_until=int(time.time() + 300))


class _UpdateTransaction(Transaction):

    def __init__(
            self,
            domain: str,
            record_key: int,
            record_value: Cell,
            subdomain_manager_address: str,
    ) -> None:
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0x537a3491, 32)
            .store_ref(
                begin_cell()
                .store_string(domain)
                .store_uint(0, 8)
                .end_cell()
            )
            .store_uint(record_key, 256)
            .store_maybe_ref(record_value)
            .end_cell()
            .to_boc()
        ).decode()
        super().__init__(
            messages=[
                TransactionMessage(
                    address=subdomain_manager_address,
                    payload=payload,
                    amount=str(int(0.02 * (10 ** 9))),
                ),
                TransactionMessage(
                    address="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",  # noqa
                    payload=urlsafe_b64encode(
                        begin_cell()
                        .store_uint(0, 32)
                        .store_string("Service fee")
                        .end_cell()
                        .to_boc()
                    ).decode(),
                    amount=str(int(0.2 * (10 ** 9))),
                )
            ],
            valid_until=int(time.time() + 300),
        )


class SetNextResolverTransaction(_UpdateTransaction):

    def __init__(
            self,
            domain: str,
            resolver_address: str,
            subdomain_manager_address: str,
    ) -> None:
        record_key = 0x19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff
        record_value = (
            begin_cell()
            .store_uint(0xba93, 16)
            .store_address(resolver_address)
            .store_uint(0, 8)
            .end_cell()
        )
        super().__init__(domain, record_key, record_value, subdomain_manager_address)


class SetWalletTransaction(_UpdateTransaction):

    def __init__(
            self,
            domain: str,
            wallet_address: str,
            subdomain_manager_address: str,
    ) -> None:
        record_key = 0xe8d44050873dba865aa7c170ab4cce64d90839a34dcfd6cf71d14e0205443b1b
        record_value = (
            begin_cell()
            .store_uint(0x9fd3, 16)
            .store_address(wallet_address)
            .store_uint(0, 8)
            .end_cell()
        )
        super().__init__(domain, record_key, record_value, subdomain_manager_address)


class SetSiteTransaction(_UpdateTransaction):

    def __init__(
            self,
            domain: str,
            adnl_address: bytes,
            subdomain_manager_address: str,
    ) -> None:
        record_key = 0xfbae041b02c41ed0fd8a4efb039bc780dd6af4a1f0c420f42561ae705dda43fe
        record_value = (
            begin_cell()
            .store_uint(0xad01, 16)
            .store_bytes(adnl_address)
            .store_uint(0, 8)
            .end_cell()
        )
        super().__init__(domain, record_key, record_value, subdomain_manager_address)


class SetStorageTransaction(_UpdateTransaction):

    def __init__(
            self,
            domain: str,
            bag_id: bytes,
            subdomain_manager_address: str,
    ) -> None:
        record_key = 0x49a25f9feefaffecad0fcd30c50dc9331cff8b55ece53def6285c09e17e6f5d7
        record_value = (
            begin_cell()
            .store_uint(0x7473, 16)
            .store_bytes(bag_id)
            .store_uint(0, 8)
            .end_cell()
        )
        super().__init__(domain, record_key, record_value, subdomain_manager_address)
