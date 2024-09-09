from cryptography.fernet import Fernet

class TokenCrypto:
    def __init__(self, key):
        """
        Initialize the TokenCrypto class with a provided key.
        Provide key as a bytes object. Fernet.generate_key() can be used to generate a key.
        """
        if not key:
            raise ValueError("An encryption key must be provided")

        # Use the key as-is, without modification
        self.key = key
        self.fernet = Fernet(self.key)

    def encrypt(self, token):
        """
        Encrypt the given token or string.
        """
        if isinstance(token, str):
            token = token.encode()
        return self.fernet.encrypt(token).decode()

    def decrypt(self, encrypted_token):
        """
        Decrypt the given encrypted token or string.
        """
        if isinstance(encrypted_token, str):
            encrypted_token = encrypted_token.encode()
        return self.fernet.decrypt(encrypted_token).decode()

    def get_key(self):
        """
        Return the encryption key as a string.
        """
        return self.key.decode()


