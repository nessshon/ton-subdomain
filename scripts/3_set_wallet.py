import asyncio

from pytoniq import LiteBalancer, WalletV3, WalletV3R1, WalletV3R2, WalletV4, WalletV4R2
from pytoniq_core import begin_cell, Address

# Mainnet or testnet (False, True)
IS_TESTNET = True

# Mnemonic for wallet creation (tape lock hammer protect ...)
MNEMONIC = "tape lock hammer protect ..."  # noqa

# Wallet version (v3, v3r1, v3r2, v4, v4r2)
WALLET_VERSION = "v4r2"

# Resolve address (Deployed contract address)
RESOLVE_ADDRESS = "EQCT5psf1XuajFHkMDwFMLOic0vJiqtTSV8RD9LcKmeGJJUG"  # noqa

# Wallet address to associate with the subdomain
WALLET_ADDRESS = "UQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNbbp"  # noqa

# Subdomain name
SUBDOMAIN = "ness"


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

    # Create a subdomain and associate it with a wallet address
    message = wallet.create_wallet_internal_message(
        destination=Address(RESOLVE_ADDRESS),  # noqa
        value=int(0.02 * 10 ** 9),
        body=(
            begin_cell()
            .store_uint(0x537a3491, 32)
            .store_ref(
                begin_cell()
                .store_string(SUBDOMAIN)
                .store_uint(0, 8)
                .end_cell()
            )
            .store_uint(0xe8d44050873dba865aa7c170ab4cce64d90839a34dcfd6cf71d14e0205443b1b, 256)
            .store_maybe_ref(
                begin_cell()
                .store_uint(0x9fd3, 16)
                .store_address(WALLET_ADDRESS)
                .store_uint(0, 8)
                .end_cell()
            )
            .end_cell()
        ),
        state_init=wallet.state_init,
    )

    # Perform the internal transfer to create the subdomain
    await wallet.raw_transfer(msgs=[message])

    # Close the LiteBalancer provider
    await provider.close_all()

    print(f"Created subdomain: {SUBDOMAIN}")


if __name__ == '__main__':
    # Run the main function
    asyncio.run(main())
