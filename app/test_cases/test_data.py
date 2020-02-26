import logging
import os
import shutil

from flask import jsonify

from app import testdata

from config import Config

logger = logging.getLogger(__name__)


class TestData:
    """
    Main class to execute TestData test
    """
    def __init__(self, ticket_id, workdir=Config.SAMBA_FILEPATH):
        logger.info("Using workdir %s", workdir)
        path = os.path.join(workdir, "CONT-" + ticket_id)
        if not os.path.isdir(path):
            logger.error(workdir + " Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + " Doesn't exists, probably initialisation failed")
        else:
            if not os.path.isdir(path + "TestData"):
                os.makedirs(os.path.join(path, "TestData"))
            dest = shutil.copyfile("*log.gz", os.path.join(path, "TestData"))
            dest1 = shutil.copyfile("*msg.gz", os.path.join(path, "TestData"))

        self.workdir = workdir
        self.ticket_id = ticket_id

    def run_testdata(self, mode, ticket_id):
        logger.info("Running command test and %s",  self.workdir)
        response = TestData.submain(mode, ticket_id)
        if response != None:
            return jsonify(TestData.submain(mode, ticket_id)), 200
        else:
            raise ValueError("Error while running Testdata for {} ticktid".format(ticket_id))




