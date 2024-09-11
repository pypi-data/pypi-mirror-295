from abc import ABC, abstractmethod
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

'''
In these classes:
SesamStrategy is the strategy interface.
EnvSesamStrategy, AzureKeyVaultSesamStrategy, and HashiCorpVaultSesamStrategy are concrete strategies for different secret management systems.
Sesam is the context that uses a strategy to get secrets.
You can switch between different secret management systems by changing the strategy at runtime. This makes your code flexible and easy to extend.
'''

# Strategy Interface
class SesamStrategy(ABC):
    @abstractmethod
    def secret(self, key: str) -> str:
        pass

# Concrete Strategy for .env
class EnvSesamStrategy(SesamStrategy):
    KEY_SUFFFIX = "_KEY"
    def secret(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if len(key.strip()) == 0:
            raise ValueError("Key cannot be empty or whitespace")
        
        # Load the .env file
        load_dotenv()
        try:
            # TODO : separate key from secret
            # Retrieve the key and encrypted secret from the .env file
            if os.getenv(key+self.KEY_SUFFFIX) is None:
                raise KeyError(f"Key of '{key}' does not exist")
            key_name = os.getenv(key+self.KEY_SUFFFIX).encode()
            encrypted_secret = os.getenv(key).encode()
            # Instantiate a Fernet instance with the key
            fernet = Fernet(key_name)
            # Decrypt the secret
            decrypted_secret = fernet.decrypt(encrypted_secret)
            return decrypted_secret.decode()
        except (AttributeError, KeyError) as error:
            raise error


# Concrete Strategy for Azure Key Vault
'''
class AzureKeyVaultSesamStrategy(SesamStrategy):
    def __init__(self, vault_url: str, credential):
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient
        self.client = SecretClient(vault_url=vault_url, credential=credential or DefaultAzureCredential())

    def get_secret(self, key: str) -> str:
        return self.client.get_secret(key).value


# Concrete Strategy for HashiCorp Vault
class HashiCorpVaultSesamStrategy(SesamStrategy):
    def __init__(self, url: str, token: str):
        import hvac
        self.client = hvac.Client(url=url, token=token)

    def get_secret(self, key: str) -> str:
        secret = self.client.secrets.kv.read_secret_version(path=key)
        return secret['data']['data'][key]
'''

# Context
class Sesam:
    def __init__(self, strategy: SesamStrategy):
        if not isinstance(strategy, SesamStrategy):
            raise TypeError("Strategy must be an instance of SesamStrategy")
        self._strategy = strategy

    def set_strategy(self, strategy: SesamStrategy):
        if not isinstance(strategy, SesamStrategy):
            raise TypeError("Strategy must be an instance of SesamStrategy")
        self._strategy = strategy

    def secret(self, key: str) -> str:
        try:
            return self._strategy.secret(key)
        except (TypeError, ValueError, KeyError) as e:
            # Handle specific exceptions if needed
            raise e
    

