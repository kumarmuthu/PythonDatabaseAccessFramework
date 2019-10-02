'''
    Class MuthukumarDbAdminSignup is used to signup for admin.

    HISTORY
    - 2018.03.25.01 - Muthukumar Subramanian
        * Initial release
    - v2018.07.15.01 - Muthukumar Subramanian
        * Added support for admin dedicated/default table CREATE and INSERT query
    - v2019.07.15.01 - Muthukumar Subramanian
        * Added logger support
'''

__version__ = "2019.07.15.01"
__author__ = "Muthukumar Subramanian"

import sys
import re
import time

# ============== Database import ==========================
from MuthukumarDb import *
# =========================================================
# ======= Muthu_sms for send a sms to user mobile =========
from MuthukumarSms import *
# =========================================================


class MuthukumarDbAdminSignup(MuthukumarDb, MuthukumarSms):
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
        admin signup here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        '''
        a_name = None
        e_mail = None
        m_num = None
        cr_pass = None
        co_pass = None
        email_send = None
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        user_log = 'MUTHUKUMAR_DB_ADMIN_SIGN_UP_LOG'
        (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=user_log, logger_enabled=True, add_handler=True)

        self.log_obj.info("***** ADMIN SIGNUP page start *****".format())
        # ADMIN NAME
        self.log_obj.info("Enter admin name: [Alphabet character only allowed, "
                          "minimum 3 character to maximum 20 chracter]".format())
        admin_adminname = (sys.stdin.readline())
        (ret, a_name) = self.admin_adminname_validate(_input_adminname=admin_adminname)
        if ret is False:
            self.log_obj.error("Issues observed while validating adminname".format())

        # ADMIN EMAIL-ID
        self.log_obj.info("Enter email-id: [Alphabet character,numbers "
                          "and special characters [ '-' and/or '.' ] are allowed] "
                          "Example: abcd_5.kum@gmail.com, noreplymuthukumar@gmail.com".format())
        admin_email = (sys.stdin.readline())
        (ret, e_mail) = self.admin_email_validate(_input_email=admin_email)
        if ret is False:
            self.log_obj.error("Issues observed while validating email".format())

        # MOBILE NUMBER
        self.log_obj.info("Enter your Mobile Number: country code(2 digit)"
                          " and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570".format())
        adminmobile_number = (sys.stdin.readline())
        (ret, m_num) = self.adminmobile_number_validate(_input_mn=adminmobile_number)
        if ret is False:
            self.log_obj.error("Issues observed while validating mobile number".format())

        # PASSWORD AND CONFIRM PASSWORD
        j = 0
        while True:
            j = j + 1
            if j == 2:
                self.log_obj.warning("Password and confirm password have last attempt".format())
            if j <= 2:
                self.log_obj.info("Enter your password: [Alphabet character and numbers "
                                  "are allowed, minimum 3 character and maximum 20 chracter]".format())
                admin_password = (sys.stdin.readline())
                pat = r"^([-./@#&+\w]+){3,20}$"
                admin_pass = re.match(pat, admin_password, re.M | re.I)
                password_cr = None
                password_co = None
                if admin_pass:
                    self.log_obj.info("Valid password: {}".format(admin_pass.group()))
                    password_cr = admin_pass.group()
                else:
                    self.log_obj.info("Entered password is invalid: {}".format(admin_password))
                    i = 0
                    self.log_obj.warning("Try again password (You can give use this format:: "
                                         "[Alphabet character and numbers are allowed, minimum 3 "
                                         "character and maximum 20 chracter]".format())
                    while True:
                        i = i + 1
                        admin_pass_2 = (sys.stdin.readline())
                        admin_pass_3 = re.match(pat, admin_pass_2, re.M | re.I)
                        if admin_pass_3:
                            self.log_obj.info("Valid admin password: {}".format(admin_pass_3.group()))
                            password_cr = admin_pass_3.group()
                            break
                        else:
                            self.log_obj.info("Entered admin password is invalid: {}".format(admin_pass_2))
                            if i == 2:
                                self.log_obj.warning("This is your last attempt".format())
                            if i >= 3:
                                break
                self.log_obj.info("Enter your confirm password: [Alphabet character and numbers "
                                  "are allowed, minimum 3 character and maximum 20 chracter]".format())
                admin_confirm_password = (sys.stdin.readline())
                admin_confirm_pass = re.match(pat, admin_confirm_password, re.M | re.I)
                if admin_confirm_pass:
                    self.log_obj.info("Valid confirm password: {}".format(admin_confirm_pass.group()))
                    password_co = admin_confirm_pass.group()
                else:
                    self.log_obj.info("Entered confirm password is invalid: {}".format(admin_confirm_password))
                    i = 0
                    self.log_obj.warning("Try again confirm password (You can give use this format:: "
                                         "[Alphabet character and numbers are allowed, minimum 3 character and "
                                         "maximum 20 chracter]".format())
                    while True:
                        i = i + 1
                        admin_confirm_pass_2 = (sys.stdin.readline())
                        admin_confirm_pass_3 = re.match(pat, admin_confirm_pass_2, re.M | re.I)
                        if admin_confirm_pass_3:
                            self.log_obj.info("Valid confirm password: {}".format(admin_confirm_pass_3.group()))
                            password_co = admin_confirm_pass_3.group()
                            break
                        else:
                            self.log_obj.info("Entered confirm password is invalid: {}".format(admin_confirm_pass_2))
                            if i == 2:
                                self.log_obj.warning("This is your last attempt".format())
                            if i >= 3:
                                break
                if (password_cr == password_co and password_cr is not None and password_co is not None):
                    cr_pass = password_cr
                    co_pass = password_co
                    self.log_obj.info("Verified password and confirm password is equal".format())
                    break
                else:
                    self.log_obj.error("Password and confirm password is not equal!!!".format())
            if j >= 3:
                break

        # verification
        if (a_name == "FAIL" or e_mail == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL" or co_pass == "FAIL"):
            self.log_obj.error("Sorry your Signup process is failed !!! Try again signup".format())
        else:
            self.log_obj.info("Inprogress your signup ... please wait a moments...".format())
            time.sleep(5)
            kwargs = {
                'login_type': 'ADMIN',
                'skip_table_create': 'SKIP',
                'log_obj': self.log_obj,
                'METHOD': 'signup',
                'admin_table_name': a_name,
                'admin_adminname': a_name,
                'admin_email': e_mail,
                'adminmobile_number': m_num,
                'admin_password': cr_pass,
                'admin_confirm_password': co_pass}
            (ret, ref) = self.Muthu_db(**kwargs)
            if ret is False:
                self.log_obj.error("Error: {}".format(ref))
            else:
                email_send = True
        self.log_obj.info("***** Admin SIGNUP page end *****".format())
        # ===================== Send sms ======================
        if m_num != "FAIL":
            if a_name != "FAIL":
                admin_name_is = a_name
            else:
                admin_name_is = 'Admin'
            kwargs = {'login_type': 'ADMIN',
                      'log_obj': self.log_obj,
                      'admin_mobile_num': m_num,
                      'user_email': e_mail,
                      'email_send': email_send,
                      'msg_signup': 'Hi' + ' ' + admin_name_is +
                                    ',\n\t Thanks for your signup...\nThanks,\nAdmin team(Muthu)\n'}
            m_ret = self.Muthu_sms(self, *args, **kwargs)
            if not m_ret:
                self.log_obj.error("Issues observed while validating Muthu_sms".format())
        else:
            self.log_obj.warning("Unable to send a sms to user mobile number...!".format())

        # Remove handler
        if self.log_obj.handlers:
            for index, each_handler in reversed(list(enumerate(self.log_obj.handlers))):
                self.log_obj.removeHandler(self.log_obj.handlers[index])

        return True, kwargs

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
            self.log_obj.warning("Try again admin name (You can give use this "
                                 "format:: [Alphabet character only allowed, minimum 3 "
                                 "character to maximum 20 chracter]".format())
            while True:
                i = i + 1
                admin_adminname_2 = (sys.stdin.readline())
                admin_adminname_3 = re.match(pat, admin_adminname_2, re.M | re.I)
                if admin_adminname_3:
                    self.log_obj.info("Valid admin name:{}".format(admin_adminname_3.group()))
                    return 1, admin_adminname_3.group()
                else:
                    self.log_obj.info("Entered admin name is invalid: {}".format(admin_adminname_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def _email(self, domain, em_domain_length, *args, **kwargs):
        '''
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
        '''
        enable_e = False
        # Matching and displaying the result accordingly
        if(em_domain_length > 63 or em_domain_length < 2):
            self.log_obj.info("According to domain rule Domain length should lie between 3 and 63".format())
            enable_e = False
        elif(re.match(r"^\-.*|.*\-$", domain, re.M | re.I)):
            self.log_obj.info("Domain name can't start or end with -\n".format())
            enable_e = False
        elif(re.match(r"^\d+", domain, re.M | re.I)):
            self.log_obj.info("Domain Name can't start with Digit\n".format())
            enable_e = False
        else:
            enable_e = True
        return enable_e

    def admin_email_validate(self, _input_email, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_email: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: email-id if it is True, else FAIL
        '''
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
            self.log_obj.warning("Try again admin Mobile Number ((You can use this "
                                 "format:: country code(2 digit) and Number(10 digit) "
                                 "[xx-xxxxxxxxxx] Example : 91-9566067570 )".format())
            i = 0
            while True:
                i = i + 1
                adminmobile_number_2 = (sys.stdin.readline())
                adminmobile_number_3 = re.match(pat, adminmobile_number_2, re.M | re.I)
                if adminmobile_number_3:
                    self.log_obj.info("Its a valid Mobile Number: {}".format(adminmobile_number_3.group()))
                    return True, adminmobile_number_3.group()
                else:
                    self.log_obj.info("admin given mobile number is invalid: {}".format(adminmobile_number_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail
