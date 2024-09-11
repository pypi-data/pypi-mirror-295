from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

'''
AES/CBC/PKCS7Padding(PKCS5Padding) 加密解密
iv是空的16字节数据
'''
iv = bytes(16)


def encrypt(data: str, key: str):
    if not isinstance(data, bytes):
        data = data.encode('utf-8')

    encryptor = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv), backend=default_backend()).encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(cipher_text).decode('utf-8')


def decrypt(data: str, key: str):
    if not isinstance(data, bytes):
        data = data.encode('utf-8')

    decryptor = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv), backend=default_backend()).decryptor()
    decrypted_data = decryptor.update(base64.b64decode(data)) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()  # PKCS7解填充
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode('utf-8')
