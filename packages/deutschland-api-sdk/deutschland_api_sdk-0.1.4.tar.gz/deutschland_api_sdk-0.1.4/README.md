
# DeutschlandAPI SDK

This SDK helps to access the [DeutschlandAPI](https://deutschland-api.dev)

## Usage

The following example shows how you initialize the client:

```python
from sdk.client import Client

client = Client.buildAnonymous()
collection = client.state().getAll();

for state in collection.entries:
    print(state.name)

```

More information about the complete API at:
https://app.typehub.cloud/d/deutschland-api/sdk
