import hashlib

def hash_string(input_string: str) -> str:
    """
    Hash a given string using SHA-256.

    :param input_string: The input string to be hashed.
    :return: The SHA-256 hash of the input string in hexadecimal format.
    """
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Encode the input string to bytes, then update the hash object
    sha256_hash.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

import hashlib

def hash_file(file_path: str) -> str:
    """
    Hash the contents of a file using SHA-256.

    :param file_path: The path to the file to be hashed.
    :return: The SHA-256 hash of the file's contents in hexadecimal format.
    """
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Open the file in binary read mode and read chunks
    with open(file_path, "rb") as file:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()