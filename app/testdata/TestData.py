import ipaddress
import fnmatch
import json
import gzip
import sys
import os

MODE = "NONE"
SAMBA_FILEPATH = "/home/opt/samba/secured"
LOG_FILEPATH = ""
MSG_FILEPATH = ""

class TestDataStat:
    def __init__(self, stats, log_count, msg_count, warning):
        self.stats = stats
        self.log_count = log_count
        self.msg_count = msg_count
        self.warning = warning
    def serialize(self):
        return {
            'stats': self.stats,
            'log_count': self.log_count,
            'msg_count': self.msg_count,
            'warning': self.warning
        }

class TestData():

    def fetch_log_lines(self):
        print (LOG_FILEPATH)
        with gzip.open(LOG_FILEPATH, 'rb') as log_file:
            i=-1
            for l in log_file:
                i += 1
        return i

    def convert_msg_to_object(self):
        with gzip.open(MSG_FILEPATH, 'rb') as msg_file:
            msgs = []
            for m in msg_file:
                msgs.append(json.loads(m, encoding="utf-8"))
        return msgs

    def draw_lines(self, strlen):
        line = "="
        for i in range(1,strlen):
            line += "="
        print (line)

    def msg_stats(self, msgs):
        log_c = self.fetch_log_lines()
        msg_c = len(msgs)
        self.draw_lines(63)
        print ("|{:^60s}|".format("STATS BASED on TESTDATA directory"))
        self.draw_lines(63)
        print ("|{:^60s}|".format("Number of logs in " +os.path.basename(LOG_FILEPATH) + " = "+ str(log_c)))
        print ("|{:^60s}|".format("Number of msgs parsed in " +os.path.basename(MSG_FILEPATH)+ " = "+ str(msg_c)))
        self.draw_lines(63)

        stats_summary = {}
        for msg in msgs:
            if msg['msgType'] not in stats_summary.keys():
                fields = msg['fields'].keys()
                key_dict = dict.fromkeys(fields)
                stats_summary[msg['msgType']] = {'dataType': msg['dataType'],'parser_count': 1,'fields':{}}
                for k,v in key_dict.items():
                    stats_summary[msg['msgType']]['fields'][k] = {'field_count': 1, 'value_count': {msg['fields'][k] : 1}}
            else:
                stats_summary[msg['msgType']]['parser_count'] += 1
                for key,val in msg['fields'].items():
                    if key in stats_summary[msg['msgType']]['fields'].keys():
                        stats_summary[msg['msgType']]['fields'][key]['field_count'] += 1
                        if val in stats_summary[msg['msgType']]['fields'][key]['value_count'].keys():
                            stats_summary[msg['msgType']]['fields'][key]['value_count'][val] += 1
                        else:
                            stats_summary[msg['msgType']]['fields'][key]['value_count'][val] = 1
                    else:
                        stats_summary[msg['msgType']]['fields'][key] = {'field_count': 1, 'value_count': {val : 1}}

        print ("")
        print ("Parsers Used:")
        self.draw_lines(63)
        print("|{:^30s}|{:^30s}|".format("Parser", "Count"))
        self.draw_lines(63)
        for k,v in stats_summary.items():
            print ("|{:^30s}|{:^30d}|".format(k, v['parser_count']))
        self.draw_lines(63)
        for parser in stats_summary.keys():
            print("")
            print ("STATS on {}".format(parser))
            print ("Fields parsed:")
            self.draw_lines(63)
            print("|{:^30s}|{:^30s}|".format("Fields", "Field Count"))
            self.draw_lines(63)
            for field in stats_summary[parser]['fields'].keys():
                print ("|{:^30s}|{:^30d}|".format(field, stats_summary[parser]['fields'][field]['field_count']))
            self.draw_lines(63)
            print("")
            for field in stats_summary[parser]['fields'].keys():
                if field != 'time':
                    len_size = len(max(stats_summary[parser]['fields'][field]['value_count'], key=len))
                    if len_size < 30:
                        space_width = 30
                    else:
                        space_width = len_size
                    if len(stats_summary[parser]['fields'][field]['value_count'].keys()) >= 10:
                        print ("Top values of the field {} (limited to top 10)".format(field))
                    else:
                        print("Top values of the field {}".format(field))
                    self.draw_lines(space_width+33)
                    print("|{:^{width}}|{:^{count_width}}|".format(field, "Count", width = space_width, count_width = '30s'))
                    self.draw_lines(space_width+33)
                    value_dict = stats_summary[parser]['fields'][field]['value_count']
                    print_count = 0
                    for s in sorted(value_dict, key=value_dict.get, reverse=True ):
                        print_count += 1
                        if print_count < 11:
                            print("|{:^{width}}|{:^{count_width}}|".format(s,value_dict[s], width = space_width, count_width = '30d'))
                        else:
                            break
                    self.draw_lines(space_width+33)
                    print ("")
        return stats_summary,log_c,msg_c

    def compute_warnings(self, stats, log_count, msg_count):
        warning = {}
        integer_fields = ['bytes', 'bytes_num', 'result_code', 'num_pages', 'src_port', 'dest_port', 'logon_type', 'num_recipients']
        if log_count != msg_count:
            warning['Common'] = {'Log and Msg count mismatch': ''}
        for parser in stats.keys():
            bytes_flag = []
            ip_flag = host_flag = False

            # Time field not parsed
            if 'time' not in stats[parser]['fields'].keys():
                warning[parser] = {'Time field not parsed': ''}

            # Host field not parsed
            if 'host' not in stats[parser]['fields'].keys():
                if parser not in warning.keys():
                    warning[parser] = {'Host field not parsed': ''}
                else:
                    warning[parser]['Host field not parsed'] = ''

            # User field not parsed
            keylist = '\t'.join(stats[parser]['fields'].keys())
            if 'user' not in keylist:
                if parser not in warning.keys():
                    warning[parser] = {'User based field not parsed': ''}
                else:
                    warning[parser]['User based field not parsed'] = ''

            # IP field not in IP format
            for f in stats[parser]['fields'].keys():
                if '_ip' in f and not ip_flag:
                    for ip in stats[parser]['fields'][f]['value_count'].keys():
                        try:
                            ipaddress.ip_address(ip)
                        except:
                            ip_flag = True
                            warning_str = "Invalid IP format found in IP field {} in some cases ({})".format(f, ip)
                            if parser not in warning.keys():
                                warning[parser] = {warning_str: ''}
                            else:
                                warning[parser][warning_str] = ''

            # Host field has an IP
                if '_host' in f and not host_flag:
                    for host in stats[parser]['fields'][f]['value_count'].keys():
                        try:
                            ipaddress.ip_address(host)
                            host_flag = True
                            warning_str = "IP format found in host field {} in some cases ({})".format(f, host)
                            if parser not in warning.keys():
                                warning[parser] = {warning_str: ''}
                            else:
                                warning[parser][warning_str] = ''
                        except:
                            break

            # Bytes field is not integer
                if f in integer_fields:
                    for bytes in stats[parser]['fields'][f]['value_count'].keys():
                        if not bytes.replace('.','').isdigit() and f not in bytes_flag:
                            if f not in bytes_flag:
                                bytes_flag.append(f)
                            warning_str = "Field ({}) is not an integer value in some cases ({})".format(f, bytes)
                            if parser not in warning.keys():
                                warning[parser] = {warning_str: ''}
                            else:
                                warning[parser][warning_str] = ''

            # no leading or trailing space
                for val in stats[parser]['fields'][f]['value_count'].keys():
                    if val.strip() != val:
                        warning_string = "Field {} has leading/trailing spaces. Example: '{}'".format(f,val)
                        if parser not in warning.keys():
                            warning[parser] = {warning_string : ''}
                        else:
                            warning[parser][warning_string] = ''
                        break

            # Percentage of fields not parsed
            for f in stats[parser]['fields'].keys():
                if stats[parser]['fields'][f]['field_count'] != stats[parser]['parser_count']:
                    warning_str = "Field {} not parsed in {}% of the msgs".format(f, round(100.0 - (float(
                        stats[parser]['fields'][f]['field_count']) / float(stats[parser]['parser_count'])) * 100.0, 1))
                    if parser not in warning.keys():
                        warning[parser] = {warning_str: ''}
                    else:
                        warning[parser][warning_str] = ''

            # check if common fields are parsed for the dataType

        if os.path.exists("dataType_fields.json"):
            with open("dataType_fields.json", "r") as datatypes:
                data = datatypes.read()
                common_fields = json.loads(data)
        else:
            with open("app/testdata/dataType_fields.json", "r") as datatypes:
                data = datatypes.read()
                common_fields = json.loads(data)

        if stats[parser]['dataType'] in common_fields.keys():
            mand_fields = set(common_fields[stats[parser]['dataType']])
            parsed_fields = set(stats[parser]['fields'].keys())
            if not mand_fields.issubset(parsed_fields):
                missed_fields = mand_fields.difference(parsed_fields)
                warning_string = "Commonly parsed field(s) {} for this dataType not parsed".format(missed_fields)
                if parser not in warning.keys():
                    warning[parser] = {warning_string: ''}
                else:
                    warning[parser][warning_string] = ''

        return warning

    def warnings(self, stats, log_count, msg_count):
        tag = "warning_" + os.path.basename(MSG_FILEPATH).replace('msg.gz','' ).replace('.','') + ".log"
        if os.path.dirname(MSG_FILEPATH):
            warning_file = os.path.dirname(MSG_FILEPATH) + "/" + tag
        else:
            warning_file = tag
        if MODE == 'REV':
            if os.path.exists(warning_file):
                with open(warning_file, 'r') as outfile:
                    print(outfile.read())
            else:
                warning = self.compute_warnings(stats, log_count, msg_count)
                if not warning:
                    print ("No warnings found")
                else:
                    print ("No comments left by developer")
                    print("")
                    self.warning_print(warning)
        else:
            # Remove old warning file if any
            if os.path.exists(warning_file):
                os.remove(warning_file)
            warning = self.compute_warnings(stats, log_count, msg_count)

            if not warning:
                print ("No warnings found =)")
            else:
                # fetch comments for warnings
                print("Please add a comment/explanation to each warning in " + warning_file)
                self.warning_print(warning)

                # write warnings and comments to file
                with open(warning_file, 'w') as outfile:
                    self.write_file(outfile, warning)
        return warning

    def warning_print(self, warning):
        for k, v in warning.items():
            print("Warnings in {}:".format(k))
            for warn, comment in v.items():
                if MODE == 'REV':
                    print_val = "{}: {}".format(warn,comment)
                else:
                    print_val = warn
                if 'not parsed in ' in warn:
                    print("\t\t" + print_val)
                else:
                    print("\t" + print_val)
            print("")

    def write_file(self, outfile, warning):
        for k, v in warning.items():
            outfile.write("Warnings in {}:\n".format(k))
            for warn, comm in v.items():
                if ' not parsed in ' in warn:
                    outfile.write("\t\t"+ warn + " : " + comm + "\n")
                else:
                    outfile.write("\t"+ warn + " : " + comm + "\n")

def main():

    #Python version check
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    # Usage and argument check
    if len(sys.argv) < 2:
        print ("Usage: python3 TestData.py <mode> <JIRA#>")
        print ("Supported modes: DEV (Developer Mode), REV (Reviewer Mode)")
        print ("For example: python3 TestData.py DEV 1000")
        exit()
    submain(sys.argv[1], sys.argv[2])


def submain(mode, ticket_id):
    if mode in ('DEV', 'REV'):
        global MODE
        MODE = mode
    else:
        print ("{} is not a supported mode. Use DEV or REV".format(mode))
        exit()
    TEMP_PATH = SAMBA_FILEPATH + "/CONT-" + ticket_id + "/TestData"
    if os.path.exists(TEMP_PATH):
        log_files = []
        msg_files = []
        for file in os.listdir(TEMP_PATH):
            if fnmatch.fnmatch(file, '*log.gz'):
                log_files.append(file)
            if fnmatch.fnmatch(file, '*msg.gz'):
                msg_files.append(file)
        if len(log_files) != len(msg_files):
            print("Number of log.gz and msg.gz in {} does not match".format(TEMP_PATH))
            exit()
        elif len(log_files) > 1:
            line = 1
            display_msg = "Please pick one of the options to analyze the file:"
            for log in log_files:
                print (str(line) + ')' + ' ' +log)
                line += 1
            option_input = input(display_msg)
            if int(option_input) not in range(1,len(log_files)+1):
                print ("Not a valid option")
                exit()
            if os.path.exists(TEMP_PATH +"/"+ log_files[int(option_input)-1].replace('log.gz','msg.gz')):
                global LOG_FILEPATH
                LOG_FILEPATH = TEMP_PATH +"/"+ log_files[int(option_input)-1]
                global MSG_FILEPATH
                MSG_FILEPATH = TEMP_PATH +"/"+ log_files[int(option_input)-1].replace('log.gz','msg.gz')
            else:
                print("Corresponding msg file {} not found in {}".format(log_files[int(option_input)-1].replace('log.gz','msg.gz'), SAMBA_FILEPATH+'\CONT-'+sys.argv[2]))
                exit()
        elif not log_files:
            print ("No log.gz file found in {}".format(TEMP_PATH))
            exit()
        elif len(log_files) == len(msg_files) == 1:
            LOG_FILEPATH = TEMP_PATH + "/" + log_files[0]
            MSG_FILEPATH = TEMP_PATH + "/" + msg_files[0]
        else:
            exit()
    else:
        print ("{} path does not exist".format(TEMP_PATH))
        exit()

    td = TestData()
    msg_list = td.convert_msg_to_object()
    stats, log_count, msg_count = td.msg_stats(msg_list)
    warning = td.warnings(stats, log_count, msg_count)
    test_data_stat = TestDataStat(stats,log_count,msg_count,warning)
    return test_data_stat.serialize()


if __name__ == '__main__': main()
