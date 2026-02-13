"""
Encryption utilities for sensitive data.
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Manages encryption and decryption of sensitive data."""
    
    def __init__(self, encryption_key: str = None):
        """
        Initialize encryption manager.
        
        Args:
            encryption_key: Base encryption key (uses ENCRYPTION_KEY env var if not provided)
        """
        if encryption_key is None:
            encryption_key = os.getenv('ENCRYPTION_KEY', 'default-key-change-in-production')
        
        self.encryption_key = encryption_key
        self._cipher = None
    
    def _get_cipher(self) -> Fernet:
        """
        Get or create Fernet cipher instance.
        
        Returns:
            Fernet cipher instance
        """
        if self._cipher is None:
            # Derive a key from the encryption key using PBKDF2HMAC
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'test-automation-framework-salt',  # In production, use a random salt
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode()))
            self._cipher = Fernet(key)
        
        return self._cipher
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a string.
        
        Args:
            plaintext: String to encrypt
            
        Returns:
            Encrypted string (base64 encoded)
        """
        try:
            cipher = self._get_cipher()
            encrypted_bytes = cipher.encrypt(plaintext.encode())
            return encrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt a string.
        
        Args:
            encrypted_text: Encrypted string (base64 encoded)
            
        Returns:
            Decrypted plaintext string
        """
        try:
            cipher = self._get_cipher()
            decrypted_bytes = cipher.decrypt(encrypted_text.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def is_encrypted(self, text: str) -> bool:
        """
        Check if a string appears to be encrypted.
        
        Args:
            text: String to check
            
        Returns:
            True if string appears to be encrypted, False otherwise
        """
        try:
            # Encrypted strings from Fernet are base64 encoded and start with 'gAAAAA'
            return text.startswith('gAAAAA')
        except:
            return False
    
    def encrypt_if_needed(self, text: str) -> str:
        """
        Encrypt text only if it's not already encrypted.
        
        Args:
            text: Text to potentially encrypt
            
        Returns:
            Encrypted text
        """
        if self.is_encrypted(text):
            return text
        return self.encrypt(text)
    
    def decrypt_if_needed(self, text: str) -> str:
        """
        Decrypt text only if it appears to be encrypted.
        
        Args:
            text: Text to potentially decrypt
            
        Returns:
            Decrypted text or original text if not encrypted
        """
        if self.is_encrypted(text):
            return self.decrypt(text)
        return text


def generate_encryption_key() -> str:
    """
    Generate a new encryption key.
    
    Returns:
        Base64 encoded encryption key
    """
    return Fernet.generate_key().decode()


def encrypt_password(password: str, encryption_key: str = None) -> str:
    """
    Encrypt a password.
    
    Args:
        password: Password to encrypt
        encryption_key: Encryption key (optional)
        
    Returns:
        Encrypted password
    """
    manager = EncryptionManager(encryption_key)
    return manager.encrypt(password)


def decrypt_password(encrypted_password: str, encryption_key: str = None) -> str:
    """
    Decrypt a password.
    
    Args:
        encrypted_password: Encrypted password
        encryption_key: Encryption key (optional)
        
    Returns:
        Decrypted password
    """
    manager = EncryptionManager(encryption_key)
    return manager.decrypt(encrypted_password)


# CLI utility for encrypting passwords
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Encrypt: python encryption.py encrypt <password> [encryption_key]")
        print("  Decrypt: python encryption.py decrypt <encrypted_password> [encryption_key]")
        print("  Generate Key: python encryption.py generate-key")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate-key":
        key = generate_encryption_key()
        print(f"Generated encryption key: {key}")
        print("\nAdd this to your .env file:")
        print(f"ENCRYPTION_KEY={key}")
    
    elif command == "encrypt":
        if len(sys.argv) < 3:
            print("Error: Password required")
            sys.exit(1)
        
        password = sys.argv[2]
        key = sys.argv[3] if len(sys.argv) > 3 else None
        
        encrypted = encrypt_password(password, key)
        print(f"Encrypted password: {encrypted}")
        print("\nAdd this to your .env file:")
        print(f"MYSQL_PASSWORD={encrypted}")
    
    elif command == "decrypt":
        if len(sys.argv) < 3:
            print("Error: Encrypted password required")
            sys.exit(1)
        
        encrypted = sys.argv[2]
        key = sys.argv[3] if len(sys.argv) > 3 else None
        
        try:
            decrypted = decrypt_password(encrypted, key)
            print(f"Decrypted password: {decrypted}")
        except Exception as e:
            print(f"Error decrypting: {e}")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
