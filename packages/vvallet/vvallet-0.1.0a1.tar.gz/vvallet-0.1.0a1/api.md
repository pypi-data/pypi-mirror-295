# Wallet

Types:

```python
from vvallet.types import (
    WalletCreateResponse,
    WalletCreateAddressResponse,
    WalletListAddressesResponse,
    WalletListBalancesResponse,
)
```

Methods:

- <code title="post /api/v1/createWallet">client.wallet.<a href="./src/vvallet/resources/wallet.py">create</a>(\*\*<a href="src/vvallet/types/wallet_create_params.py">params</a>) -> <a href="./src/vvallet/types/wallet_create_response.py">WalletCreateResponse</a></code>
- <code title="post /api/v1/createAddress">client.wallet.<a href="./src/vvallet/resources/wallet.py">create_address</a>(\*\*<a href="src/vvallet/types/wallet_create_address_params.py">params</a>) -> <a href="./src/vvallet/types/wallet_create_address_response.py">WalletCreateAddressResponse</a></code>
- <code title="post /api/v1/listAddress">client.wallet.<a href="./src/vvallet/resources/wallet.py">list_addresses</a>(\*\*<a href="src/vvallet/types/wallet_list_addresses_params.py">params</a>) -> <a href="./src/vvallet/types/wallet_list_addresses_response.py">WalletListAddressesResponse</a></code>
- <code title="post /api/v1/listBalances">client.wallet.<a href="./src/vvallet/resources/wallet.py">list_balances</a>(\*\*<a href="src/vvallet/types/wallet_list_balances_params.py">params</a>) -> <a href="./src/vvallet/types/wallet_list_balances_response.py">WalletListBalancesResponse</a></code>

# Transfer

Types:

```python
from vvallet.types import TransferCreateResponse
```

Methods:

- <code title="post /api/v1/transfer">client.transfer.<a href="./src/vvallet/resources/transfer.py">create</a>(\*\*<a href="src/vvallet/types/transfer_create_params.py">params</a>) -> <a href="./src/vvallet/types/transfer_create_response.py">TransferCreateResponse</a></code>
