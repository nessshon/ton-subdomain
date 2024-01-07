import asyncio

from pytoniq import LiteBalancer, WalletV3, WalletV3R1, WalletV3R2, WalletV4, WalletV4R2
from pytoniq_core import begin_cell, Address

# Mainnet or testnet (False, True)
IS_TESTNET = True

# Mnemonic for wallet creation (tape lock hammer protect ...)
MNEMONIC = "tape lock hammer protect ..."  # noqa

# Wallet version (v3, v3r1, v3r2, v4, v4r2)
WALLET_VERSION = "v4r2"

# NFT Domain address
DOMAIN_ADDRESS = "EQCZRjSdJ7OJgheL95F5NeEqgvnhCJGZI0E874kDfPw1fRek"  # noqa

# Resolve address (Deployed contract address)
RESOLVE_ADDRESS = "EQCT5psf1XuajFHkMDwFMLOic0vJiqtTSV8RD9LcKmeGJJUG"  # noqa


async def main():
    # Set up LiteBalancer provider
    if IS_TESTNET:
        provider = LiteBalancer.from_testnet_config(trust_level=1)
    else:
        provider = LiteBalancer.from_mainnet_config(trust_level=1)
    await provider.start_up()

    # Create a Ton wallet from the provided mnemonic
    wallets = {"v3": WalletV3, "v3r1": WalletV3R1, "v3r2": WalletV3R2, "v4": WalletV4, "v4r2": WalletV4R2}
    wallet = await wallets[WALLET_VERSION].from_mnemonic(
        provider=provider,
        mnemonics=MNEMONIC.split(" "),
    )

    # Create an internal transfer message
    message = wallet.create_wallet_internal_message(
        destination=Address(DOMAIN_ADDRESS),
        value=int(0.02 * 10 ** 9),
        body=(
            begin_cell()
            .store_uint(0x4eb1f0f9, 32)
            .store_uint(0, 64)
            .store_uint(0x19f02441ee588fdb26ee24b2568dd035c3c9206e11ab979be62e55558a1d17ff, 256)
            .store_maybe_ref(
                begin_cell()
                .store_uint(0xba93, 16)
                .store_address(RESOLVE_ADDRESS)
                .store_uint(0, 8)
                .end_cell()
            )
            .end_cell()
        ),
        state_init=wallet.state_init,
    )

    # Perform the internal transfer
    await wallet.raw_transfer(msgs=[message])

    # Close the LiteBalancer provider
    await provider.close_all()

    print(f"Resolved address: {RESOLVE_ADDRESS}")


if __name__ == '__main__':
    # Run the main function
    asyncio.run(main())
