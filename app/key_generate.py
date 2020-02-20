import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

class KeyGenerate:
	def generate_key():
		password_provided = "secret_for_conversion" #change this based on the future scope.
		password = password_provided.encode() 
		salt = b'\xc0\xf9\xb3\xe8\x82.\xdb\xf8\xd4\xb2f\xfa\xbbs\xdf\x0c' # Fixed salt to encode the keys
		kdf = PBKDF2HMAC(
		    algorithm=hashes.SHA256(),
		    length=32,
		    salt=salt,
		    iterations=100000,
		    backend=default_backend()
		)
		key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
		fernet_key = Fernet(key)
		return fernet_key