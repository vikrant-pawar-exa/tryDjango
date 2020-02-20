# SBT
# This class is responsible for calling SBT tool and getting results
import logging
import os

from flask_restful import reqparse, abort, Api, Resource

import subprocess

logger = logging.getLogger(__name__)

class sbt_resource(Resource):

    def __init__(self):
        self.result = 'test'


    def get(self, ticket_id):


        try:
            my_sbt = SBT()
            (out , err )= my_sbt.run_test()
            # print("Received", ticket_id)
            print("Output" + out)
            print("Error" + err)
            return "Received" + out, 200

        except ValueError as v:
            print ( "Value Error")
            return "Error" + str(v) , 500

    def execute_sbt(self):
        return self.result


class SBT():
    """
    Main class to execute sbt test
    """

    def __init__(self, workdir='/home/vikrant/exa_security'):
        logger.info("Using workdir %s", workdir)
        if not os.path.isdir(workdir):
            logger.error(workdir + "Doesn't exists, probably initialisation failed")
            raise ValueError(workdir + "Doesn't exists, probably initialisation failed")

        if not os.path.isfile(os.path.join(workdir, "build.sbt")):
            msg = "build.sbt Doesn't exists, EXA_HOME isn't set correctly call may have failed"
            logger.error(msg)
            raise ValueError(msg)

        self.workdir = workdir

    def run_test(self):
        output = subprocess.run("cd "+self.workdir + "; sbt test")
        err = "--"

        # p = subprocess.Popen(["ls", "-ltrs"], stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()

        print("Output" + str(output))
        print("Error" + str(err))

        return str(output), str(err)
