import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
from app.key_generate import KeyGenerate

class KeyConversion:
	
	def encrypt_key(token):
		fernet_key = KeyGenerate.generate_key()
		try:
			encrypted = fernet_key.encrypt(token.encode())
			return encrypted
		except Exception as inst:
			print(type(inst)) # the exception instance
			print(inst.args) # arguments stored in .args

	def decrypt_key(encrypted_token):
		fernet_key = KeyGenerate.generate_key()
		try:
			#import pdb; pdb.set_trace()
			decrypted = fernet_key.decrypt(encrypted_token)
			return decrypted.decode()
		except Exception as inst:
			print(type(inst)) # the exception instance
			print(inst.args) # arguments stored in .args
