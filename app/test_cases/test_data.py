import logging
import os, glob
import shutil
from datetime import date

from app.utils.file_converter import Triage
from app.models.tools_tickets_audit import ToolsTicketAudit
from app.testdata import TestData

from config import Config

logger = logging.getLogger(__name__)


class Testdata:
    """
    Main class to execute TestData test
    """
    """
        def __init__(self, ticket_id):
        workdir = Triage.get_ticket_dir(ticket_id)
        logger.info("Using workdir %s", workdir)
        source_dir= workdir + '/dataInput/'+ date.today().strftime('%Y-%m-%d') 
        if not os.path.isdir(workdir):
            logger.error(workdir + " Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + " Doesn't exists, probably initialisation failed")
        else:
            if not os.path.isdir(workdir + "TestData"):
                os.makedirs(os.path.join(workdir, "TestData"),exist_ok=True)
            log_files = glob.iglob(os.path.join(source_dir, "*log.gz"))
            msg_files = glob.iglob(os.path.join(source_dir, "*msg.gz"))
            for file in log_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(workdir, "TestData"))
            for file in msg_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(workdir, "TestData"))

        self.workdir = workdir
        self.ticket_id = ticket_id

    """
    def __init__(self, ticket_id):
        workdir = "/secure/samba/{}".format(ticket_id)
        logger.info("Using workdir %s", workdir)
        source_dir= workdir + '/dataInput/'+ date.today().strftime('%Y-%m-%d')
        if not os.path.isdir(workdir):
            logger.error(workdir + " Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + " Doesn't exists, probably initialisation failed")
        else:
            if not os.path.isdir(workdir + "TestData"):
                os.makedirs(os.path.join(workdir, "TestData"),exist_ok=True)
            log_files = glob.iglob(os.path.join(source_dir, "*log.gz"))
            msg_files = glob.iglob(os.path.join(source_dir, "*msg.gz"))
            for file in log_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(workdir, "TestData"))
            for file in msg_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(workdir, "TestData"))

        self.workdir = workdir
        self.ticket_id = ticket_id

    def run_testdata(self, mode, ticket_id):
        logger.info("Running command test and %s",  self.workdir)
        try:
            response = TestData.submain(mode, ticket_id[-4:])
            if response != None:
                tool_details = {'ticket_id': ticket_id, 'user_email': 'akshay@gslab.com', 'tool_executed': 'testdata',
                                'output': 'success'}
                ToolsTicketAudit.create_audit(tool_details)
                return response
            else:
                raise ValueError("Error while running Testdata for {} ticktid".format(ticket_id))
        except:
            return {"message": "Error while running Testdata for {} ticktid".format(ticket_id)}, 422



