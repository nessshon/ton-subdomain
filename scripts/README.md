# Managing .ton Subdomains Guide

In this guide, we will write code to manage .ton subdomains, deploy a smart contract for subdomain management, set it as
the main controller for subdomains, and create a subdomain record while binding it to a wallet address.

## Preparation

* Start by installing the pytoniq library using the following command:

   ```bash
   pip install pytoniq
   ```

* Get a .ton domain if you don't have one. You can get it on the testnet [here](https://dns.ton.org/?testnet=true).

## Writing code

### Deploying the subdomain-manager Smart Contract

To deploy the smart contract, follow these steps:

1. Create a Python script (e.g., `deploy-subdomain-manager.py`).
2. Insert the following code and specify your parameters in the IS_TESTNET, MNEMONIC, WALLET_VERSION constants:

   ```python title="deploy-subdomain-manager.py"
   # deploy-subdomain-manager.py
   
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
   ```

3. Save the script and run it.
4. After successful execution of the code, a line will be displayed with the address of the deployed smart contract;
   save it; in the next stages it will be used as RESOLVE_ADDRESS.

### Set a subdomain manager on the .ton domain

To resolve an address, follow these steps:

1. Create a Python script (e.g., `set_next_resolve.py`).
2. Insert the following code and specify your parameters in the IS_TESTNET, MNEMONIC, WALLET_VERSION, DOMAIN_ADDRESS,
   RESOLVE_ADDRESS constants:

   ```python title="set_next_resolve.py"
   # set_next_resolve.py
   
   import asyncio

   from pytoniq import LiteBalancer, WalletV4R2
   from pytoniq_core import begin_cell, Address
   
   # Mainnet or testnet (False, True)
   IS_TESTNET = True
   
   # Mnemonic for wallet creation (tape lock hammer protect ...)
   MNEMONIC = "tape lock hammer protect ..."  # noqa
   
   # Wallet version (v3, v3r1, v3r2, v4, v4r2)
   WALLET_VERSION = "v4r2"
   
   # NFT DNS Domain address
   DOMAIN_ADDRESS = "<Your NFT DNS Domain Address>"  # noqa
   
   # Resolve address (Deployed contract address)
   RESOLVE_ADDRESS = "<Your Resolve Address>"  # noqa
   
   
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

   ```
3. Save the script and run it.
4. The resolved address will be displayed.

### Creating a Subdomain and set wallet address

To resolve an address, follow these steps:

1. Create a Python script (e.g., `set_wallet.py`).
2. Insert the following code and specify your parameters in the IS_TESTNET, MNEMONIC, WALLET_VERSION, RESOLVE_ADDRESS,
   WALLET_ADDRESS, SUBDOMAIN constants:

   ```python title="set_wallet.py"
   # set_wallet.py
   
   import asyncio
   
   from pytoniq import LiteBalancer, WalletV4R2
   from pytoniq_core import begin_cell, Address
   
   # Mainnet or testnet (False, True)
   IS_TESTNET = True
   
   # Mnemonic for wallet creation (tape lock hammer protect ...)
   MNEMONIC = "tape lock hammer protect ..."  # noqa
   
   # Wallet version (v3, v3r1, v3r2, v4, v4r2)
   WALLET_VERSION = "v4r2"
   
   # Resolve address (Deployed contract address)
   RESOLVE_ADDRESS = "<Your Resolve Address>"  # noqa
   
   # Wallet address to associate with the subdomain
   WALLET_ADDRESS = "<Your Wallet Address>"  # noqa
   
   # Subdomain name
   SUBDOMAIN = "<Your Subdomain Name>"  # noqa
   
   
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
   ```
3. Save the script and run it.
4. The created subdomain will be displayed.

## Summary

This documentation guides you through deploying a smart contract, resolving an address, and creating subdomains on the
.ton domain using Python and the pytoniq library.

What is next?
Using the last script provided, you can create multiple subdomains by running the script with different values for
SUBDOMAIN and WALLET_ADDRESS.

## See Also

* [Telegram bot for managing .ton subdomains](https://t.me/TONSubdomainBot)
* [Subdomain Manager source code](https://github.com/Gusarich/simple-subdomain)
* [Source code of scripts](https://github.com/tonmendon/ton-subdomain/tree/main/scripts)
