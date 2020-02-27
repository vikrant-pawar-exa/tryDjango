import ast
import importlib
import logging
import os
import re
import subprocess
from datetime import datetime
from distutils.dir_util import copy_tree
from fnmatch import fnmatch
from shutil import copyfile
from zipfile import ZipFile

from app.utils.constant import Constants
from app.utils.custom_response import make_resp
from config import Config

logger = logging.getLogger(__name__)
class  Triage:

    def test_source_code_compatible(self,code_data):
        try:
            return ast.parse(code_data)
        except SyntaxError as exc:
            logger.exception("Syntax error")
            return False

    #Converting csv to log file and returns log file 
    def csv_to_log(self, file):
        sample_file = "sample.log"
        if file.endswith(".csv"):
            logger.info(f'found csv file: {file}')
            bash_command= Config.FETCH_CSV_SCRIPT + " " +  file + " > " +sample_file
            bash_command = "python3 " + bash_command if self.test_source_code_compatible(Config.FETCH_CSV_SCRIPT) else "python2 " + bash_command
            # my_module = importlib.import_module(Config.FETCH_CSV_SCRIPT)
            logger.info(f'Running command {bash_command}')

            subprocess.check_output(bash_command, shell= True)
            return sample_file
        elif file.endswith(".log"):
            logger.info(f'found log file: {file}')
            return file
        else:
            logger.error(f'file {file} not found')
            return None

    def unzip_zip(self, zip_file):
        logger.info("Exctracting " )
        extract_dest = os.path.splitext(os.path.basename(zip_file))[0]
        extracted_log_list = []
        # extracting .csv, .txt, .log files from all .zip files in the directory
        logger.info("\nFrom: " + zip_file)
        with ZipFile(zip_file) as zipObj:
            listOfFileNames = zipObj.namelist()
            logger.info("Extracting: ")
            logger.info(listOfFileNames)
            for fileName in listOfFileNames:
                if fileName.endswith('.csv') or fileName.endswith('.txt') or fileName.endswith('.log'):
                    zipObj.extract(fileName,extract_dest)
                    extracted_log_list.append(fileName)
                elif os.path.isdir(fileName):
                    zipObj.extract(fileName,extract_dest)
                    extracted_log_list.append(fileName)
        logger.info("\nExtracted: ")
        logger.info(extracted_log_list)
        return extracted_log_list

    @staticmethod
    def get_ticket_dir(ticket_id,user="_test_"):
        """
            This function will create home dir and clone latet Exa_sec to it 
        """
        ticket_dir = Config.WORK_DIR+'/'+ticket_id
        if os.path.exists(ticket_dir):
            logger.error("Path {} already exists".format(ticket_dir))
        else:
            logger.info("Creating folder " +ticket_dir )
            os.makedirs(ticket_dir)
        # TODO: Error handling

        # TODO: git clone exa_sec
        logger.info("Ticket ID for %s is %s", ticket_id , ticket_dir)

        return ticket_dir

    def pre_test_setup(self, ticket_number, file_path):      
        # Should be pre_test setup 
        work_dir = Config.WORK_DIR + f'/{ticket_number}/dataInput/' + datetime.today().strftime('%Y-%m-%d')+ "/"
        logger.info(f'working directory: {work_dir}')
        logger.info("checking for file %s ", work_dir + file_path)
        
        if not os.path.exists(work_dir + file_path):
            logger.error(f"Log file  {file_path} doesn't exist")
            return make_resp({"message":f"Log file  {file_path} doesn't exist"}, 404)
        os.chdir(work_dir)

        try:
            file_path = re.sub(" ","\ ",file_path)
            log_file_name = self.csv_to_log(file_path)
            if not log_file_name == None:
                subprocess.check_output([Config.MAKE_SPLUNKCSV_SCRIPT, log_file_name])
                formated_log_gz_file_name = Constants.FORMATED_LOG_GZ_FILE_PREFIX + log_file_name + ".gz"
                os.rename(formated_log_gz_file_name, Constants.SPLUNK_MIXED_LOG_FILE)
                logger.info('Successfully generated GZ file')
                return make_resp({"message":"Successfully generated GZ file"}, 200)
            else:
                logger.error("Insuficient data: No suitable file found")
                return make_resp({"message":"Insuficient data"}, 400)
        except subprocess.CalledProcessError as cp:
            logger.error(f"Failed to convert file to log.gz file \n error: {cp}")
            return make_resp({"message":"Failed to convert file to log.gz file"}, 500)


    def fetch_log_file(self, work_dir):
        files = []
        logger.info("Fetching all .csv, .txt, and .log files in folder")
        for fname in os.listdir(work_dir):
            if fname.endswith('.csv') or fname.endswith('.txt') or fname.endswith('.log') or fname.endswith('.zip') or fname.endswith('.gz') :
                files.append(fname)
            elif os.path.isdir(fname):
                files.append(fname)
        logger.info("Folder contains:")
        logger.info(files)
        return files

    def get_log_files(self, ticket_id, subdirectory):
        logger.info("Getting log files for "+ ticket_id)
        work_dir = Triage.get_ticket_dir(ticket_id)
        log_path = Config.SMB_logs + "/" +  ticket_id + "/"
        # ToDO: ticket_path to log file path
        work_dir = work_dir + '/dataInput/'+ datetime.today().strftime('%Y-%m-%d') + "/"
        logger.info(f'working directory for test files: {work_dir}')
        logger.info('log path for ticket_id %s, is %s', ticket_id, log_path)
    
        if not os.path.exists(log_path):
            logger.error(f"Ticket path {log_path} doesn't exist")
            return make_resp({"message":f"Ticket path {log_path} doesn't exist"}, 500)
        
        try:
            copy_tree(log_path, work_dir)
            logger.info(f"Successfully copied content of {log_path} to {work_dir}")
        except DistutilsFileError as er:
            logger.error(f"{log_path} is not Directory ")
            return make_resp({"message":f"{log_path} is not Directory "}, 404)

        os.chdir(work_dir)
        
        if not subdirectory == "None" :
            if subdirectory.endswith(".zip"):
                logger.info(f"Found {subdirectory}")
                return self.unzip_zip(subdirectory)
            elif os.path.isdir(subdirectory):
                work_dir = work_dir + subdirectory
            else:
                return make_resp({"message":f"{subdirectory} is not zip or Directory "}, 400)


        #To fetch all log files
        return self.fetch_log_file(work_dir)
