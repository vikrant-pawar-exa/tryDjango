import logging, sys

from flask import request, send_file
from flask_restful import Resource
from app.utils.file_converter import Triage
from app.utils.custom_response import make_resp

from app.test_cases.sbt import SBT
from app.test_cases.test_data import Testdata

logger = logging.getLogger(__name__)


class test_case(Resource):

    def post(self, ticket_id, test_name):
        logger.info("Got request to execute %s test for %s", test_name, ticket_id)
        logger.info("Request {}".format(request.args))

        try:

            if test_name not in ('sbt', 'sake', 'lime','pre_test'):
                error_msg = "Invalid test_name {0}".format(test_name)
                logger.error(error_msg)
                return {"Error": error_msg}, 400
            if test_name.lower() == 'sbt':
                logger.debug("For SBT")
                my_sbt = SBT()
                tmp_file, success = my_sbt.run_sbt_file()
                sbt_resp = {"SBT_Result": success, "File": tmp_file}
                logger.debug(" Got SBT output as %s, with file %s, for ticket %s", success, tmp_file, ticket_id)
                return sbt_resp, 200
            if test_name.lower() =='pre_test' :
                # Pre test function should create backend folder for latest user
                logger.debug("For pre_test")
                json_data = request.get_json(force=True)
                if not json_data:
                     return make_resp({'message': 'No input data provided'}, 400)
                log_file_path = json_data["logFilePath"]
                # Assuming log path as /samba/<ticketDir>
                return Triage().pre_test_setup(ticket_id, log_file_path)

        except ValueError as ve:
            logger.error("Got execption %s", ve)
            return { "status" : "got error {}".format(ve)  }, 500

        return {"status": "test case not implemented"}, 500

    def get(self, ticket_id, test_name):
        logger.info("Got request to get result of  %s test for %s", test_name, ticket_id)
        logger.info("Request {}".format(request.args))


        if test_name not in ('sbt', 'sake', 'lime', 'pre_test', 'testdata'):
            error_msg = "Invalid test_name {0}".format(test_name)
            logger.error(error_msg)
            return {"Error": error_msg}, 400
        if test_name.lower() == 'sbt':
            logger.debug("For SBT")
            need_html = request.args.get('htmlPage', default="False", type=str)
            if need_html == "False":
                return {"Error ": "Missing Query Parameter htmlPage"}, 400
            else:
                out = SBT.get_html_sbt(need_html)
                logger.debug("Output --- Got Output Request " + out)
                return send_file(out)
        if test_name.lower() == 'testdata':
            logger.debug("For TestData")
            my_testdata = Testdata(ticket_id)
            testdata_resp=my_testdata.run_testdata('DEV', ticket_id)
            logger.debug(" Got TestData output as  for ticket %s", ticket_id)
            return testdata_resp, 200
        if test_name.lower() == 'pre_test':
            logger.debug("For pre_test")
            subdirectory = request.args.get('subdirectory', default="None", type=str)
            try:
                return Triage().get_log_files(ticket_id, subdirectory)
            except:
                logging.error("----Exception in Fetch file API : {}".format(sys.exc_info()[1]))
                logger.exception("----Exception in Fetch file API : {}".format(sys.exc_info()[1]))
                return make_resp({"message": "Exception in API: {}".format(sys.exc_info()[1])}, 422)

        return {"status": "test case not implemented"}, 500