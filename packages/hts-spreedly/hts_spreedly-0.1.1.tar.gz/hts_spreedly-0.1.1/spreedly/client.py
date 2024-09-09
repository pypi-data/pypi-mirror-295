import httpx

from dataclasses import dataclass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode
from .exception import AuthException, UnknownException


@dataclass
class Encryption:
    """
    Encryption parameters for Spreedly.

    The public_key should be an RSA public key.

    See: https://docs.spreedly.com/reference/api/v1/#certificates
    """

    certificate_token: str
    public_key: str


class Client:
    """
    Rich client used to interact with the Spreedly API.

    See: https://docs.spreedly.com/reference/api/v1/
    """

    def __init__(
        self,
        *,
        base_url: str,
        env_key: str,
        access_secret: str,
        encryption: Encryption = None,
    ):
        """
        Instantiates a Spreedly client.

        Use the env_key and access_secret corresponding to the environment where the
        spreedly operations should be taking place.

        if encryption is specified, field-level encryption will be applied to request payloads.
        """
        self.base_url = base_url
        self.encryption = encryption

        self._httpx = httpx.Client(
            # see https://docs.spreedly.com/reference/api/v1/#authentication
            auth=httpx.BasicAuth(username=env_key, password=access_secret),
        )

        if encryption:
            self._public_key = serialization.load_pem_public_key(
                encryption.public_key.encode("utf-8")
            )

    def _encrypt(self, value: str) -> str:
        return b64encode(
            self._public_key.encrypt(
                value.encode("utf-8"),
                # unfortunately, this was not defined on the docs explicitly, and was discovered organically.
                # other forms of padding would result in a rejected value.
                padding.PKCS1v15(),
            )
        ).decode("utf-8")

    def _build_tokenize_payload(
        self,
        *,
        number: str,
        expiration_month: str,
        expiration_year: str,
        first_name: str,
        last_name: str,
    ) -> dict:
        # see: https://docs.spreedly.com/reference/api/v1/#field-level-encryption
        transform = self._encrypt if self.encryption else lambda x: x

        card = {
            "number": transform(number),
            "month": transform(expiration_month),
            "year": transform(expiration_year),
            "first_name": transform(first_name),
            "last_name": transform(last_name),
        }

        payload = {
            "payment_method": (
                {"credit_card": card}
                if not self.encryption
                else {
                    "credit_card": card,
                    "encryption_certificate_token": self.encryption.certificate_token,
                    "encrypted_fields": "number,month,year,first_name,last_name",
                }
            )
        }
        return payload

    def tokenize(
        self,
        *,
        number: str,
        expiration_month: str,
        expiration_year: str,
        first_name: str,
        last_name: str,
    ) -> str:
        """
        Tokenizes a credit card.

        Returns a string that represents the credit card.
        """
        payload = self._build_tokenize_payload(
            number=number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            first_name=first_name,
            last_name=last_name,
        )
        raw_response = self._httpx.post(
            f"{self.base_url}/v1/payment_methods.json",
            json=payload,
        )

        response = raw_response.json()

        if raw_response.status_code == 401:
            raise AuthException(errors=response["errors"], response=response)
        elif raw_response.status_code == 500:
            raise UnknownException(response=response)

        return response["transaction"]["payment_method"]["token"]

    def close(self):
        """
        Release any held resources.
        """
        self._httpx.close()
