import logging

from flask import request, send_file
from flask_restful import Resource

from app.test_cases.sbt import SBT

logger = logging.getLogger(__name__)


class test_case(Resource):

    def post(self, ticket_id, test_name):
        logger.info("Got request to execute %s test for %s", test_name, ticket_id)
        logger.info("Request {}".format(request.args))

        if test_name not in ('sbt', 'sake', 'lime'):
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

        return {"status": "test case not implemented"}, 500

    def get(self, ticket_id, test_name):
        logger.info("Got request to get result of  %s test for %s", test_name, ticket_id)
        logger.info("Request {}".format(request.args))

        if test_name not in ('sbt', 'sake', 'lime'):
            error_msg = "Invalid test_name {0}".format(test_name)
            logger.error(error_msg)
            return {"Error": error_msg}, 400
        if test_name.lower() == 'sbt':
            logger.debug("For SBT")
            need_html = request.args.get('htmlPage', default="False", type=str)
            my_sbt = SBT()
            if need_html == "False":
                return {"Error ": "Missing Query Parameter htmlPage"}, 400
            else:
                out = my_sbt.get_html_sbt(need_html)
                logger.debug("Output --- Got Output Request " + out)
                return send_file(out)

        return {"status": "test case not implemented"}, 500