import base64
import asyncio
from typing import Union
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


class CryptographyManager:
    def __init__(
        self,
        password: Union[str, bytes],
        salt: Union[str, bytes] = None,
        iterations: int = 400000,
    ):
        """
        Initialize the CryptographyManager with the given parameters.

        :param password: The password used for key derivation.
        :param salt: The salt to use for PBKDF2. If None, a new salt is generated.
        :param iterations: The number of iterations for PBKDF2.
        """
        self.password = (
            password if isinstance(password, bytes) else str.encode(password)
        )
        self.salt = (
            salt
            if isinstance(salt, bytes)
            else str.encode(salt).decode("unicode_escape").encode()
        )
        self.iterations = iterations
        self.key_length = 32  # Length of the derived key in bytes (for Fernet)

        # Create PBKDF2HMAC instance
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=self.salt,
            iterations=self.iterations,
            backend=default_backend(),
        )

        # Derive a key from the password
        self.key = self.kdf.derive(self.password)

        # Encode the key in Base64 for Fernet
        self.encoded_key = base64.urlsafe_b64encode(self.key)

        # Create Fernet instance with the derived key
        self.fernet = Fernet(self.encoded_key)

    async def __aencrypt(self, message: Union[str, bytes]) -> bytes:
        """
        Encrypt the given message using Fernet asynchronously.

        :param message: The message to encrypt.
        :return: The encrypted message.
        """
        message = message if isinstance(message, bytes) else str.encode(message)
        return await asyncio.to_thread(self.fernet.encrypt, message)

    async def __adecrypt(self, token: bytes) -> bytes:
        """
        Decrypt the given token using Fernet asynchronously.

        :param token: The encrypted message to decrypt.
        :return: The decrypted message.
        """
        message = await asyncio.to_thread(self.fernet.decrypt, token)
        return message.decode()

    def encrypt(self, message: Union[str, bytes]) -> bytes:
        try:
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return self.__aencrypt(message=message)
        else:
            return asyncio.run(self.__aencrypt(message=message))

    def decrypt(self, token: bytes) -> bytes:
        try:
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return self.__adecrypt(token=token)
        else:
            return asyncio.run(self.__adecrypt(token=token))
