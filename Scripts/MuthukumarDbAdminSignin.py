'''
    Class MuthukumarDbAdminSignin is used to signin for admin.

    HISTORY
    - 2018.05.19.01 - Muthukumar Subramanian
        * Initial release
    - v2018.06.10.01 - Muthukumar Subramanian
        * Added email support for signin page
    - v2019.07.14.01 - Muthukumar Subramanian
        * Added logger support
'''

__version__ = "2019.07.14.01"
__author__ = "Muthukumar Subramanian"
import sys
import re
import time

# ========================= Database import ===============
from MuthukumarDb import *
# =========================================================


class MuthukumarDbAdminSignin(MuthukumarDb):
    def __init__(self, *args, **kwargs):
        self.fail = "FAIL"
        self.log_obj = None
        self.object_db = None
        self.user_lib_obj = None
        if object_db is not None:
            self.object_db = object_db

    def test_run(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        admin signin here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        '''
        u_name = None
        m_num = None
        admin_email_id = None
        e_mail_send = False
        adminname_ck = None
        password_ck = None
        mobile_number_ck = None
        cr_pass = None
        ret_bool = True
        from_admin_access = kwargs.get('from_admin_access', False)
        admin_log = 'MUTHUKUMAR_DB_ADMIN_SIGN_IN_LOG'
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        if from_admin_access is False:
            (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=admin_log, logger_enabled=True,
                                                              add_handler=True)
        else:
            self.log_obj = kwargs.get('log_obj')
        self.log_obj.info("***** Admin SIGNIN page start *****".format())
        # ADMIN NAME
        self.log_obj.info("Enter admin name: [Alphabet character only allowed,"
                          " minimum 3 character to maximum 20 chracter]".format())
        adminname = (sys.stdin.readline())
        (ret, u_name) = self.admin_adminname_validate(_input_adminname=adminname)
        if ret is False:
            self.log_obj.error("Issues observed while validating admin name".format())

        # MOBILE NUMBER
        self.log_obj.info("Enter your Mobile Number: country code(2 digit) "
                          "and Number(10 digit) [xx-xxxxxxxxxx] \nExample : 91-9566067570".format())
        adminmobile_number = (sys.stdin.readline())
        (ret, m_num) = self.adminmobile_number_validate(_input_mn=adminmobile_number)
        if ret is False:
            self.log_obj.error("Issues observed while validating mobile number".format())

        # ADMIN PASSWORD
        self.log_obj.info("Enter your password: [Alphabet character and numbers "
                          "are allowed, minimum 3 character and maximum 20 chracter]".format())
        admin_password = (sys.stdin.readline())
        (ret, cr_pass) = self.admin_password_validate(_input_pwd=admin_password)
        if not ret:
            self.log_obj.error("Issues observed while validating admin password".format())

        # Verification
        if u_name == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL":
            self.log_obj.error("Sorry your signin process is failed!!! Try again signin".format())
        else:
            self.log_obj.info("Inprogress your signin ... please wait a moments...".format())
            time.sleep(5)
            kwargs = {'login_type': 'ADMIN', 'skip_table_create': 'SKIP',
                      'log_obj': self.log_obj, 'METHOD': 'signin',
                      'admin_table_name': u_name, 'admin_adminname': u_name,
                      'adminmobile_number': m_num, 'admin_password': cr_pass}
            (ret, ref) = self.Muthu_db(**kwargs)
            if ret is False:
                self.log_obj.error("Error: {}".format(ref))
            else:
                for key, value in ref.items():
                    if key == m_num:
                        mobile_number_ck = True
                        for key2, value2 in value.items():
                            if key2 == 'admin_adminname':
                                if value2 == u_name:
                                    adminname_ck = True
                            if key2 == 'admin_password':
                                if value2 == cr_pass:
                                    password_ck = True
                            if key2 == 'admin_email':
                                admin_email_id = value2
        if adminname_ck and password_ck and mobile_number_ck:
            self.log_obj.info("Entered admin mobilenumber, adminname and adminpassword are matched.".format())
            e_mail_send = True
        else:
            self.log_obj.error("Entered admin mobilenumber, adminname and adminpassword are not matched!!!. "
                               "please check your credentials.".format())
            ret_bool = False

        if e_mail_send is True and from_admin_access is False:
            self.log_obj.info("If you want to sending email, please give your option: (Yes/y or No/n)".format())
            loop_count = 0
            while True:
                loop_count = loop_count + 1
                email_skip = (sys.stdin.readline())
                self.log_obj.info("Selected option is: {}".format(email_skip))
                if re.match(r'Yes|y', email_skip, re.M | re.I):
                    self.log_obj.info("Email will send to admin Email-id for backup...".format())
                    e_mail_send = True
                    break
                elif re.match(r'No|n', email_skip, re.M | re.I):
                    self.log_obj.info("Email will not send to admin Email-id!.".format())
                    e_mail_send = False
                    break
                else:
                    self.log_obj.info("Admin given option is invalid!!!.".format())
                    e_mail_send = False
                    if loop_count == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if loop_count >= 3:
                        break

            kwargs = {'log_obj': self.log_obj,
                      'admin_mobile_num': m_num,
                      'user_email': admin_email_id,
                      'email_send': e_mail_send,
                      'send_file': admin_log}
        self.log_obj.info("***** Admin SIGNIN page end *****".format())

        # Remove handler
        if from_admin_access is False:
            if self.log_obj.handlers:
                for index, each_handler in reversed(list(enumerate(self.log_obj.handlers))):
                    self.log_obj.removeHandler(self.log_obj.handlers[index])
        return ret_bool, kwargs

    def admin_adminname_validate(self, _input_adminname, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_adminname: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: adminname if it is True, else FAIL
        '''
        pat = r"^[a-zA-Z0-9\_]{3,20}$"
        admin_adminname = re.match(pat, _input_adminname, re.M | re.I)
        if admin_adminname:
            self.log_obj.info("Valid admin name: {}".format(admin_adminname.group()))
            return True, admin_adminname.group()
        else:
            self.log_obj.info("Entered admin name is invalid: {}".format(_input_adminname))
            i = 0
            self.log_obj.warning("Try again admin name (You can give use this format:: "
                                 "[Alphabet character only allowed, minimum 3 character to "
                                 "maximum 20 chracter]".format(_input_adminname))
            while True:
                i = i + 1
                admin_adminname_2 = (sys.stdin.readline())
                admin_adminname_3 = re.match(pat, admin_adminname_2, re.M | re.I)
                if admin_adminname_3:
                    self.log_obj.info("Valid admin name: {}".format(admin_adminname_3.group()))
                    return True, admin_adminname_3.group()
                else:
                    self.log_obj.info("Entered admin name is invalid: {}".format(admin_adminname_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def adminmobile_number_validate(self, _input_mn, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_mn: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: mobile number if it is True, else FAIL
        '''
        pat = r"^(\d{2})-(\d{10})$"
        adminmobile_number = re.match(pat, _input_mn, re.M | re.I)
        if adminmobile_number:
            self.log_obj.info("Its a valid Mobile Number: {}".format(adminmobile_number.group()))
            return True, adminmobile_number.group()
        else:
            self.log_obj.info("Entered Mobile Number is Invalid: {}".format(_input_mn))
            self.log_obj.warning("Try again admin Mobile Number (You can use this format:: "
                                 "country code(2 digit) and Number(10 digit) [xx-xxxxxxxxxx] "
                                 "Example : 91-9566067570)".format())
            i = 0
            while True:
                i = i + 1
                adminmobile_number_2 = (sys.stdin.readline())
                adminmobile_number_3 = re.match(pat, adminmobile_number_2, re.M | re.I)
                if adminmobile_number_3:
                    self.log_obj.info("Its a valid Mobile Number: {}".format(adminmobile_number_3.group()))
                    return True, adminmobile_number_3.group()
                else:
                    self.log_obj.info("Admin given mobile number is invalid: {}".format(adminmobile_number_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def admin_password_validate(self, _input_pwd, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_pwd: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: password if it is True, else FAIL
        '''
        pat = r"^([-./@#&+\w]+){3,20}$"
        admin_pass = re.match(pat, _input_pwd, re.M | re.I)
        if admin_pass:
            self.log_obj.info("Valid password: {}".format(admin_pass.group()))
            return True, admin_pass.group()
        else:
            self.log_obj.info("Entered password is invalid: {}".format(_input_pwd))
            i = 0
            self.log_obj.warning("Try again password (You can give use this format:: "
                                 "[Alphabet character and numbers are allowed, minimum 3 character "
                                 "and maximum 20 chracter]".format())
            while True:
                i = i + 1
                admin_pass_2 = (sys.stdin.readline())
                admin_pass_3 = re.match(pat, admin_pass_2, re.M | re.I)
                if admin_pass_3:
                    self.log_obj.info("Valid admin password: {}".format(admin_pass_3.group()))
                    return True, admin_pass_3.group()
                else:
                    self.log_obj.info("Entered admin password is invalid: {}".format(admin_pass_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail
