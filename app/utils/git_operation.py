from app.utils.constant import Constants
import logging, os
from config import Config
logger = logging.getLogger(__name__)

PROJECT_ROOT_PATH = os.path.abspath(os.curdir)
GIT_ACCESS_TOKEN = "958ae41bc7e3b778684bb82d04a2542ba33b8f50"

def clone_repo():
    # import pdb; pdb.set_trace()
    try:
      username = "testuser"
      dest_repo_path = PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"] + "/" + username + "/"
      if not os.path.exists(dest_repo_path):
        os.chdir(PROJECT_ROOT_PATH)
        os.mkdir(Config.GIT["DEST_REPO_DIR"], mode=0o777)
        os.chdir(PROJECT_ROOT_PATH + "/" + Config.GIT["DEST_REPO_DIR"])
        os.mkdir(username, mode=0o777)
      os.chdir(dest_repo_path)
      os.system("git clone " + "https://" + GIT_ACCESS_TOKEN + "@github.com/" + Config.GIT["OWNER"] + "/" + Config.GIT["REPO"] + ".git")
      logger.debug("-------Repo cloned  successfully--------------")
      return "Cloned the repo successfully" + os.system('pwd')
    except Exception as e:
      logger.debug("---Exception in cloned repo {}------------------".format(e.args))


