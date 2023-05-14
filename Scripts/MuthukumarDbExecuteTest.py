from MuthukumarEmail import *
# Muthu_email for send an email
'''
    Class MuthukumarDbExecuteTest is main execution of the framework. We can import a file from argparse or
    default library mapped dict list. Method 'get_version_DB' will collect all the imported file(s) of version(s).
    Executed file logs will be send through an email.

    HISTORY
    - 2019.07.27.01 - Muthukumar Subramanian
        * Initial release
    - 2022.10.05.01 - Muthukumar Subramanian
        * Updated the script as per the pep8 standard
'''
import re
import sys
import os
import time
from prettytable import PrettyTable
from MuthukumarDbUtilityCall import *
from datetime import datetime
import argparse

starting_timestamp = datetime.now()
start_time = str(starting_timestamp)

__version__ = '2022.10.05.01'
__author__ = 'Muthukumar Subramanian'


execute_test_log = 'MUTHUKUMAR_DB_EXECUTE_TEST_LOG'
(ok, log_obj) = user_lib_obj.Create_dir(file_name=execute_test_log, logger_enabled=True, add_handler=True)


class MuthukumarDbExecuteTest(sub_class_for_import_utils):
    def __init__(self, import_mod_name=None, *args, **kwargs):
        self.list = import_mod_name
        sub_class_for_import_utils.__init__(self, module_list=self.list, *args, **kwargs)

    def test(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
         Usage:
                Required argument(s):
                    :param kwargs: default dict, required support_def_list, available_def_list, log_obj, user_lib_obj
                Optional argument(s):
                    :param args: default list
        :return: ret_dict_test
        """
        ret_dict_test = {}
        mod_support_list = None
        available_functions = None
        log_obj = None
        user_lib_obj = None
        print("### Executing test method ###".format())
        if kwargs:
            mod_support_list = kwargs.get('support_def_list')
            available_functions = kwargs.get('available_def_list')
            log_obj = kwargs.get('log_obj')
            user_lib_obj = kwargs.get('user_lib_obj')

        if mod_support_list and available_functions:
            try:
                for each_def in available_functions:
                    if re.search(r'test_run.*', each_def):
                        if callable(available_functions.get(each_def)):
                            if log_obj and user_lib_obj.handler_as_root is False:
                                for index, each_handler in enumerate(log_obj.root.handlers):
                                    log_obj.root.removeHandler(log_obj.root.handlers[index])
                                # for index, each_handler in reversed(list(enumerate(log_obj.handlers))):
                                #     log_obj.removeHandler(log_obj.handlers[index])
                            time.sleep(1)
                            ret_code, ret_ref = available_functions.get(each_def)(self, *args, **kwargs)
                            if ret_code:
                                ret_dict_test.update({'ret_kwargs': ret_ref})
                            # ================= Send email if signup is successful =======================
                            if isinstance(ret_ref, dict):
                                if ret_ref.get('email_send') is True:
                                    e_ret = object_email.Muthu_email(obj, **ret_ref)
                                    if not e_ret:
                                        print("Issues observed while validating Muthu_email".format())
                                else:
                                    print("Unable to send an attachment(log file) to appropriate email id...!".format())
                            # =============================================================================
            except Exception as er_test_run_func_call:
                log_obj.error("Observed exception when call Func--> test_run!!! {}.".format(er_test_run_func_call))
            try:
                # Append remaining line(s)
                execute_test_log = 'MUTHUKUMAR_DB_EXECUTE_TEST_LOG'
                ret_ok, log_obj = user_lib_obj.Create_dir(file_name=execute_test_log, logger_enabled=True,
                                                        add_handler=True, append_log=True)
                if ret_ok:
                    ret_dict_test.update({'log_obj': log_obj})
            except Exception as err_log:
                print("Observed exception when create exec test!!! {}.".format(err_log))
            return True, ret_dict_test
        else:
            return False, ret_dict_test

    def get_version_DB(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
         Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: file_name_list, version
        """
        try:
            version = __version__
        except Exception as e:
            version = None
            pass
        file_name = __file__
        if file_name is not None:
            file_name_list = file_name.split('\\')
            file_name_list = [re.sub(r'.*\/(.*)\.py', r"\1", i, flags=re.I) for i in file_name_list if
                              re.match(r'.*.py', i, flags=re.I)]
            self.version_dict.update({file_name_list[0]: version})
            return True, file_name_list[0], version
        else:
            return False, None, None

    def table_for_version(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
         Usage:
            Required argument(s):
                :param kwargs: default dict
            Optional argument(s):
                :param args: default list
        :return: Boolean
        """
        table_2 = PrettyTable()
        table_2.field_names = ['Module Name', 'Version']
        table_2.title = "Executed modules version"
        list_app = []
        for k, v in self.version_dict.items():
            list_app.append([k, v])
        if list_app:
            for j in list_app:
                table_2.add_row(j)
            kwargs.update({'table_obj': table_2})
            ret = user_lib_obj.pretty_table_to_html_table_convertor(**kwargs)
        return True

    def table_for_execution(self, t_time, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
         Usage:
            Required argument(s):
                :param t_time: executed total time
                :param kwargs: default dict
            Optional argument(s):
                :param args: default list
        :return: Boolean
        """
        self.t_time = t_time
        list_app = []
        table_3 = PrettyTable()
        col = 'Execution Time'
        table_3.hrules = 1
        table_3.field_names = ['%64s' % (col), '%16s' % (self.t_time)]

        list_app.append(['DEL', 'DEL'])
        if list_app:
            for j in list_app:
                table_3.add_row(j)
                table_3.del_row(0)
            kwargs.update({'table_obj': table_3})
        ret = user_lib_obj.pretty_table_to_html_table_convertor(**kwargs)
        return True

    def cleanup_html_log(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        we can delete all the html and log file from log wrote directory.
        As of now disabled this method.
         Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: Boolean
        """
        # TODO cleanup_html_log
        changedir = os.chdir(r"C:\\Users\\ADMIN\\Documents\\GitHub\\PythonDatabaseAccessFramework"
                             r"\\Scripts\\MuthukumarClass.py")
        cwd1 = os.getcwd()
        list_all = os.listdir(cwd1)
        if list_all:
            list_all_log = [i for i in list_all if re.match(r'muthu.*.html$|muthu.*.log$', i, flags=re.I)]
            for each_html in list_all_log:
                os.remove(each_html)
        return True


def top_table(*args, **kwargs):
    """
    ..codeauthor:: Muthukumar Subramanian
    Script will import mentioned file(s), but it depends on mapped modules path
     Usage:
        Required argument(s):
            :param kwargs: default dict
        Optional argument(s):
            :param args: default list
    :return: execute_mod, module_list if it is successful, else Boolean
    """
    table = PrettyTable()
    table_field_values_append = []
    int_c = 0
    for dict_k, v in module_map.items():
        int_c = int_c + 1
        table_field_values_append.append([int_c, dict_k, v])

    table.field_names = ['Index', 'Module Key', 'Module Name']
    table.title = "Module Mapping List"
    table.hrules = 1
    for j in table_field_values_append:
        table.add_row(j)
    kwargs.update({'table_obj': table})
    ret = user_lib_obj.pretty_table_to_html_table_convertor(**kwargs)

    execute_mod = []
    module_list = []
    argparse_enable = False
    for dict_k, dict_v in module_map.items():
        if re.search(r'argparse_file.*', dict_k):
            argparse_enable = True

    if argparse_enable:
        for dict_k, dict_v in module_map.items():
            if re.search(r'argparse_file.*', dict_k):
                execute_mod.append(dict_v)
                module_list.append(dict_k)
        log_obj.info("Execute_mod: {}{}".format(execute_mod, module_list))
    else:
        log_obj.info("Enter data:".format())
        get_data = sys.stdin.readline()
        get_data = get_data.strip()
        log_obj.info("Entered data is: {}".format(get_data))
        m = None
        m1 = None
        if get_data != '':
            m = re.match(r"^((?![a-zA-Z]+).)*$", get_data)
            m1 = re.match(r"[a-zA-Z]+", get_data)
        index_d = None
        key_d = None
        if m is not None:
            get_data = int(get_data)
        elif m1 is not None:
            get_data = str(get_data)

        try:
            for i in range(0, len(table_field_values_append), 1):
                for j in range(0, len(table_field_values_append), 1):
                    if isinstance(get_data, int):
                        try:
                            if table_field_values_append[i][j] == get_data:
                                execute_mod.append(table_field_values_append[i][2])
                                module_list.append(table_field_values_append[i][1])
                        except IndexError:
                            continue
                    elif isinstance(get_data, str):
                        try:
                            if table_field_values_append[i][j] == get_data:
                                execute_mod.append(table_field_values_append[i][2])
                                module_list.append(table_field_values_append[i][1])
                        except IndexError:
                            continue
                    else:
                        log_obj.info("Invalid data: {}".format(get_data))
        except Exception as rr:
            log_obj.info("Exception: {}".format(rr))
            pass
        log_obj.info("Execute_mod: {}{}".format(execute_mod, module_list))
    return execute_mod, module_list


# Argparse
parser = argparse.ArgumentParser(description='Parse script required arguments')
parser.add_argument("--script-path", help="provide required script name", type=str, nargs='+',
                    required=False, default=None)  # action='append' or nargs='*'
parser.add_argument("--email", help="provide email-id", type=str,
                    required=False, default=None)
args = parser.parse_args()
final_log_send_mail_id = None
list_send = []
if args.script_path is not None:
    list_send.append(args.script_path)
    file_name = args.script_path
    if isinstance(file_name, list):
        file_name_append = []
        for i in file_name:
            m1 = re.search(r',', i)
            if m1 is not None:
                j = i.split(',')
                for k in j:
                    if not re.match(r',', k):
                        if k == '':
                            continue
                        j = re.sub(r'^\s+|\s+$', r'', k)
                        file_name_append.append(j)
                    else:
                        continue
            else:
                file_name_append.append(i)
        for index, each_list_ind in enumerate(file_name_append):
            module_map.update({'argparse_file_%s' % (index): each_list_ind})
    elif isinstance(file_name, str):
        module_map.update({'argparse_file': file_name})
if args.email is not None:
    def _email(domain, em_domain_length, *args, **kwargs):
        enable_e = False
        # Matching and displaying the result accordingly
        if em_domain_length > 63 or em_domain_length < 2:
            print("According to domain rule Domain length should lie between 3 and 63".format())
            enable_e = False
        elif re.match(r"^-.*|.*-$", domain, re.M | re.I):
            print("Domain name can't start or end with -\n".format())
            enable_e = False
        elif re.match(r"^\d+", domain, re.M | re.I):
            print("Domain Name can't start with Digit\n".format())
            enable_e = False
        else:
            enable_e = True
        return enable_e

    pat = r"^([a-zA-Z][\w\_\.]{3,50})\@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,4})$"
    send_mail_id = re.match(pat, args.email, re.M | re.I)
    if send_mail_id is not None:
        domain = send_mail_id.group(2)
        em_domain_length = len(domain)
        enable_valid = _email(domain, em_domain_length)
        if enable_valid:
            log_obj.info("Email-id is: {}".format(send_mail_id.group()))
            final_log_send_mail_id = send_mail_id.group()
else:
    log_obj.info("Email-id is: {}".format(args.email))
ret_kwargs = None
kwargs_for_table = {'log_obj': log_obj}

send_file, list_send = top_table(**kwargs_for_table)
obj = MuthukumarDbExecuteTest(import_mod_name=list_send)
ret_code, file_key, ver = obj.get_version_DB()
if ret_code:
    log_obj.info("Exec File '{}' Current version is \"{}\" ".format(file_key, ver))
else:
    log_obj.info("Could not found version".format())

# Executable module import and run
ret_c, ret_dict = obj.execute_file_import()
if ret_c is False:
    log_obj.error("Unable to import given module, so could you please check once!!!.".format())
else:
    try:
        ret_dict.update(kwargs_for_table)
        ret_dict.update({'send_file': send_file})
        ret_cond, ret_test = obj.test(obj, **ret_dict)
        if ret_cond:
            log_obj = ret_test.get('log_obj')
            ret_kwargs = ret_test.get('ret_kwargs')
    except Exception as err_test:
        log_obj.error("Unable to execute Func--> test!!! {}.".format(err_test))
# get version list
obj.table_for_version(**kwargs_for_table)

# Total execution time
ending_timestamp = datetime.now()
end_time = str(ending_timestamp)
total_time, t1, t2 = user_lib_obj.get_execution_time(start_time, end_time)
obj.table_for_execution(total_time, **kwargs_for_table)

log_obj.info("**************** END ****************".format())
# Clearing file handler
log_obj.handlers.clear()

# ================== Sending an email with all the attachments ===================
em_kwargs = {'send_all_file': True, 'user_email': final_log_send_mail_id}
if final_log_send_mail_id is None:
    print("Email-id not provided so we are skipping sending the entire log!.")
else:
    # Send all log
    e_ret = object_email.Muthu_email(obj, **em_kwargs)
    if not e_ret:
        print("Issues observed while validating Muthu_email".format())
    else:
        print("Successfully sent the entire log message to provided e-mail...")
# =============================================================================

# TODO
# cleanup html log(s)
# obj.cleanup_html_log()
