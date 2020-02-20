from app.database import client
from app.key_conversion import KeyConversion

class Users:
	def get_users():
		all_users = client.user_profiles.find()
		return all_users

	def get_user(email):
		print(email)
		user = client.user_profiles.find_one({"email": email},  {'_id': False})
		print(user['jira_token'])
		print(user)
		print(user['git_token'])
		user['jira_token'] = KeyConversion.decrypt_key(user['jira_token'])
		user['git_token'] = KeyConversion.decrypt_key(user['git_token'])
		return user

	def new_user(user):
		try:
			user['jira_token'] = KeyConversion.encrypt_key(user['jira_token'])
			user['git_token'] = KeyConversion.encrypt_key(user['git_token'])
			print("In user creat method")
			print(user)
			if client.user_profiles.find_one({'email': user['email']}):
				updated_user = client.user_profiles.update_one({'email': user['email']}, user)
				return updated_user.id
			else:
				new_user = client.user_profiles.insert_one(user)
				return new_user.inserted_id
		except Exception as inst:
			print(type(inst)) # the exception instance
			print(inst.args) # argu

