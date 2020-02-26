import logging
import os, glob
import shutil
from datetime import date

from app.testdata import TestData

from config import Config

logger = logging.getLogger(__name__)


class Testdata:
    """
    Main class to execute TestData test
    """
    def __init__(self, ticket_id, workdir=Config.SAMBA_FILEPATH):
        logger.info("Using workdir %s", workdir)
        path = os.path.join(workdir, ticket_id)
        source_dir="home/user/test/dataInput/{}".format(date.today())
        if not os.path.isdir(path):
            logger.error(workdir + " Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + " Doesn't exists, probably initialisation failed")
        else:
            if not os.path.isdir(path + "TestData"):
                os.makedirs(os.path.join(path, "TestData"),exist_ok=True)
            log_files = glob.iglob(os.path.join(source_dir, "*log.gz"))
            msg_files = glob.iglob(os.path.join(source_dir, "*msg.gz"))
            for file in log_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(path, "TestData"))
            for file in msg_files:
                if os.path.isfile(file):
                    shutil.copy(file, os.path.join(path, "TestData"))

        self.workdir = workdir
        self.ticket_id = ticket_id

    def run_testdata(self, mode, ticket_id):
        logger.info("Running command test and %s",  self.workdir)
        try:
            response = TestData.submain(mode, ticket_id)
            if response != None:
                return response
            else:
                raise ValueError("Error while running Testdata for {} ticktid".format(ticket_id))
        except:
            return {"message": "Error while running Testdata for CONT-{} ticktid".format(ticket_id)}, 422



