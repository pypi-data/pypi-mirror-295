import os
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key_from_string(key_string: str) -> bytes:
    """
    Derives a 32-byte key from the given string using SHA-256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'',  # Salt should be added in production for security, but is omitted here for simplicity.
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(key_string.encode('utf-8'))

def decrypt_aes256(encrypted_data: bytes, key: str, iv: Optional[bytes] = None) -> str:
    """
    Decrypts the encrypted data with the provided key string.
    
    You could also use an iv, but if you don't it will take the default one. The default iv is 16 zero bytes.

    :param key: string to be hashed to 32 bytes
    :param iv:  16 bytes long
    :return: Decrypted data.
    """
    # Derive a 32-byte key from the key string
    key_bytes = derive_key_from_string(key)
    
    # If IV is not provided, use a default one (here it's assumed to be 16 bytes for AES)
    if iv is None:
        iv = b'\x00' * 16
    elif len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Convert bytes to string and return
    return unpadded_data.decode('utf-8')

def encrypt_aes256(plaintext: str, key: str, iv: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    Encrypts the plaintext with the provided key string.

    You could also use an iv, but if you don't, it will take the default one. The default iv value is randomly chosen.

    :param key: string to be hashed to 32 bytes
    :param iv:  16 bytes long
    :return: iv, encrypted_data
    """
    # Derive a 32-byte key from the key string
    key_bytes = derive_key_from_string(key)
    
    # If IV is not provided, generate a random 16-byte IV
    if iv is None:
        iv = os.urandom(16)
    elif len(iv) != 16:
        raise ValueError("IV must be 16 bytes long.")
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plaintext to be compatible with AES block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return the IV and the encrypted data
    return iv, encrypted_data
