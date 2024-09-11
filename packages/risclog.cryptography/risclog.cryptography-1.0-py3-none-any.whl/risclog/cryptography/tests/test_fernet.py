import os
import pytest
from risclog.cryptography import CryptographyManager


@pytest.mark.asyncio
async def test_async_cryptography_manager():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"
    salt = os.urandom(16)

    crypto_manager = CryptographyManager(password=password, salt=salt)

    token = await crypto_manager.encrypt(message)
    assert token is not None

    decrypted_message = await crypto_manager.decrypt(token)
    assert decrypted_message == message.decode()


@pytest.mark.asyncio
async def test_async_cryptography_manager_invalid_token():
    salt = os.urandom(16)
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    invalid_token = b"InvalidToken"
    crypto_manager = CryptographyManager(password=password, salt=salt)

    with pytest.raises(Exception):
        await crypto_manager.decrypt(invalid_token)


def test_cryptography_manager():
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    message = b"Secret message!"
    salt = os.urandom(16)

    crypto_manager = CryptographyManager(password=password, salt=salt)

    token = crypto_manager.encrypt(message)
    assert token is not None

    decrypted_message = crypto_manager.decrypt(token)
    assert decrypted_message == message.decode()


def test_cryptography_manager_invalid_token():
    salt = os.urandom(16)
    password = b"fSaCbrwrNZt0TYumhzbAOCQl2Trp2siFqXa-rowb4l8="
    invalid_token = b"InvalidToken"
    crypto_manager = CryptographyManager(password=password, salt=salt)

    with pytest.raises(Exception):
        crypto_manager.decrypt(invalid_token)
