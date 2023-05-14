"""
    Class MuthukumarDbUserSignup is used to signup for user.

    HISTORY
    - 2018.03.25.01 - Muthukumar Subramanian
        * Initial release
    - v2019.07.14.01 - Muthukumar Subramanian
        * Added logger support
"""

import sys
import re
import time

__version__ = "2019.07.14.01"
__author__ = "Muthukumar Subramanian"


# ============== Database import ==========================
from MuthukumarDb import *
# =========================================================
# === Muthu_sms for send a sms to user/admin mobile =======
from MuthukumarSms import *
# =========================================================


class MuthukumarDbUserSignup(MuthukumarDb, MuthukumarSms):
    def __init__(self, *args, **kwargs):
        self.fail = "FAIL"
        self.log_obj = None
        self.object_db = None
        self.user_lib_obj = None
        if object_db is not None:
            self.object_db = object_db
        super().__init__(self, *args, **kwargs)

    def test_run(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        user signup here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        """
        f_name = None
        s_name = None
        u_name = None
        e_mail = None
        m_num = None
        d_birth = None
        cr_pass = None
        co_pass = None
        email_send = None
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        user_log = 'MUTHUKUMAR_DB_USER_SIGN_UP_LOG'
        (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=user_log, logger_enabled=True, add_handler=True)

        self.log_obj.info("***** User SIGNUP page start *****".format())
        # FIRST NAME
        self.log_obj.info("Enter first name: [Alphabet character only allowed,"
                          " minimum 3 character to maximum 20 chracter]".format())
        user_firstname = (sys.stdin.readline())
        (ret, f_name) = self.user_firstname_validate(_input_firstname=user_firstname)
        if ret is False:
            self.log_obj.error("Issues observed while validating first name".format())

        # SECOND NAME
        self.log_obj.info("Enter second name: [Alphabet character only allowed, "
                          "minimum 1 character to maximum 20 chracter]".format())
        user_secondname = (sys.stdin.readline())
        (ret, s_name) = self.user_secondname_validate(_input_secondname=user_secondname)
        if ret is False:
            self.log_obj.error("Issues observed while validating second name".format())

        # USER NAME
        self.log_obj.info("Enter user name: [Alphabet character only allowed, "
                          "minimum 3 character to maximum 20 chracter]".format())
        user_username = (sys.stdin.readline())
        (ret, u_name) = self.user_username_validate(_input_username=user_username)
        if ret is False:
            self.log_obj.error("Issues observed while validating username".format())

        # EMAIL-ID
        self.log_obj.info("Enter email-id: [Alphabet character,numbers and "
                          "special characters [ '-' and/or '.' ] are allowed] Example: "
                          "abcd_5.kum@gmail.com, noreplymuthukumar@gmail.com".format())
        user_email = (sys.stdin.readline())
        (ret, e_mail) = self.user_email_validate(_input_email=user_email)
        if ret is False:
            self.log_obj.error("Issues observed while validating email".format())

        # MOBILE NUMBER
        self.log_obj.info("Enter your Mobile Number: country code(2 digit) "
                          "and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570".format())
        usermobile_number = (sys.stdin.readline())
        (ret, m_num) = self.usermobile_number_validate(_input_mn=usermobile_number)
        if ret is False:
            self.log_obj.error("Issues observed while validating mobile number".format())

        # DATE OF BIRTH
        self.log_obj.info("Enter your date of birth: Example- [dd/mm/yyyy] or "
                          "[dd-mm-yyyy] or [dd.mm.yyyy]".format())
        self.log_obj.info("NOTE:- Date of birth is not equal to today or future date!!!".format())

        (a, today_date, c, d) = self.user_lib_obj.Time_Date()
        self.log_obj.info("Today Date: {}".format(today_date))
        userdate_of_birth = (sys.stdin.readline())
        (ret, d_birth) = self.userdate_of_birth_validate(_input_db=userdate_of_birth)
        if ret is False:
            self.log_obj.error("Issues observed while validating date of birth".format())

        # PASSWORD AND CONFIRM PASSWORD
        (ret, cr_pass, co_pass) = self.user_pswd_and_conpswd_validate()
        if ret is False:
            self.log_obj.error("Issues observed while validating password".format())

        # Verification
        if (f_name == "FAIL" or s_name == "FAIL" or u_name == "FAIL" or e_mail == "FAIL" or m_num == "FAIL"
                or d_birth == "FAIL" or cr_pass == "FAIL" or co_pass == "FAIL"):
            self.log_obj.error("Sorry your Signup process is failed !!! Try again signup".format())
        else:
            self.log_obj.info("In progress your signup ... please wait a moments...".format())
            time.sleep(5)
            kwargs = {'login_type': 'USER', 'skip_table_create': 'SKIP', 'log_obj': self.log_obj,
                      'METHOD': 'signup', 'user_table_name': u_name,
                      'user_firstname': f_name, 'user_secondname': s_name,
                      'user_username': u_name, 'user_email': e_mail,
                      'usermobile_number': m_num, 'userdate_of_birth': d_birth,
                      'user_password': cr_pass, 'user_confirm_password': co_pass}
            (ret, ref) = self.Muthu_db(self, *args, **kwargs)
            if ret is False:
                self.log_obj.error("Error: {}".format(ref))
            else:
                email_send = True
        self.log_obj.info("***** User SIGNUP page end *****".format())
        # ===================== Send sms ======================
        if m_num != "FAIL":
            if u_name != "FAIL":
                user_name_is = u_name
            else:
                user_name_is = 'User'
            kwargs = {'login_type': 'USER',
                      'log_obj': self.log_obj,
                      'user_mobile_num': m_num,
                      'user_email': e_mail,
                      'email_send': email_send,
                      'msg_signup': 'Hi' + ' ' + user_name_is +
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

    def user_firstname_validate(self, _input_firstname, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_firstname: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: firstname if it is True, else FAIL
        """
        pat = "^[a-zA-Z]{3,20}$"
        # pat = "muthu" search= match word anywhere but within pattern,
        # match= beginning match
        user_firstname = re.match(pat, _input_firstname, re.M | re.I)
        if user_firstname:
            self.log_obj.info("It's a valid first name: {}".format(user_firstname.group()))
            return True, user_firstname.group()
        else:
            self.log_obj.info("Entered first name is invalid: {}".format(_input_firstname))
            i = 0
            self.log_obj.warning("Try again first name (You can give use this "
                                 "format:: [Alphabet character only allowed, minimum 3 "
                                 "character to maximum 20 chracter]".format())
            while True:
                i = i + 1
                user_firstname_2 = (sys.stdin.readline())
                user_firstname_3 = re.match(pat, user_firstname_2, re.M | re.I)
                if user_firstname_3:
                    self.log_obj.info("It's a valid first name: {}".format(user_firstname_3.group()))
                    return True, user_firstname_3.group()
                else:
                    self.log_obj.info("Entered first name is invalid: {}".format(user_firstname_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def user_secondname_validate(self, _input_secondname, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_secondname: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: secondname if it is True, else FAIL
        """
        pat = "^[a-zA-Z]{1,20}$"
        user_secondname = re.match(pat, _input_secondname, re.M | re.I)
        if user_secondname:
            self.log_obj.info("It's a valid second name: {}".format(user_secondname.group()))
            return True, user_secondname.group()
        else:
            self.log_obj.info("Entered second name is invalid: {}".format(_input_secondname))
            i = 0
            self.log_obj.warning("Try again second name (You can give use this "
                                 "format:: [Alphabet character only allowed, minimum 1 "
                                 "character to maximum 20 chracter]".format())
            while True:
                i = i + 1
                user_secondname_2 = (sys.stdin.readline())
                user_secondname_3 = re.match(pat, user_secondname_2, re.M | re.I)
                if user_secondname_3:
                    self.log_obj.info("It's a valid second name: {}".format(user_secondname_3.group()))
                    return True, user_secondname_3.group()
                else:
                    self.log_obj.info("Entered second name is invalid: {}".format(user_secondname_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

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
            self.log_obj.info("It's a valid user name: {}".format(user_username.group()))
            return True, user_username.group()
        else:
            self.log_obj.info("Entered user name is invalid: {}".format(_input_username))
            i = 0
            self.log_obj.warning("Try again user name (You can give use this "
                                 "format:: [Alphabet character only allowed, minimum 3 "
                                 "character to maximum 20 chracter]".format())
            while True:
                i = i + 1
                user_username_2 = (sys.stdin.readline())
                user_username_3 = re.match(pat, user_username_2, re.M | re.I)
                if user_username_3:
                    self.log_obj.info("It's a valid user name: {}".format(user_username_3.group()))
                    return True, user_username_3.group()
                else:
                    self.log_obj.info("Entered user name is invalid: {}".format(user_username_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

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
        enable_e = None
        # Matching and displaying the result accordingly
        if (em_domain_length > 63 or em_domain_length < 2):
            self.log_obj.warning("According to domain rule Domain length "
                                 "should lie between 3 and 63".format())
            enable_e = False
        elif (re.match(r"^\-.*|.*\-$", domain, re.M | re.I)):
            self.log_obj.warning("Domain name can't start or end with -".format())
            enable_e = False
        elif (re.match(r"^\d+", domain, re.M | re.I)):
            self.log_obj.warning("Domain Name can't start with Digit".format())
            enable_e = False
        else:
            enable_e = True
        return enable_e

    def user_email_validate(self, _input_email, *args, **kwargs):
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
        user_email = re.match(pat, _input_email, re.M | re.I)
        retry_valid = False
        if user_email:
            domain = user_email.group(2)
            em_domain_length = len(domain)
            enable_valid = self._email(domain, em_domain_length)
            if enable_valid:
                self.log_obj.info("It's a valid Email ID: {}".format(user_email.group()))
                return True, user_email.group()
            else:
                retry_valid = True
        else:
            retry_valid = True
        if retry_valid:
            self.log_obj.info("Entered user Email ID is invalid: {}".format(_input_email))
            i = 0
            self.log_obj.warning("Try again email-id (You can give use this "
                                 "format:: [Alphabet character only allowed, minimum 3 "
                                 "character to maximum 50 chracter]".format())
            while True:
                i = i + 1
                retry_valid = False
                enable_valid = False
                user_email_2 = (sys.stdin.readline())
                user_email_3 = re.match(pat, user_email_2, re.M | re.I)
                if user_email_3:
                    domain = user_email_3.group(2)
                    em_domain_length = len(domain)
                    enable_valid = self._email(domain, em_domain_length)
                    retry_valid = True
                else:
                    retry_valid = True
                if retry_valid:
                    if enable_valid:
                        self.log_obj.info("It's a valid Email ID: {}".format(user_email_3.group()))
                        return True, user_email_3.group()
                    else:
                        self.log_obj.info("Entered user Email ID is invalid: {}".format(user_email_2))
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
            self.log_obj.info("It's a valid mobile number: {}".format(usermobile_number.group()))
            return True, usermobile_number.group()
        else:
            self.log_obj.info("Entered mobile number is invalid: {}".format(_input_mn))
            self.log_obj.warning("Try again user mobile number (You can use this "
                                 "format:: country code(2 digit) and number(10 digit) "
                                 "[xx-xxxxxxxxxx] Example : 91-9566067570 )".format())
            i = 0
            while True:
                i = i + 1
                usermobile_number_2 = (sys.stdin.readline())
                usermobile_number_3 = re.match(pat, usermobile_number_2, re.M | re.I)
                if usermobile_number_3:
                    self.log_obj.info("It's a valid mobile number: {}".format(usermobile_number_3.group()))
                    return True, usermobile_number_3.group()
                else:
                    self.log_obj.info("Entered mobile number is invalid: {}".format(usermobile_number_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def userdate_of_birth_validate(self, _input_db, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_db: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: date of birthif it is True, else FAIL
        """
        pat = r"^(3[01]|[12][0-9]|0[1-9])(\-|\.|\/)(1[0-2]|0[1-9])(\-|\.|\/)([0-9]{4})$"
        date_of_birth = re.match(pat, _input_db, re.M | re.I)
        retry_valid = False
        if date_of_birth:
            g_1 = date_of_birth.group(1)
            g_2 = date_of_birth.group(2)
            g_3 = date_of_birth.group(3)
            g_4 = date_of_birth.group(4)
            g_5 = date_of_birth.group(5)

            if (g_2 and (g_2 == '/' or g_2 == '-' or g_2 == '.')):
                g_2 = '/'
            if (g_4 and (g_4 == '/' or g_4 == '-' or g_4 == '.')):
                g_4 = '/'
            final_date_of_birth = g_1 + g_2 + g_3 + g_4 + g_5
            (a, b, date_a, dt) = self.user_lib_obj.Time_Date()
            if final_date_of_birth:
                date_b = dt.strptime(final_date_of_birth, "%d/%m/%Y")
                if date_b < date_a:
                    self.log_obj.info("It's a valid date of birth: {}".format(final_date_of_birth))
                    return True, final_date_of_birth
                else:
                    retry_valid = True
        else:
            retry_valid = True

        if retry_valid:
            self.log_obj.info("Entered date of birth is invalid: {}".format(_input_db))
            self.log_obj.warning("Try again user Date Of Birth (You can give use this "
                                 "format:: [dd/mm/yyyy] or [dd-mm-yyyy] or [dd.mm.yyyy]".format())
            i = 0
            while True:
                i = i + 1
                retry_valid = False
                final_date_of_birth = None
                date_of_birth_2 = (sys.stdin.readline())
                date_of_birth_3 = re.match(pat, date_of_birth_2, re.M | re.I)
                if date_of_birth_3:
                    g_1 = date_of_birth_3.group(1)
                    g_2 = date_of_birth_3.group(2)
                    g_3 = date_of_birth_3.group(3)
                    g_4 = date_of_birth_3.group(4)
                    g_5 = date_of_birth_3.group(5)

                    if (g_2 and (g_2 == '/' or g_2 == '-' or g_2 == '.')):
                        g_2 = '/'
                    if (g_4 and (g_4 == '/' or g_4 == '-' or g_4 == '.')):
                        g_4 = '/'
                    final_date_of_birth = g_1 + g_2 + g_3 + g_4 + g_5
                    retry_valid = True
                else:
                    retry_valid = True
                if retry_valid:
                    (a, b, date_a, dt) = self.user_lib_obj.Time_Date()
                    if final_date_of_birth:
                        date_b = dt.strptime(final_date_of_birth, "%d/%m/%Y")
                        if date_b < date_a:
                            self.log_obj.info("It's a valid date of birth: {}".format(final_date_of_birth))
                            return True, final_date_of_birth
                    else:
                        retry_valid = True
                if retry_valid:
                    self.log_obj.info("Entered date of birth is invalid: {}".format(date_of_birth_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail

    def user_pswd_and_conpswd_validate(self, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: password_cr, password_co it is True, else FAIL
        """
        j = 0
        while True:
            j = j + 1
            if j == 2:
                self.log_obj.warning("Password and confirm password have last attempt".format())
            if j <= 2:
                self.log_obj.info("Enter your password: [Alphabet character "
                                  "and numbers are allowed, minimum 3 character and "
                                  "maximum 20 chracter]".format())
                user_password = (sys.stdin.readline())
                pat = r"^([-./@#&+\w]+){3,20}$"
                user_pass = re.match(pat, user_password, re.M | re.I)
                password_cr = None
                password_co = None
                if user_pass:
                    self.log_obj.info("It's a valid password: {}".format(user_pass.group()))
                    password_cr = user_pass.group()
                else:
                    self.log_obj.info("Entered password is invalid: {}".format(user_password))
                    i = 0
                    self.log_obj.warning("Try again password (You can give use this "
                                         "format:: [Alphabet character and numbers are allowed, "
                                         "minimum 3 character and maximum 20 chracter]".format())
                    while True:
                        i = i + 1
                        user_pass_2 = (sys.stdin.readline())
                        user_pass_3 = re.match(pat, user_pass_2, re.M | re.I)
                        if user_pass_3:
                            self.log_obj.info("It's a valid password: {}".format(user_pass_3.group()))
                            password_cr = user_pass_3.group()
                            break
                        else:
                            self.log_obj.info("Entered user password is invalid: {}".format(user_pass_2))
                            if i == 2:
                                self.log_obj.warning("This is your last attempt".format())
                            if i >= 3:
                                break

                self.log_obj.info("Enter your confirm password: [Alphabet character "
                                  "and numbers are allowed, minimum 3 character and maximum 20 chracter]".format())
                user_confirm_password = (sys.stdin.readline())
                user_confirm_pass = re.match(pat, user_confirm_password, re.M | re.I)
                if user_confirm_pass:
                    self.log_obj.info("It's a valid confirm password: {}".format(user_confirm_pass.group()))
                    password_co = user_confirm_pass.group()
                else:
                    self.log_obj.info("Entered confirm password is invalid: {}".format(user_confirm_password))
                    i = 0
                    self.log_obj.warning("Try again confirm password (You can give use this "
                                         "format:: [Alphabet character and numbers are allowed, minimum "
                                         "3 character and maximum 20 chracter]".format())
                    while True:
                        i = i + 1
                        user_confirm_pass_2 = (sys.stdin.readline())
                        user_confirm_pass_3 = re.match(pat, user_confirm_pass_2, re.M | re.I)
                        if user_confirm_pass_3:
                            self.log_obj.info("It's a valid confirm password: {}".format(user_confirm_pass_3.group()))
                            password_co = user_confirm_pass_3.group()
                            break
                        else:
                            self.log_obj.info("Entered confirm password is invalid: {}".format(user_confirm_pass_2))
                            if i == 2:
                                self.log_obj.warning("This is your last attempt".format())
                            if i >= 3:
                                break
                if (password_cr == password_co and password_cr is not None and password_co is not None):
                    self.log_obj.info("Verified password and confirm password is equal".format())
                    break
                else:
                    self.log_obj.info("Password and confirm password is not equal !!!".format())
            if j >= 3:
                return False, self.fail, self.fail
        return True, password_cr, password_co
