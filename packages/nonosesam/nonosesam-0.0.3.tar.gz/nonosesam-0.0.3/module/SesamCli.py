import click
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

# Load existing .env file
load_dotenv()

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@click.command()
@click.argument('secret_name')
def generate_secret(secret_name):
    """Generate an encrypted secret and store it in the .env file."""
    # Generate a random secret
    secret = Fernet.generate_key().decode()

    # Encrypt the secret
    encrypted_secret = cipher_suite.encrypt(secret.encode()).decode()

    # Store the encrypted secret in the .env file
    set_key('.env', secret_name, encrypted_secret)

    # Store the encryption key in the .env file (for decryption purposes)
    set_key('.env', f'{secret_name}_KEY', key.decode())

    click.echo(f'Secret {secret_name} generated and stored in .env file.')

if __name__ == '__main__':
    generate_secret()
