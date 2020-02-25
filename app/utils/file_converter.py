import os, re, logging, subprocess, ast
from fnmatch import fnmatch
from distutils.dir_util import copy_tree
from zipfile import ZipFile
from datetime import datetime
from shutil import copyfile

from config import Config
from app.utils.custom_response import make_resp
from app.utils.constant import Constants

class  Triage:

    def test_source_code_compatible(self,code_data):
        try:
            return ast.parse(code_data)
        except SyntaxError as exc:
            return False

    #Converting csv to log file and returns log file 
    def csv_to_log(self, file):
        sample_file = "sample.log"
        if file.endswith(".csv"):
            logging.info(f'found csv file: {file}')
            bash_command= Config.FETCH_CSV_SCRIPT + " " +  file + " > " +sample_file
            bash_command = "python " + bash_command if self.test_source_code_compatible(Config.FETCH_CSV_SCRIPT) else "python2 " + bash_command
            subprocess.check_output(bash_command, shell= True)
            return sample_file
        elif file.endswith(".log"):
            logging.info(f'found log file: {file}')
            return file
        else:
            logging.error(f'file {file} not found')
            return None

    def unzip_zip(self, log_file):
        logging.info("Exctracting " )
        extract_dest = os.path.splitext(os.path.basename(log_file))[0]
        extracted_log_list = []
        # extracting .csv, .txt, .log files from all .zip files in the directory
        logging.info("\nFrom: " + log_file)
        with ZipFile(log_file) as zipObj:
            listOfFileNames = zipObj.namelist()
            logging.info("Extracting: ")
            logging.info(listOfFileNames)
            for fileName in listOfFileNames:
                if fileName.endswith('.csv') or fileName.endswith('.txt') or fileName.endswith('.log'):
                    zipObj.extract(fileName,extract_dest)
                    extracted_log_list.append(fileName)
                elif os.path.isdir(fileName):
                    zipObj.extract(fileName,extract_dest)
                    extracted_log_list.append(fileName)
        logging.info("\nExtracted: ")
        logging.info(extracted_log_list)
        return extracted_log_list

    def lime_setup(self, ticket_number, log_file):       
        work_dir = Config.WORK_DIR + datetime.today().strftime('%Y-%m-%d')+ "/"
        logging.info(f'working directory: {work_dir}')
        
        if not os.path.exists(work_dir + log_file):
            logging.error(f"Log file  {log_file} doesn't exist")
            return make_resp({"message":"Log file  {log_file} doesn't exist"}, 404)
        os.chdir(work_dir)

        try:
            log_file_name = self.csv_to_log(log_file)
            if not log_file_name == None:
                subprocess.check_output([Config.MAKE_SPLUNKCSV_SCRIPT, log_file_name])
                os.rename(Constants.FORMATED_SAMPLE_FILE, Constants.SPLUNK_MIXED_LOG_FILE)
                logging.info('Successfully generated GZ file')
                return make_resp({"message":"Successfully generated GZ file"}, 200)
            else:
                logging.error("Insuficient data: No suitable file found")
                return make_resp({"message":"Insuficient data"}, 400)
        except subprocess.CalledProcessError as cp:
            logging.error(f"Failed to convert file to log.gz file \n error: {cp}")
            return make_resp({"message":"Failed to convert file to log.gz file"}, 500)


    def fetch_log_file(self, work_dir):
        files = []
        logging.info("Fetching all .csv, .txt, and .log files in folder")
        for fname in os.listdir(work_dir):
            if fname.endswith('.csv') or fname.endswith('.txt') or fname.endswith('.log') or fname.endswith('.zip') :
                files.append(fname)
            elif os.path.isdir(fname):
                files.append(fname)
        logging.info("Folder contains:")
        logging.info(files)
        return files

    def get_log_files(self, ticket_id, subdirectory):
        logging.info("Getting log files for "+ ticket_id)
        work_dir = Config.WORK_DIR
        ticket_path = Config.TICKETS_DIR_PATH +  ticket_id + "/"
        work_dir = work_dir + datetime.today().strftime('%Y-%m-%d') + "/"
        logging.info(f'working directory: {work_dir}')
    
        if not os.path.exists(ticket_path):
            logging.error(f"Ticket path {ticket_path} doesn't exist")
            return make_resp({"message":f"Ticket path {ticket_path} doesn't exist"}, 500)
        
        try:
            copy_tree(ticket_path, work_dir)
            logging.info(f"Successfully copied content of {ticket_path} to {work_dir}")
        except DistutilsFileError as er:
            logging.error(f"{ticket_path} is not Directory ")
            return make_resp({"message":f"{ticket_path} is not Directory "}, 404)

        os.chdir(work_dir)
        
        if not subdirectory == "None" :
            if subdirectory.endswith(".zip"):
                logging.info(f"Found {subdirectory}")
                return self.unzip_zip(subdirectory)
            elif os.path.isdir(subdirectory):
                work_dir = work_dir + subdirectory
            else:
                return make_resp({"message":f"{subdirectory} is not zip or Directory "}, 400)


        #To fetch all log files
        return self.fetch_log_file(work_dir)
        
