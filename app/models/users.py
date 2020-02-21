from app.database import client
from app.utils.token_conversion import TokenConversion
import logging

class Users:
	def get_users():
		all_users = client.user_profiles.find()
		return all_users

	# get user based on email
	def get_user(email):
		try:
			user = client.user_profiles.find_one({"email": email},  {'_id': False})
			user['jira_token'] = TokenConversion.decrypt_token(user['jira_token'])
			user['git_token'] = TokenConversion.decrypt_token(user['git_token'])
			return user
		except Exception as inst:
			logging.error("----Error while getting user : {}".format(type(inst)))

	def new_user(user):
		try:
			user['jira_token'] = TokenConversion.encrypt_token(user['jira_token'])
			user['git_token'] = TokenConversion.encrypt_token(user['git_token'])
			if client.user_profiles.find_one({'email': user['email']}):
				updated_user = client.user_profiles.update_one({'email': user['email']}, user)
				return updated_user.id
			else:
				new_user = client.user_profiles.insert_one(user)
				return new_user.inserted_id
		except Exception as inst:
			logging.error("----Error while creating user : {}".format(type(inst)))
