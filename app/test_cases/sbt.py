# SBT
# This class is responsible for calling SBT tool and getting results
import logging
import os
import subprocess
from random import randint

from ansi2html import Ansi2HTMLConverter

from config import Config

logger = logging.getLogger(__name__)


# class sbt_resource(Resource):
#
#     def get(self, ticket_id):
#         """
#         Get File by name with status
#         :param ticket_id:
#         :return:
#         """
#         try:
#             need_html = request.args.get('htmlPage', default="False", type=str)
#             my_sbt = SBT()
#             if need_html != "False":
#                 out = my_sbt.get_html_sbt(need_html)
#                 logger.debug("Output --- Got Output Request " + out)
#                 return send_file(out)
#             else:
#                 tmp_file, success = my_sbt.run_sbt_file()
#                 sbt_resp = {"SBT_Result": success , "File": tmp_file}
#                 logger.debug(" Got SBT output as %s, with file %s, for ticket %s", success, tmp_file, ticket_id)
#                 return sbt_resp, 200
#
#         except ValueError as v:
#             print("Value Error")
#             return "Error" + str(v), 500
#

class SBT:
    """
    Main class to execute sbt test
    """

    def __init__(self, workdir=Config.EXA_SECURITY):
        logger.info("Using workdir %s", workdir)
        if not os.path.isdir(workdir):
            msg = "workDir = "+ workdir + " Doesn't exists, probably initialisation failed"
            logger.error(msg)
            raise ValueError(msg)

        if not os.path.isfile(os.path.join(workdir, "build.sbt")):
            msg = "build.sbt Doesn't exists, EXA_HOME isn't set correctly call may have failed"
            logger.error(msg)
            raise ValueError(msg)

        self.workdir = workdir

    @staticmethod
    def get_html_sbt(tmp_file):

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
        """
        Run Sbt too
        :return:
        tmp_file : tmp File with SBT output
        sucess : True / False
        """
        sbt_path = "sbt"
        logger.info("Running command %s test and %s", sbt_path, self.workdir)
        n = 10
        tmp_file = "/tmp/tmp_sbt" + ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])

        with open(tmp_file, "w") as file:
            output = subprocess.run([sbt_path, "test"], stdout=file, cwd=self.workdir)

        logger.debug("sbt command executed %s , %s", output, bool(output.returncode))
        logger.debug("sbt output is stored at  %s ", tmp_file)

        chk_op = subprocess.run(["grep" , "All tests passed" , tmp_file ], cwd=self.workdir)
        print (chk_op.check_returncode) 

        return tmp_file, bool(output.returncode == 0)
