from app.database import client
from app.utils.token_conversion import TokenConversion
import logging


class Ticket_history:
    def add_status(history_ticket_status):
        try:
            client.jira_ticket_status.insert_one(history_ticket_status)
        except Exception as inst:
            logging.error("----Error while Adding ticket status history : {}".format(type(inst)))
