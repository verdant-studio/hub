from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

FERNET_SECRET_KEY = os.getenv('FERNET_SECRET_KEY')

if not FERNET_SECRET_KEY:
    raise ValueError('FERNET_SECRET_KEY is not set!')

fernet = Fernet(FERNET_SECRET_KEY.encode())