import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def aes_encrypt(plaintext, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    encrypted_data = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + encrypted_data


def aes_decrypt(encrypted_data, key):
    nonce = encrypted_data[:12]
    encrypted_data = encrypted_data[12:]
    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
    return decrypted_data


def decrypt_file(path, key_path):
    with open(path, "rb") as file_in:
        file_data = file_in.read()
    with open(key_path, "rb") as f:
        key = f.read()
    iv = file_data[: AES.block_size]
    encrypted_data = file_data[AES.block_size :]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode("utf-8")
