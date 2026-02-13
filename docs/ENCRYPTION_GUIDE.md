# Password Encryption Guide

## Overview

This framework supports encrypted passwords in environment variables for enhanced security. MySQL passwords (and other sensitive data) can be encrypted before storing them in `.env` files.

## Quick Start

### 1. Generate an Encryption Key

```bash
python src/utils/encryption.py generate-key
```

This will output:
```
Generated encryption key: <your-key-here>

Add this to your .env file:
ENCRYPTION_KEY=<your-key-here>
```

### 2. Encrypt Your Password

```bash
python src/utils/encryption.py encrypt "your_password"
```

Or with a specific encryption key:
```bash
python src/utils/encryption.py encrypt "your_password" "your_encryption_key"
```

This will output:
```
Encrypted password: <encrypted-string>

Add this to your .env file:
MYSQL_PASSWORD=<encrypted-string>
```

### 3. Update Your .env File

```env
# Encryption Key
ENCRYPTION_KEY=your_generated_encryption_key

# MySQL Database Settings
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=gAAAAABhxxx...  # Your encrypted password
MYSQL_DATABASE=test_automation
```

## Usage in Code

The MySQL MCP Server automatically decrypts passwords:

```python
from src.mcp_server.mysql_server import MySQLMCPServer
from src.utils.config import Config

config = Config()

# Password is automatically decrypted if needed
mysql_server = MySQLMCPServer(
    host=config.get("MYSQL_HOST"),
    port=int(config.get("MYSQL_PORT")),
    user=config.get("MYSQL_USER"),
    password=config.get("MYSQL_PASSWORD"),  # Can be encrypted or plain
    database=config.get("MYSQL_DATABASE"),
    encryption_key=config.get("ENCRYPTION_KEY")  # Optional
)
```

## Manual Encryption/Decryption

### In Python Code

```python
from src.utils.encryption import EncryptionManager, encrypt_password, decrypt_password

# Using helper functions
encrypted = encrypt_password("my_password")
decrypted = decrypt_password(encrypted)

# Using EncryptionManager class
manager = EncryptionManager()
encrypted = manager.encrypt("my_password")
decrypted = manager.decrypt(encrypted)

# Check if text is encrypted
is_encrypted = manager.is_encrypted(encrypted)  # True

# Decrypt only if needed
password = manager.decrypt_if_needed("plain_or_encrypted_password")
```

### Using CLI

```bash
# Encrypt a password
python src/utils/encryption.py encrypt "MySecurePassword123"

# Decrypt a password
python src/utils/encryption.py decrypt "gAAAAABhxxx..."

# With custom encryption key
python src/utils/encryption.py encrypt "password" "custom_key"
python src/utils/encryption.py decrypt "gAAAAABhxxx..." "custom_key"
```

## Security Best Practices

### 1. Keep Encryption Key Secure

❌ **DON'T:**
- Commit encryption keys to version control
- Share encryption keys in plain text
- Use the same key across environments

✅ **DO:**
- Store encryption keys in secure secret managers (AWS Secrets Manager, Azure Key Vault, etc.)
- Use different keys for dev, staging, and production
- Rotate keys regularly

### 2. Environment-Specific Keys

```bash
# Development
ENCRYPTION_KEY=dev_key_xxx

# Staging
ENCRYPTION_KEY=staging_key_xxx

# Production
ENCRYPTION_KEY=prod_key_xxx
```

### 3. .gitignore Configuration

Ensure your `.gitignore` includes:

```gitignore
.env
.env.local
*.key
secrets/
```

### 4. CI/CD Integration

For CI/CD pipelines, use secret environment variables:

**GitHub Actions:**
```yaml
- name: Run Tests
  env:
    ENCRYPTION_KEY: ${{ secrets.ENCRYPTION_KEY }}
    MYSQL_PASSWORD: ${{ secrets.MYSQL_PASSWORD }}
  run: pytest tests/
```

**GitLab CI:**
```yaml
test:
  variables:
    ENCRYPTION_KEY: $ENCRYPTION_KEY
    MYSQL_PASSWORD: $MYSQL_PASSWORD
  script:
    - pytest tests/
```

## How It Works

### Encryption Process

1. Uses **Fernet** (symmetric encryption) from the `cryptography` library
2. Derives a key from your encryption key using **PBKDF2** with SHA256
3. Encrypts the password and encodes it in base64
4. Result starts with `gAAAAA` (Fernet format identifier)

### Auto-Detection

The framework automatically detects if a password is encrypted by checking if it starts with `gAAAAA`. If it is, it decrypts it; otherwise, it uses the plain text password.

```python
# Both work seamlessly
MYSQL_PASSWORD=plain_password          # Used as-is
MYSQL_PASSWORD=gAAAAABhxxx...         # Automatically decrypted
```

## Troubleshooting

### Error: "Decryption failed"

**Cause:** Wrong encryption key or corrupted encrypted text

**Solution:**
1. Verify you're using the same encryption key that was used for encryption
2. Re-encrypt the password with the correct key

### Error: "ENCRYPTION_KEY not found"

**Cause:** Encryption key not set in environment

**Solution:**
```bash
# Add to .env file
ENCRYPTION_KEY=your_key_here

# Or set in environment
export ENCRYPTION_KEY=your_key_here
```

### Plain Password Still Works

The framework supports both encrypted and plain passwords. If you don't want plain passwords:

1. Always encrypt passwords before adding to `.env`
2. Add validation in your code to reject plain passwords

## Examples

### Complete Workflow

```bash
# 1. Generate key
python src/utils/encryption.py generate-key
# Output: ENCRYPTION_KEY=ZXvB3f5K...

# 2. Encrypt password
python src/utils/encryption.py encrypt "MyDBPassword123"
# Output: MYSQL_PASSWORD=gAAAAABh...

# 3. Update .env
cat >> .env << EOF
ENCRYPTION_KEY=ZXvB3f5K...
MYSQL_PASSWORD=gAAAAABh...
EOF

# 4. Run tests (password is auto-decrypted)
pytest tests/database/test_mysql.py -v
```

### Encrypting Multiple Passwords

```python
from src.utils.encryption import encrypt_password

passwords = {
    'mysql': 'mysql_password',
    'postgres': 'postgres_password',
    'redis': 'redis_password'
}

encryption_key = "your_encryption_key"

for name, password in passwords.items():
    encrypted = encrypt_password(password, encryption_key)
    print(f"{name.upper()}_PASSWORD={encrypted}")
```

## Migration from Plain Passwords

If you have existing plain passwords in `.env`:

```bash
# 1. Backup current .env
cp .env .env.backup

# 2. Generate new encryption key
python src/utils/encryption.py generate-key > key.txt

# 3. Encrypt existing password
python src/utils/encryption.py encrypt "$(grep MYSQL_PASSWORD .env | cut -d= -f2)"

# 4. Update .env with encrypted password and key
```

## Advanced Usage

### Custom Encryption Manager

```python
from src.utils.encryption import EncryptionManager

# Custom encryption key
manager = EncryptionManager(encryption_key="my_custom_key")

# Encrypt multiple values
encrypted_values = {
    'password': manager.encrypt("secret123"),
    'api_key': manager.encrypt("key_abc123"),
    'token': manager.encrypt("token_xyz789")
}

# Later, decrypt when needed
for key, encrypted in encrypted_values.items():
    decrypted = manager.decrypt(encrypted)
    print(f"{key}: {decrypted}")
```

### Conditional Encryption

```python
from src.utils.encryption import EncryptionManager

manager = EncryptionManager()

# Only encrypt if not already encrypted
password = "plain_password"
if not manager.is_encrypted(password):
    encrypted = manager.encrypt(password)
else:
    encrypted = password
```

## References

- [Cryptography Library Documentation](https://cryptography.io/)
- [Fernet Specification](https://github.com/fernet/spec/blob/master/Spec.md)
- [PBKDF2 Key Derivation](https://en.wikipedia.org/wiki/PBKDF2)
