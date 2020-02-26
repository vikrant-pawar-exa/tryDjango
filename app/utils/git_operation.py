from app.utils.constant import Constants
from app.utils.user import get_user_tokens
import logging, os, subprocess
from config import Config
logger = logging.getLogger(__name__)

PROJECT_ROOT_PATH = os.path.abspath(os.curdir)

def clone_repo(api_token, ticket_id):
    try:
      if not len(ticket_id) > 0: return {"status": "error", "msg": "Ticket ID must be present"}
      user_tokens = get_user_tokens(api_token)
      if not user_tokens["git_token"]: return {"status": "error", "msg": "Git access token must be present"}
      username = user_tokens["git_username"]
      if username == None: return {"status": "error", "msg": "Git username must be present"}
      dest_repo_path = PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"] + "/" + username + "/"
      if not os.path.exists(dest_repo_path):
        os.chdir(PROJECT_ROOT_PATH)
        os.mkdir(Config.GIT["DEST_REPO_DIR"], mode=0o777)
        os.chdir(PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"])
        os.mkdir(username, mode=0o777)
      os.chdir(dest_repo_path)
      clone_return_code = subprocess.run("git clone " + "https://" + user_tokens["git_token"] + "@github.com/" + Config.GIT["OWNER"] + "/" + Config.GIT["REPO"] + ".git", shell=True)
      if clone_return_code.returncode == 0:
        # import pdb; pdb.set_trace()
        logger.debug("-------Cloned the repo successfully--------------")
        os.chdir(Config.GIT["REPO"])
        branch_checkout = os.system("git checkout -b "+ticket_id)
        if branch_checkout == 0:
          logger.debug("--Switched to new branch---{}--------------".format(ticket_id))
          return {"status": "success", "msg": ticket_id }
      else:
        logger.debug("---Error in clone: {} --------------".format(clone_return_code))
        return {"status": "error", "msg": "Error in repo clone: Shell error code => {}".format(clone_return_code) }
    except Exception as e:
      logger.debug("---Exception in clonning repo {}------------------".format(e.args))
      return {"status": "error", "msg": "Exception in repo clone: ".format(e.args) }


