import os, re, logging
from fnmatch import fnmatch
from distutils.dir_util import copy_tree
from zipfile import ZipFile
from datetime import datetime
from shutil import copyfile

from config import Config
from app.utils.custom_response import make_resp
from app.utils.constant import Constants

class  Triage:
    #Converting csv to log file and returns log file 
    def csv_to_log(self, file):
        sample_file = "sample.log"
        if file.endswith(".csv"):
            logging.info(f'found csv file: {file}')
            os.system("python " + Config.FETCH_CSV_SCRIPT + " " +  file + " > " +sample_file)
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
            logging.error(f"Log file  {ticket_path} doesn't exist")
            return make_resp({"message":"Log file  {ticket_path} doesn't exist"}, 404)
        os.chdir(work_dir)

        if log_file.endswith(".zip"):
            return self.unzip_zip(log_file)
        
        log_file_name = self.csv_to_log(log_file)
        if not log_file_name == None:
            os.system(Config.MAKE_SPLUNKCSV_SCRIPT +" "+ log_file_name)
            os.rename(Constants.FORMATED_SAMPLE_FILE, Constants.SPLUNK_MIXED_LOG_FILE)
            logging.info('Successfully generated GZ file')
            return make_resp({"message":"Successfully generated GZ file"}, 200)
        else:
            logging.info("Insuficient data: No suitable file found")
            return make_resp({"message":"Insuficient data"}, 400)


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

    def get_log_files(self, ticket_id):
        logging.info("Getting log files for "+ ticket_id)
        work_dir = Config.WORK_DIR
        ticket_path = Config.TICKETS_DIR_PATH +  ticket_id + "/"
        work_dir = work_dir + datetime.today().strftime('%Y-%m-%d')
        logging.info(f'working directory: {work_dir}')
    
        if not os.path.exists(ticket_path):
            logging.error(f"Ticket path {ticket_path} doesn't exist")
            return make_resp({"message":"Internal server error"}, 500)
        copy_tree(ticket_path, work_dir)
        os.chdir(work_dir)
        #To fetch all log files
        return self.fetch_log_file(work_dir)
        
