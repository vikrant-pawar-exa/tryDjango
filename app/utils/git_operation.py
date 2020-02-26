from app.utils.constant import Constants
from app.utils.user import get_user_tokens
import logging, os
from config import Config
logger = logging.getLogger(__name__)

PROJECT_ROOT_PATH = os.path.abspath(os.curdir)

def clone_repo(api_token):
    # import pdb; pdb.set_trace()
    try:
      user_tokens = get_user_tokens(api_token)
      if not user_tokens["git_token"]: return "Git access token must be present"
      username = user_tokens["git_username"]
      if username == None: return "Git username must be present"
      dest_repo_path = PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"] + "/" + username + "/"
      if not os.path.exists(dest_repo_path):
        os.chdir(PROJECT_ROOT_PATH)
        os.mkdir(Config.GIT["DEST_REPO_DIR"], mode=0o777)
        os.chdir(PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"])
        os.mkdir(username, mode=0o777)
      os.chdir(dest_repo_path)
      os.system("git clone " + "https://" + user_tokens["git_token"] + "@github.com/" + Config.GIT["OWNER"] + "/" + Config.GIT["REPO"] + ".git")
      logger.debug("-------Cloned the repo successfully--------------")
      os.chdir(Config.GIT["REPO"])
      branch_checkout = os.system("git checkout -b "+Config.GIT["DEFAULT_BRANCH"])
      logger.debug("---{}--------------".format(branch_checkout))
      logger.debug("---Branch List {} --------------".format(os.system("git branch")))
      return "Cloned and checkout the repo successfully"
    except Exception as e:
      logger.debug("---Exception in clonning repo {}------------------".format(e.args))


