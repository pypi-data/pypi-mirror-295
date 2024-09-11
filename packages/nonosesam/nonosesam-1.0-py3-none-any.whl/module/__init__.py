# my_package/__init__.py

from abc import ABC, abstractmethod
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Import the strategy interface and concrete strategies
from .module import (
    SesamStrategy,
    EnvSesamStrategy,
    # AzureKeyVaultSesamStrategy,  # Uncomment if you implement this
    # HashiCorpVaultSesamStrategy  # Uncomment if you implement this
)

# Import the context class
from .module import Sesam

# Optional: Define package-level variables or initialization code
__version__ = "1.0.0"
