"""
    Class MuthukumarDbUserSignin is used to signin for user.

    HISTORY
    - 2018.05.19.01 - Muthukumar Subramanian
        * Initial release
    - v2019.07.14.01 - Muthukumar Subramanian
        * Added logger support
"""

import sys
import re
import time

__version__ = "2019.07.14.01"
__author__ = "Muthukumar Subramanian"

# ========================= Database import ===============
from MuthukumarDb import *
# =========================================================


class MuthukumarDbUserSignin(MuthukumarDb):
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
        user signin here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        """
        u_name = None
        m_num = None
        user_email_id = None
        e_mail_send = False
        username_ck = None
        password_ck = None
        mobile_number_ck = None
        cr_pass = None
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        user_log = 'MUTHUKUMAR_DB_USER_SIGN_IN_LOG'
        (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=user_log, logger_enabled=True, add_handler=True)

        self.log_obj.info("***** User SIGNIN page start *****".format())
        # USER NAME
        self.log_obj.info("Enter user name: [Alphabet character only allowed,"
                          " minimum 3 character to maximum 20 chracter]".format())
        username = (sys.stdin.readline())
        (ret, u_name) = self.user_username_validate(_input_username=username)
        if ret is False:
            self.log_obj.error("Issues observed while validating username".format())

        # MOBILE NUMBER
        self.log_obj.info("Enter your Mobile Number: country code(2 digit) "
                          "and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570".format())
        usermobile_number = (sys.stdin.readline())
        (ret, m_num) = self.usermobile_number_validate(_input_mn=usermobile_number)
        if ret is False:
            self.log_obj.error("Issues observed while validating mobile number".format())

        # USER PASSWORD
        self.log_obj.info("Enter your password: [Alphabet character and numbers "
                          "are allowed, minimum 3 character and maximum 20 chracter]".format())
        user_password = (sys.stdin.readline())
        (ret, cr_pass) = self.user_password_validate(_input_pwd=user_password)
        if not ret:
            self.log_obj.error("Issues observed while validating user password".format())

        # Verification
        if u_name == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL":
            self.log_obj.error("Sorry your signin process is failed!!! Try again signin".format())
        else:
            self.log_obj.info("Inprogress your signin ... please wait a moments...".format())
            time.sleep(5)
            kwargs = {'login_type': 'USER', 'skip_table_create': 'SKIP',
                      'log_obj': self.log_obj, 'METHOD': 'signin',
                      'user_table_name': u_name, 'user_username': u_name,
                      'usermobile_number': m_num, 'user_password': cr_pass}
            (ret, ref) = self.Muthu_db(**kwargs)
            if ret is False:
                self.log_obj.error("Error: {}".format(ref))
            else:
                for key, value in ref.items():
                    if key == m_num:
                        mobile_number_ck = True
                        for key2, value2 in value.items():
                            if key2 == 'user_username':
                                if value2 == u_name:
                                    username_ck = True
                            if key2 == 'user_password':
                                if value2 == cr_pass:
                                    password_ck = True
                            if key2 == 'user_email':
                                user_email_id = value2
        if username_ck and password_ck and mobile_number_ck:
            self.log_obj.info("Entered user mobilenumber, username and userpassword are matched.".format())
            e_mail_send = True
        else:
            self.log_obj.error("Entered user mobilenumber, username and userpassword are not matched!!!."
                               " please check your credentials.".format())

        if e_mail_send is True:
            self.log_obj.info("If you want to sending email, please give your option: (Yes/y or No/n)".format())
            loop_count = 0
            while True:
                loop_count = loop_count + 1
                email_skip = (sys.stdin.readline())
                self.log_obj.info("Selected option is: {}".format(email_skip))
                if re.match(r'Yes|y', email_skip, re.M | re.I):
                    self.log_obj.info("Email will send to user Email-id for backup...".format())
                    e_mail_send = True
                    break
                elif re.match(r'No|n', email_skip, re.M | re.I):
                    self.log_obj.info("Email will not send to user Email-id!.".format())
                    e_mail_send = False
                    break
                else:
                    self.log_obj.info("User given option is invalid!!!.".format())
                    e_mail_send = False
                    if loop_count == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if loop_count >= 3:
                        break

            kwargs = {'log_obj': self.log_obj,
                      'user_mobile_num': m_num,
                      'user_email': user_email_id,
                      'email_send': e_mail_send,
                      'send_file': user_log}
        self.log_obj.info("***** User SIGNIN page end *****".format())

        # Remove handler
        if self.log_obj.handlers:
            for index, each_handler in reversed(list(enumerate(self.log_obj.handlers))):
                self.log_obj.removeHandler(self.log_obj.handlers[index])

        return True, kwargs

    def user_username_validate(self, _input_username, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_username: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: username if it is True, else FAIL
        """
        pat = r"^[a-zA-Z0-9\_]{3,20}$"
        user_username = re.match(pat, _input_username, re.M | re.I)
        if user_username:
            self.log_obj.info("Valid user name: {}".format(user_username.group()))
            return True, user_username.group()
        else:
            self.log_obj.info("Entered user name is invalid: {}".format(_input_username))
            i = 0
            self.log_obj.warning("Try again user name (You can give use this format:: "
                                 "[Alphabet character only allowed, minimum 3 character to "
                                 "maximum 20 chracter]".format(_input_username))
            while True:
                i = i + 1
                user_username_2 = (sys.stdin.readline())
                user_username_3 = re.match(pat, user_username_2, re.M | re.I)
                if user_username_3:
                    self.log_obj.info("Valid user name: {}".format(user_username_3.group()))
                    return True, user_username_3.group()
                else:
                    self.log_obj.info("Entered user name is invalid: {}".format(user_username_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def usermobile_number_validate(self, _input_mn, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_mn: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: mobile number if it is True, else FAIL
        """
        pat = r"^(\d{2})-(\d{10})$"
        usermobile_number = re.match(pat, _input_mn, re.M | re.I)
        if usermobile_number:
            self.log_obj.info("Its a valid Mobile Number: {}".format(usermobile_number.group()))
            return True, usermobile_number.group()
        else:
            self.log_obj.info("Entered Mobile Number is Invalid: {}".format(_input_mn))
            self.log_obj.warning("Try again user Mobile Number (You can use this format:: "
                                 "country code(2 digit) and Number(10 digit) [xx-xxxxxxxxxx] "
                                 "Example : 91-9566067570)".format())
            i = 0
            while True:
                i = i + 1
                usermobile_number_2 = (sys.stdin.readline())
                usermobile_number_3 = re.match(pat, usermobile_number_2, re.M | re.I)
                if usermobile_number_3:
                    self.log_obj.info("Its a valid Mobile Number: {}".format(usermobile_number_3.group()))
                    return True, usermobile_number_3.group()
                else:
                    self.log_obj.info("User given mobile number is invalid: {}".format(usermobile_number_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def user_password_validate(self, _input_pwd, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_pwd: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: password if it is True, else FAIL
        """
        pat = r"^([-./@#&+\w]+){3,20}$"
        user_pass = re.match(pat, _input_pwd, re.M | re.I)
        if user_pass:
            self.log_obj.info("Valid password: {}".format(user_pass.group()))
            return True, user_pass.group()
        else:
            self.log_obj.info("Entered password is invalid: {}".format(_input_pwd))
            i = 0
            self.log_obj.warning("Try again password (You can give use this format:: "
                                 "[Alphabet character and numbers are allowed, minimum 3 character "
                                 "and maximum 20 chracter]".format())
            while True:
                i = i + 1
                user_pass_2 = (sys.stdin.readline())
                user_pass_3 = re.match(pat, user_pass_2, re.M | re.I)
                if user_pass_3:
                    self.log_obj.info("Valid user password: {}".format(user_pass_3.group()))
                    return True, user_pass_3.group()
                else:
                    self.log_obj.info("Entered user password is invalid: {}".format(user_pass_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail
