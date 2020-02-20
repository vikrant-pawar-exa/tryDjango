# SBT
# This class is responsible for calling SBT tool and getting results
import logging
import os
import subprocess
from random import randint

from ansi2html import Ansi2HTMLConverter
from flask import send_file
from flask_restful import Resource

from config import Config

logger = logging.getLogger(__name__)


class sbt_resource(Resource):

    def get(self, ticket_id):
        try:
            my_sbt = SBT()
            out = my_sbt.get_html_sbt()
            logger.debug("Output --- Got Output Request " + out)
            return send_file(out)

        except ValueError as v:
            print("Value Error")
            return "Error" + str(v), 500


class SBT:
    """
    Main class to execute sbt test
    """

    def __init__(self, workdir=Config.EXA_SECURITY):
        logger.info("Using workdir %s", workdir)
        if not os.path.isdir(workdir):
            logger.error(workdir + "Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + "Doesn't exists, probably initialisation failed")

        if not os.path.isfile(os.path.join(workdir, "build.sbt")):
            msg = "build.sbt Doesn't exists, EXA_HOME isn't set correctly call may have failed"
            logger.error(msg)
            raise ValueError(msg)

        self.workdir = workdir

    def get_html_sbt(self):
        tmp_file = self.run_sbt_file()
        conv = Ansi2HTMLConverter()

        with open(tmp_file) as f:
            content = f.readlines()
        raw_txt = " "
        for c in content:
            raw_txt = raw_txt + c

        with open(tmp_file + '.html', 'w') as f:
            f.write(conv.convert(raw_txt))
        # final_html = conv.convert(raw_txt)
        return tmp_file + '.html'

    def run_sbt_file(self):
        sbt_path = "sbt"
        logger.info("Running command %s test and %s", sbt_path, self.workdir)
        n = 10
        tmp_file = "/tmp/tmp_sbt" + ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])

        with open(tmp_file, "w") as file:
            output = subprocess.run([sbt_path, "test"], stdout=file, cwd=self.workdir)

        logger.debug("sbt command executed %s", output)
        logger.debug("sbt output is stored at  %s ", tmp_file)

        return tmp_file
