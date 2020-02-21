import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
from app.utils.key_generate import KeyGenerate

class TokenConversion:
	
	def encrypt_token(token):
		generated_key = KeyGenerate.generate_key()
		try:
			encrypted = generated_key.encrypt(token.encode())
			return encrypted
		except Exception as inst:
			logging.error("----Error while encryption of token : {}".format(type(inst)))

	def decrypt_token(encrypted_token):
		generated_key = KeyGenerate.generate_key()
		try:
			decrypted = generated_key.decrypt(encrypted_token)
			return decrypted.decode()
		except Exception as inst:
			logging.error("----Error while decryption : {}".format(type(inst)))

