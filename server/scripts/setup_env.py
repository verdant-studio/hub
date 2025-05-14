from cryptography.fernet import Fernet
import os

# Path to the .env file
env_file_path = '.env'

# Check if .env file exists
if os.path.exists(env_file_path):
    # Read the .env file to check for FERNET_SECRET_KEY
    with open(env_file_path, 'r') as file:
        for line in file:
            if line.startswith('FERNET_SECRET_KEY'):
                print('FERNET_SECRET_KEY already exists in .env. Skipping key generation.')
                exit(0)

# Generate a new Fernet key
new_key = Fernet.generate_key().decode()

# Write the FERNET_SECRET_KEY to the .env file
with open(env_file_path, 'a') as file:
    file.write(f'FERNET_SECRET_KEY=\'{new_key}\'\n')

print(f'FERNET_SECRET_KEY has been added to {env_file_path}')