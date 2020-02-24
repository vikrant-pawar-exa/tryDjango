from app.database import client
import logging
from app.utils.constant import Constants
from datetime import datetime


class ToolsTicketAudit:

	def create_audit(tool_details):
		try:
			tool_details['tool_executed'] = Constants.TOOLS.index(tool_details['tool_executed'].upper())
			tool_details['completion_time'] = str(datetime.now)
			client.tools_and_ticket_logging.insert_one(tool_details)
			return 'success'
		except Exception as e:
			logging.error("----Error while decryption : {}".format(type(e)))
			return 'failure'

	def get_audit_by_useremail(email):
		try:
			audit_logs = client.tools_and_ticket_logging.find({'user_email': email},  {'_id': False})
			return audit_logs
		except Exception as e:
			logging.error("----Error while decryption : {}".format(type(e)))
			return None

	def get_audit_by_useremail(ticket_id):
		try:
			audit_logs = client.tools_and_ticket_logging.find({'ticket_id': ticket_id},  {'_id': False})
			return audit_logs
		except Exception as e:
			logging.error("----Error while decryption : {}".format(type(e)))
			return None