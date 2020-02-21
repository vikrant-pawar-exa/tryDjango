import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
from app.utils.constant import Constants

class KeyGenerate:
	def generate_key():
		key_derivation = PBKDF2HMAC(
		    algorithm=hashes.SHA256(),
		    length=32,
		    salt=Constants.SALT,
		    iterations=100000,
		    backend=default_backend()
		)
		key = base64.urlsafe_b64encode(key_derivation.derive(Constants.PASSWORD.encode())) 
		return Fernet(key)