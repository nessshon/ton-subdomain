import asyncio
from uuid import uuid4

from pytoniq import Contract, WalletV4R2, LiteBalancer
from pytoniq_core import Cell, begin_cell, StateInit

# Mainnet or testnet (False, True)
IS_TESTNET = True

# Mnemonic for wallet creation (tape lock hammer protect ...)
MNEMONIC = "tape lock hammer protect ..."  # noqa

# Wallet version (v3, v3r1, v3r2, v4, v4r2)
WALLET_VERSION = "v4r2"

# Smart contract code in base64
CONTRACT_CODE = "te6cckECCgEAAR0AART/APSkE/S88sgLAQIBYgIDAgLOBAUA06HGGEOukkFScAWAAeXAjEWuFg+AASoE8a5CBbwF4Aeuk+ACA/IF8IUGD+ge30JgQ4QBHEcF4DPgSIPcsR+2TdxJZK0boGuHkkDcI1cvN8xcqqsUOi/+Z7ygZ0JDgAEkYgPABQYP6B7fQmECASAGBwIBIAgJALsMzHQdNch+kAw8AH4QccF8uH1IMcAkTDg0x8BghBTejSRuo421AHQIPkC+EKDB/QPb6EwAtP/0wABwAGY1DBAE4MH9BeXMFiDB/RbMOIB+QL4QoMH9Bf4YvACkTDigABs7UTQ+kAB+GH0BDD4YoAAZPhCyPhBzxb0AMntVIAAdCCT0wcBkOgg10kS1yMBgxq1s4Q=="  # noqa


async def main():
    # Set up LiteBalancer provider
    if IS_TESTNET:
        provider = LiteBalancer.from_testnet_config(trust_level=1)
    else:
        provider = LiteBalancer.from_mainnet_config(trust_level=1)
    await provider.start_up()

    # Create a Ton wallet from the provided mnemonic
    wallet = await WalletV4R2.from_mnemonic(
        provider=provider,
        mnemonics=MNEMONIC.split(" "),
    )

    # Prepare the initial state for the smart contract
    state_init = StateInit(
        code=Cell.one_from_boc(CONTRACT_CODE),
        data=(
            begin_cell()
            .store_address(wallet.address.to_str())
            .store_maybe_ref(None)
            .store_uint(uuid4().int & (2 ** 64 - 1), 64)
            .end_cell()
        )
    )

    # Deploy the contract
    contract = await Contract.from_state_init(
        provider=provider,
        workchain=0,
        state_init=state_init,
    )
    await wallet.deploy_via_internal(contract=contract)

    # Close the LiteBalancer provider
    await provider.close_all()

    print(f"Deployed contract address: {contract.address.to_str()}")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
