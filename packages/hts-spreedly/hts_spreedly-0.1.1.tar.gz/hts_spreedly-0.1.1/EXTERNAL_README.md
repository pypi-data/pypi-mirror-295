# hts-spreedly

HTSFA client for interacting with the [Spreedly Payments API](https://docs.spreedly.com/reference/api/v1/#introduction).

## Usage Example

```python
import spreedly.client

client = spreedly.client.Client(
    base_url="https://core.spreedly.com",
    env_key=env_token, # spreedly environment token
    access_secret=access_secret, # environment access secret
    # optional encryption settings
    encryption=spreedly.client.Encryption(
        # token identifying which RSA certificate to use
        certificate_token=cert_token,
        # the certificate's public key
        public_key=pubkey
    ),
)

token = client.tokenize(
    number="4111111111111111",
    expiration_month="01",
    expiration_year="2028",
    first_name="john",
    last_name="smith",
)

print("Successfully tokenized card", token)

```
