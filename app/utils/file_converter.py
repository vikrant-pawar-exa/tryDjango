import os, re, logging
from fnmatch import fnmatch
from distutils.dir_util import copy_tree
from zipfile import ZipFile
from datetime import datetime

from config import Config
from app.utils.custom_response import make_resp

class  Triage:

    #checks zip file in file path 
    def check_zip_file(self, log_file_path):
        head_tail = os.path.split(log_file_path)
        pattern = re.compile(".*zip.*")
        if re.match(pattern, head_tail[0]):
            splits = log_file_path.split("/")
            for split in splits:
                if split.endswith(".zip") :
                    with ZipFile(split) as zf:
                        extracted_folder = os.path.splitext(split)[0]
                        logging.info(f"Extracted in:{extracted_folder}")
                        zf.extractall(extracted_folder)
                        os.chdir(extracted_folder)
                elif os.path.isdir(split):
                    os.chdir(split)
                else:
                    return split
        else:
            return log_file_path

    #Converting csv to log file and returns log file 
    def get_log_file(self, file):
        sample_file = "sample.log"
        file = self.check_zip_file(file)
        if not os.path.exists("./" +file):
            logging.error(f"{file} doesn't exist")
            return None
        if file.endswith(".csv"):
            logging.info(f'found csv file: {file}')
            os.system("python " + Config.FETCH_CSV_SCRIPT + " " +  file + " > " +sample_file)
            return sample_file
        if file.endswith(".log"):
            logging.info(f'found log file: {file}')
            return file
        logging.error(f'file {file} not found')
        return None

    def lime_setup(self, ticket_number, log_file_path):         #
        #Setting env variable
        os.environ["EXABEAM_HOME"]= Config.EXABEAM_HOME
        work_dir = Config.WORK_DIR
        logging.info(f'EXABEAM_HOME = {os.getenv("EXABEAM_HOME")}')
        ticket_path = Config.TICKETS_DIR_PATH + '/CONT-' + ticket_number
        work_dir = work_dir + datetime.today().strftime('%Y-%m-%d')
        logging.info(f'working directory: {work_dir}')
        
        if not os.path.exists(ticket_path):
            logging.error(f"Ticket path {ticket_path} doesn't exist")
            return make_resp({"message":"Internal server error"}, 500)
        copy_tree(ticket_path, work_dir)
        os.chdir(work_dir)
        log_file_name = self.get_log_file(log_file_path)
        
        if not log_file_name == None:
            os.system(Config.MAKE_SPLUNKCSV_SCRIPT +" "+ log_file_name)
            os.rename('formated_sample.log.gz', '00.Splunk.mixed.log.gz')
            logging.info(Successfully generated GZ file)
            return make_resp({"message":"Successfully generated GZ file"}, 200)
        else:
            logging.info("Insuficient data: No suitable file found")
            return make_resp({"message":"Insuficient data"}, 400)
        