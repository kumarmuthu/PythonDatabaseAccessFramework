"""
    Class MuthukumarDbAdminAccess is used to read|insert|update|delete for admin/user table.
    Operation before we need to login admin authorized credentials used to login, then we can do any operation here.

    HISTORY
    - 2018.05.19.01 - Muthukumar Subramanian
        * Initial release
    - v2019.07.20.01 - Muthukumar Subramanian
        * Added logger support
"""
import sys
import re
# from beautifultable import BeautifulTable
from prettytable import PrettyTable

# ========================= Database import ===============
from MuthukumarDb import *
# =========================================================

__version__ = "2019.07.20.01"
__author__ = "Muthukumar Subramanian"


class MuthukumarDbAdminAccess(MuthukumarDb):
    def __init__(self, *args, **kwargs):
        self.fail = "FAIL"
        self.log_obj = None
        self.object_db = None
        self.user_lib_obj = None
        if object_db is not None:
            self.object_db = object_db
        MuthukumarDb.__init__(self, *args, **kwargs)

    def test_run(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        admin/user table read|insert|update|delete here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        """
        get_input_dict = {}
        e_mail_send = False
        E_mail_send = None
        access_option = None
        int_table_option = None
        selected_query_access = None
        admin_email_id = None
        obj_admin_signin = None
        ret_bool = False
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        admin_log = 'MUTHUKUMAR_DB_ADMIN_ACCESS'
        (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=admin_log, logger_enabled=True, add_handler=True)
        kwargs['log_obj'] = self.log_obj
        self.log_obj.info("***** Admin ACCESS page start *****".format())
        kwargs.update({'from_admin_access': True})
        from MuthukumarDbAdminSignin import MuthukumarDbAdminSignin
        obj_admin_signin = MuthukumarDbAdminSignin()
        ret_bool, ret_ref = obj_admin_signin.test_run(self, *args, **kwargs)
        if ret_bool is False:
            self.log_obj.error("Admin signin is failed!!, so you can't access User_Table and Admin_Table".format())
        else:
            self.log_obj.info("***** Selected table to access Database query: "
                              "User_Table[1] Admin_Table[2]*****".format())
            while_control = True
            while True:
                table_option = (sys.stdin.readline())
                table_option = table_option.strip()
                try:
                    int_table_option = int(table_option)
                except ValueError as err:
                    pass
                if int_table_option == 1:
                    get_input_dict = {'login_type': 'USER', 'user_table_name': 'USER_TABLE'}
                    self.log_obj.info("User_Table will access".format())
                    break
                elif int_table_option == 2:
                    get_input_dict = {'login_type': 'ADMIN', 'admin_table_name': 'ADMIN_TABLE'}
                    self.log_obj.info("Admin_Table will access".format())
                    break
                else:
                    get_input_dict = {}
                    while_control = False
                    self.log_obj.error("Admin gave invalid option!!!".format())
                    break

            count_break = 0
            if while_control:
                self.log_obj.info("Note: Admin Access will denied while using more than 20(tms)".format())
                while True:
                    self.log_obj.info("<<<<<*** Choose your operation ***>>>>>".format())
                    self.log_obj.info("======= SELECT-1 [READ],SELECT-2 [INSERT],SELECT-3 [UPDATE],"
                                      "SELECT-4 [DELETE],SELECT-5 [EXIT] =======".format())
                    int_access_option = None
                    exec_option = {'1': 'read', '2': 'insert', '3': 'update', '4': 'delete', '5': 'exit'}
                    access_option = (sys.stdin.readline())
                    access_option = access_option.strip()
                    try:
                        int_access_option = int(access_option)
                    except ValueError as err:
                        pass
                    count_break = count_break + 1
                    if int_access_option:
                        if ((int_access_option > 5) or (int_access_option == -1) or (int_access_option == 0)):
                            kwargs = {}
                            self.log_obj.info("Selected option is invalid! {}".format(int_access_option))
                            break
                        elif int_access_option == 5:
                            self.log_obj.info("Exiting Database access...".format())
                            break
                        else:
                            query_option_selected = exec_option[str(int_access_option)]
                            get_input_dict['query_option'] = query_option_selected
                            get_input_dict['exec_option'] = exec_option
                            get_input_dict['count_break'] = count_break
                            # Func -> Database_access
                            (ret, ref_dba) = self.Database_access(**get_input_dict)
                            if ret is False:
                                self.log_obj.error("Issues observed while validating Database_access".format())
                                break
                            else:
                                e_mail_send = True
                                if ref_dba == 'break':
                                    break
                    else:
                        break

            if e_mail_send is True:
                self.log_obj.info("If you want to send an email, please give your option: (Yes/y or No/n)".format())
                loop_count = 0
                while True:
                    loop_count = loop_count + 1
                    email_skip = (sys.stdin.readline())
                    self.log_obj.info("Selected option is: {}".format(email_skip))
                    if re.match(r'Yes|y', email_skip, re.M | re.I):
                        self.log_obj.info("Email will send to admin Email-id for backup..."
                                          "\nEnter admin Email-id: ".format())
                        admin_email_id_get = (sys.stdin.readline())
                        admin_email_id_get = admin_email_id_get.strip()
                        ret_bool, admin_email_id = self.admin_email_validate(admin_email_id_get)
                        if ret_bool is True:
                            self.log_obj.info("Entered admin Email-id is: {}".format(admin_email_id))
                        else:
                            admin_email_id = None
                        break
                    elif re.match(r'No|n', email_skip, re.M | re.I):
                        self.log_obj.info("Email will not send to admin Email-id!".format())
                        e_mail_send = False
                        break
                    else:
                        self.log_obj.error("Given option is invalid!!!".format())
                        if loop_count == 2:
                            self.log_obj.warning("This is your last attempt".format())
                        if loop_count >= 3:
                            break

        kwargs = {'log_obj': self.log_obj,
                  'user_email': admin_email_id,
                  'email_send': e_mail_send,
                  'send_file': admin_log}
        kwargs.update(ret_ref)
        self.log_obj.info("***** Admin ACCESS page end *****".format())
        # Remove handler
        if self.log_obj.handlers:
            for index, each_handler in reversed(list(enumerate(self.log_obj.handlers))):
                self.log_obj.removeHandler(self.log_obj.handlers[index])

        return True, kwargs

    def _read_query(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'return_op' database returned output,
                            'login_type' either admin or user table
            Optional argument(s):
                :param args: default list
        :return: Boolean
        """
        return_op = kwargs.get('return_op')
        login_type = kwargs.get('login_type')
        table = PrettyTable()
        LIST_key = []
        LIST_value = []
        LIST_value_final = []
        for key, value in return_op.items():
            for key_1, value_1 in value.items():
                LIST_key.append(key_1)
                LIST_value.append(value_1)
        # removing duplicated column ofget_input_dict['all_query_access'] list
        sordered_key = []
        for i in LIST_key:
            if i not in sordered_key:
                sordered_key.append(i)
        length_column = len(sordered_key)
        # split with DB table column count
        for i in range(0, len(LIST_value), length_column):
            LIST_value_final.append(LIST_value[i:i + length_column])
        table.field_names = sordered_key
        for j in LIST_value_final:
            table.add_row(j)
        # self.log_obj.info("Displaying {} data base Data(s):\n{}".format(login_type, table))
        kwargs.update({'table_obj': table})
        ret = self.user_lib_obj.pretty_table_to_html_table_convertor(**kwargs)
        return True

    def Database_access(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'query_option' which query need to execute on database,
                                'login_type' either admin or user table
            Optional argument(s):
                :param args: default list
        :return: Boolean and break or un-break for while loop termination/proceed further action
        """
        get_input_dict = {}
        query_option = kwargs.get('query_option')
        login_type = kwargs.get('login_type')
        get_input_dict['log_obj'] = self.log_obj
        count_break = kwargs.get('count_break')
        table_name = None
        get_input_dict.update(kwargs)
        text = None
        if login_type == 'USER':
            database_name = 'user_verification'
            table_name = kwargs.get('user_table_name')
        else:
            database_name = 'admin_verification'
            table_name = kwargs.get('admin_table_name')
        (ok_ret, return_op) = self.User_and_admin_signin(**get_input_dict)
        if count_break < 20:
            if query_option == 'read':
                get_input_dict['return_op'] = return_op
                ret_q = self._read_query(**get_input_dict)
                if ret_q is False:
                    self.log_obj.error("Issues observed while executing Func--> _read_query".format())
                self.log_obj.info("***** Admin selected option is : READ ,so next query execution is denied. "
                                  "Login/Run again and continue your access *****".format())
                return True, 'break'

            # ************* INSERT Query execute here *************
            elif query_option == 'insert':
                self.log_obj.info("####### Implement later #######".format())
                # string = "INSERT INTO user_verification.dbo." + user_table_name + \
                # "(user_name,user_password,mobile_number) VALUES ('zxc','zxc','91-0123456789')"

            # ************* UPDATE Query execute here *************
            elif query_option == 'update':
                get_input_dict['return_op'] = return_op
                ret_q = self._read_query(**get_input_dict)
                if ret_q is False:
                    self.log_obj.error("Issues observed while executing Func--> _read_query".format())
                self.log_obj.info("Please enter mobile number to make an update".format())
                finalmobile_number = None
                input_mn = (sys.stdin.readline())
                pat = r"^(\d{2})-(\d{10})$"
                mobile_number = re.match(pat, input_mn, re.M | re.I)
                if mobile_number:
                    self.log_obj.info("Its a valid Mobile Number: {}".format(mobile_number.group()))
                    finalmobile_number = mobile_number.group()
                else:
                    self.log_obj.info("Entered Mobile Number is Invalid: {}".format(input_mn))
                    self.log_obj.warning("Try again Mobile Number ((You can use this format:: country code(2 digit) "
                                         "and Number(10 digit) [xx-xxxxxxxxxx] "
                                         "Example : 91-9566067570 )".format())
                    i = 0
                    while True:
                        i = i + 1
                        mobile_number_2 = (sys.stdin.readline())
                        mobile_number_3 = re.match(pat, mobile_number_2, re.M | re.I)
                        if mobile_number_3:
                            self.log_obj.info("Its a valid Mobile Number: {}".format(mobile_number_3.group()))
                            finalmobile_number = mobile_number_3.group()
                            break
                        else:
                            self.log_obj.error("Given mobile number is invalid: {}".format(mobile_number_2))
                            if i == 2:
                                self.log_obj.warning("This is your last attempt".format())
                            if i >= 3:
                                break
                db_matched_num = None
                set_num = None
                which_column = None
                what_value = None
                str_which_column = None
                str_what_value = None
                for key, value in return_op.items():
                    if key == finalmobile_number:
                        for key_1, value_2 in value.items():
                            pat_column = ".*mobile_number"
                            pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                            if pat_column_2:
                                db_matched_num = pat_column_2.group()
                                set_num = return_op[finalmobile_number][db_matched_num]
                if set_num is None:
                    self.log_obj.error("Admin entered number is not found on Data base entry!!!"
                                       "So try again!!!".format())
                else:
                    self.log_obj.info("Which column need to update!".format())
                    which_column = (sys.stdin.readline())
                    which_column = which_column.strip()
                    try:
                        str_which_column = str(which_column)
                        self.log_obj.info("Selected column is: {}".format(str_which_column))
                    except ValueError as err:
                        pass
                    self.log_obj.info("What value need to replace!".format())
                    what_value = (sys.stdin.readline())
                    what_value = what_value.strip()
                    try:
                        str_what_value = str(what_value)
                        self.log_obj.info("Selected value is: {}".format(str_what_value))
                    except ValueError as err:
                        pass
                    if str_which_column and str_what_value:
                        list_str_which_column = []
                        regx_pswd_u = re.match(r'user_password|user_confirm_password', str_which_column)
                        regx_pswd_a = re.match(r'admin_password|admin_confirm_password', str_which_column)
                        if regx_pswd_u is not None:
                            list_str_which_column = ['user_password', 'user_confirm_password']
                        elif regx_pswd_a is not None:
                            list_str_which_column = ['admin_password', 'admin_confirm_password']
                        else:
                            list_str_which_column.append(str_which_column)
                        update_succ_list = []
                        for each in list_str_which_column:
                            query = "UPDATE %s.dbo.%s SET %s = \'%s\' WHERE %s = \'%s\'" % (database_name, table_name,
                                                                                            each,
                                                                                            str_what_value,
                                                                                            db_matched_num,
                                                                                            set_num
                                                                                            )
                            # query = "UPDATE " + database_name + ".dbo." + table_name + " SET " +
                            # str_which_column + " = \'" + str_what_value + "\' WHERE " +
                            # db_matched_num + " = \'" + set_num + "\'"
                            get_input_dict['string_query'] = query
                            get_input_dict['exec_table_name'] = table_name
                            (ret) = self.Access_query(**get_input_dict)
                            if ret is False:
                                update_succ_list.append(False)
                                self.log_obj.error("Issues observed while executing Func--> Access_query".format())
                            else:
                                update_succ_list.append(True)
                        if all(x is True for x in update_succ_list):
                            (ok_ret, return_op) = self.User_and_admin_signin(**get_input_dict)
                            get_input_dict['return_op'] = return_op
                            ret_q = self._read_query(**get_input_dict)
                            if ret_q is False:
                                self.log_obj.error("Issues observed while executing Func--> _read_query".format())
                    else:
                        self.log_obj.warning("Try again!!!".format())

            # ************* DELETE Query execute here *************
            elif query_option == 'delete':
                # string = "DELETE " + user_table_name + " WHERE mobile_number = '91-0123456789'"
                get_input_dict['return_op'] = return_op
                ret_q = self._read_query(**get_input_dict)
                if ret_q is False:
                    self.log_obj.error("Issues observed while executing Func--> _read_query".format())
                self.log_obj.info("Please enter mobile number to delete a Admin\\User account".format())
                finalmobile_number = None
                input_mn = (sys.stdin.readline())
                pat = r"^(\d{2})-(\d{10})$"
                mobile_number = re.match(pat, input_mn, re.M | re.I)
                if mobile_number:
                    self.log_obj.info("Its a valid Mobile Number: {}".format(mobile_number.group()))
                    finalmobile_number = mobile_number.group()
                else:
                    self.log_obj.info("Entered Mobile Number is Invalid: {}".format(input_mn))
                    self.log_obj.info("Try again Mobile Number ((You can use this format:: country code(2 digit) "
                                      "and Number(10 digit) [xx-xxxxxxxxxx] "
                                      "Example : 91-9566067570 )".format())
                    i = 0
                    while True:
                        i = i + 1
                        mobile_number_2 = (sys.stdin.readline())
                        mobile_number_3 = re.match(pat, mobile_number_2, re.M | re.I)
                        if mobile_number_3:
                            self.log_obj.info("Its a valid Mobile Number: {}".format(mobile_number_3.group()))
                            finalmobile_number = mobile_number_3.group()
                            break
                        else:
                            self.log_obj.info("Given mobile number is invalid: {}".format(mobile_number_2))
                            if i == 2:
                                self.log_obj.info("This is your last attempt".format())
                            if i >= 3:
                                break
                db_matched_num_of_column = None
                set_num = None
                which_column = None
                which_num_del = None
                str_which_column = None
                str_which_num_del = None
                for key, value in return_op.items():
                    if key == finalmobile_number:
                        for key_1, value_2 in value.items():
                            pat_column = ".*mobile_number"
                            pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                            if pat_column_2:
                                db_matched_num_of_column = pat_column_2.group()
                                set_num = return_op[finalmobile_number][db_matched_num_of_column]
                if set_num is None:
                    self.log_obj.info("Admin entered number is not found on Data base entry!!!"
                                      "So try again!!!".format())
                else:
                    self.log_obj.info("Re-enter->>> Which mobile number need to delete!".format())
                    which_num_del = (sys.stdin.readline())
                    which_num_del = which_num_del.strip()
                    try:
                        str_which_num_del = str(which_num_del)
                    except ValueError as err:
                        pass
                    if set_num == str_which_num_del:
                        query = "DELETE %s.dbo.%s WHERE %s = \'%s\'" % (database_name, table_name,
                                                                        db_matched_num_of_column, str_which_num_del)
                        # query = "DELETE " + database_name + ".dbo." + table_name + " WHERE " +
                        # db_matched_num_of_column + " = \'" + str_which_num_del + "\'"
                        get_input_dict['string_query'] = query
                        get_input_dict['exec_table_name'] = table_name
                        (ret) = self.Access_query(**get_input_dict)
                        if ret is False:
                            self.log_obj.error("Issues observed while executing Func--> Access_query".format())
                        else:
                            (ok_ret, return_op) = self.User_and_admin_signin(**get_input_dict)
                            get_input_dict['return_op'] = return_op
                            ret_q = self._read_query(**get_input_dict)
                            if ret_q is False:
                                self.log_obj.error("Issues observed while executing Func--> _read_query".format())
                    else:
                        self.log_obj.error("Miss matched Try again!!!".format())

        elif count_break >= 20:
            self.log_obj.error("***** Access denied while using more than 20(tms) *****".format())
            return True, 'break'

        return True, 'unbreak'

    def _email(self, domain, em_domain_length, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        It is part of user_email_validate function
        Usage:
            Required argument(s):
                :param domain: user_email data
                :param em_domain_length: length of the email
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: Boolean
        """
        enable_e = False
        # Matching and displaying the result accordingly
        if (em_domain_length > 63 or em_domain_length < 2):
            self.log_obj.info("According to domain rule Domain length should lie between 3 and 63".format())
            enable_e = False
        elif (re.match(r"^\-.*|.*\-$", domain, re.M | re.I)):
            self.log_obj.info("Domain name can't start or end with -\n".format())
            enable_e = False
        elif (re.match(r"^\d+", domain, re.M | re.I)):
            self.log_obj.info("Domain Name can't start with Digit\n".format())
            enable_e = False
        else:
            enable_e = True
        return enable_e

    def admin_email_validate(self, _input_email, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_email: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: email-id if it is True, else FAIL
        """
        pat = r"^([a-zA-Z][\w\_\.]{3,50})\@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,4})$"
        admin_email = re.match(pat, _input_email, re.M | re.I)
        retry_valid = False
        if admin_email:
            domain = admin_email.group(2)
            em_domain_length = len(domain)
            enable_valid = self._email(domain, em_domain_length)
            if enable_valid:
                self.log_obj.info("Its a valid Email ID: {}".format(admin_email.group()))
                return True, admin_email.group()
            else:
                retry_valid = True
        else:
            retry_valid = True
        if retry_valid:
            self.log_obj.info("Entered admin Email ID is invalid: {}".format(_input_email))
            i = 0
            self.log_obj.warning("Try again email-id (You can give use this format:: "
                                 "[Alphabet character only allowed, minimum 3 "
                                 "character to maximum 50 chracter]".format())
            while True:
                i = i + 1
                retry_valid = False
                enable_valid = False
                admin_email_2 = (sys.stdin.readline())
                admin_email_3 = re.match(pat, admin_email_2, re.M | re.I)
                if admin_email_3:
                    domain = admin_email_3.group(2)
                    em_domain_length = len(domain)
                    enable_valid = self._email(domain, em_domain_length)
                    retry_valid = True
                else:
                    retry_valid = True
                if retry_valid:
                    if enable_valid:
                        self.log_obj.info("Its a valid Email ID: {}".format(admin_email_3.group()))
                        return True, admin_email_3.group()
                    else:
                        self.log_obj.info("Entered admin Email ID is invalid: {}".format(admin_email_2))
                        if i == 2:
                            self.log_obj.warning("This is your last attempt".format())
                        if i >= 3:
                            break
        return False, self.fail
