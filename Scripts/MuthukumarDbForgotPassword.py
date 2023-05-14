"""
    Class MuthukumarDbForgotPassword is used to generate OTP and send that OTP to user/admin either sms or email-id.
    Then we are resting or changing old password for admin/user.

    HISTORY
    - 2019.01.27.01 - Muthukumar Subramanian
        * Initial release
    - v2019.07.14.01 - Muthukumar Subramanian
        * Added logger support
"""

import threading
import time
import pdb
import random
import base64
import pyotp
import sys
import re
from datetime import datetime
# ============== Database import ==========================
from MuthukumarDb import *
# =========================================================
# ============= Muthu_email for send an email =============
from MuthukumarEmail import *
# =========================================================
# ======= Muthu_sms for send a sms to admin mobile ========
from MuthukumarSms import *
# =========================================================

__version__ = "2019.07.14.01"
__author__ = "Muthukumar Subramanian"


class MuthukumarDbForgotPassword(MuthukumarDb, MuthukumarEmail, MuthukumarSms):
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
        admin/user password reset/change here
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: kwargs
        """
        u_name = None
        e_mail = None
        m_num = None
        d_birth = None
        cr_pass = None
        either_admin_user = None
        either_admin_user_get = None
        either_change_reset = None
        time_for_expire = 180
        totp = pyotp.TOTP('base32secret3232', interval=time_for_expire)
        global exitFlag
        exitFlag = None
        global otp_success
        otp_success = False
        global gen_otp
        gen_otp = None
        password_change_enable = False
        password_reset_enable = False
        forgot_password_option = None
        e_mail_send = False
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        admin_log = 'MUTHUKUMAR_DB_FORGOT_PASSWORD_LOG'
        (ok, self.log_obj) = self.user_lib_obj.Create_dir(file_name=admin_log, logger_enabled=True, add_handler=True)

        self.log_obj.info("***** Forgot password page start *****".format())
        self.log_obj.info("***** Are you change your password please select[1]\n"
                          "Are you reset your password please select[2] *****".format())
        while True:
            select_option = (sys.stdin.readline())
            select_option = select_option.strip()
            self.log_obj.info("Selected option is: {}".format(select_option))
            try:
                either_change_reset = int(select_option)
            except ValueError as err:
                pass
            if either_change_reset == 1:
                forgot_password_option = "change"
                self.log_obj.info("Password will {}".format(forgot_password_option))
                password_change_enable = True
                break
            elif either_change_reset == 2:
                forgot_password_option = "reset"
                self.log_obj.info("Password will {}".format(forgot_password_option))
                password_reset_enable = True
                break
            else:
                either_change_reset = None
                self.log_obj.warning("Given option is invalid!!!".format())
                break
        if either_change_reset is not None:
            self.log_obj.info("***** Selected categories to change/reset password: User_Table[1]"
                              " Admin_Table[2]*****".format())
            while True:
                table_option = (sys.stdin.readline())
                table_option = table_option.strip()
                try:
                    either_admin_user_get = int(table_option)
                except ValueError as err:
                    pass
                if either_admin_user_get == 1:
                    either_admin_user = 'USER'
                    get_input = {'login_type': either_admin_user, 'user_table_name': 'USER_TABLE'}
                    self.log_obj.info("User password will {}".format(forgot_password_option))
                    break
                elif either_admin_user_get == 2:
                    either_admin_user = 'ADMIN'
                    get_input = {'login_type': either_admin_user, 'admin_table_name': 'ADMIN_TABLE'}
                    self.log_obj.info("Admin password will {}".format(forgot_password_option))
                    break
                else:
                    get_input = None
                    self.log_obj.warning("Admin/User gave an invalid option!!!".format())
                    break

            if either_admin_user is not None:

                # USER NAME
                self.log_obj.info("Enter user name: [Alphabet character only allowed, "
                                  "minimum 3 character to maximum 20 chracter]".format())
                user_username = (sys.stdin.readline())
                (ret, u_name) = self.user_username_validate(_input_username=user_username)
                if ret is False:
                    self.log_obj.error("Issues observed while validating username".format())

                # EMAIL-ID
                self.log_obj.info("Enter email-id: [Alphabet character,numbers and "
                                  "special characters [ '-' and/or '.' ] are allowed]\nExample: "
                                  "abcd_5.kum@gmail.com, noreplymuthukumar@gmail.com".format())
                user_email = (sys.stdin.readline())
                (ret, e_mail) = self.user_email_validate(_input_email=user_email)
                if ret is False:
                    self.log_obj.error("Issues observed while validating email".format())

                # MOBILE NUMBER
                self.log_obj.info("Enter your Mobile Number: country code(2 digit) "
                                  "and Number(10 digit) [xx-xxxxxxxxxx] \nExample : 91-9566067570".format())
                usermobile_number = (sys.stdin.readline())
                (ret, m_num) = self.usermobile_number_validate(_input_mn=usermobile_number)
                if ret is False:
                    self.log_obj.error("Issues observed while validating mobile number".format())

                if either_admin_user == 'USER':
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

                if((d_birth is not None or d_birth != "FAIL") and e_mail != "FAIL" and u_name != "FAIL"):
                    get_input = {'login_type': either_admin_user, 'dir_obj': self.log_obj}
                    (ok_ret, return_op) = self.User_and_admin_signin(**get_input)

                    save_user_name = None
                    save_email = None
                    save_date_of_birth = None
                    save_password = None
                    exsits_mobile_number = False
                    exsits_user_name = False
                    exsits_email = False
                    exsits_date_of_birth = False
                    password_success = False

                    # Verify mobile number and get data(s) from database
                    if any(m_num in each_num for each_num in return_op.keys()):
                        exsits_mobile_number = True
                        for key, value in return_op.items():
                            if m_num == key:
                                for key_1, value_1 in value.items():
                                    pat_column = ".*(username|adminname)"
                                    pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                                    if pat_column_2 is not None:
                                        db_matched_num = pat_column_2.group()
                                        save_user_name = return_op[m_num][db_matched_num]
                                    pat_email = ".*email"
                                    pat_email_2 = re.match(pat_email, key_1, re.M | re.I)
                                    if pat_email_2 is not None:
                                        db_matched_email = pat_email_2.group()
                                        save_email = return_op[m_num][db_matched_email]
                                    pat_password = "user_password|admin_password"
                                    pat_password_2 = re.match(pat_password, key_1, re.M | re.I)
                                    if pat_password_2 is not None:
                                        db_matched_password = pat_password_2.group()
                                        save_password = return_op[m_num][db_matched_password]
                                    if either_admin_user == 'USER':
                                        pat_date_of_birth = ".*date_of_birth"
                                        pat_date_of_birth_2 = re.match(pat_date_of_birth, key_1, re.M | re.I)
                                        if pat_date_of_birth_2 is not None:
                                            db_matched_db_birth = pat_date_of_birth_2.group()
                                            save_date_of_birth = return_op[m_num][db_matched_db_birth]
                        self.log_obj.info("Given mobile number is {} exists on Database".format(m_num))

                        # Verify user name
                        if u_name == save_user_name:
                            exsits_user_name = True
                            self.log_obj.info("Given user_name is {} exists on Database".format(u_name))
                        else:
                            self.log_obj.error("Given user_name is {} does't exist on Database".format(u_name))

                        # Verify email
                        if e_mail == save_email:
                            exsits_email = True
                            self.log_obj.info("Given email is {} exists on Database".format(e_mail))
                        else:
                            self.log_obj.error("Given email is {} does't exist on Database".format(e_mail))
                        if either_admin_user == 'USER':
                            # Verify date of birth
                            if d_birth == save_date_of_birth:
                                exsits_date_of_birth = True
                                self.log_obj.info("Given date of birth is {} exists on Database".format(d_birth))
                            else:
                                self.log_obj.error("Given date of birth is {} does't exist on Database".format(d_birth))
                    else:
                        self.log_obj.error("Given mobile number is {} does't exist on Database".format(m_num))
                    get_password = False
                    if either_admin_user == 'USER':
                        if(exsits_mobile_number is True and exsits_user_name is True
                                and exsits_email is True
                                and exsits_date_of_birth is True):
                            get_password = True
                    else:
                        if(exsits_mobile_number is True and exsits_user_name is True
                           and exsits_email is True):
                            get_password = True
                    if get_password is True:
                        if password_change_enable is True:
                            self.log_obj.info("Enter your old password: [Alphabet character and numbers are allowed, "
                                              "minimum 3 character and maximum 20 "
                                              "chracter]".format())
                            user_password = (sys.stdin.readline())

                            (ret, cr_pass) = self.user_password_validate(_input_pwd=user_password)
                            if ret is False:
                                self.log_obj.error("Issues observed while validating Func--> "
                                                   "user_password_validate".format())

                            if save_password == cr_pass:
                                self.log_obj.info("Given password is {} exists on Database".format(cr_pass))
                                password_success = True
                            else:
                                self.log_obj.error("Given password is {} does't exist on Database".format(cr_pass))
                    else:
                        self.log_obj.error("Given data's are wrong!, so try again forgot password/reset password "
                                           "with correct credential".format())

                    if((password_success is True and password_change_enable is True) or(password_reset_enable is True)
                       and get_password is True):
                        receive_otp = None
                        self.log_obj.info("***** Generated OTP send through your email-id: "
                                          "please select[1]\n Generated OTP send through your mobile number: "
                                          "please select[2] *****".format())
                        either_email_mobile = None
                        while True:
                            select_option = (sys.stdin.readline())
                            select_option = select_option.strip()
                            try:
                                either_email_mobile = int(select_option)
                            except ValueError as err:
                                pass
                            if either_email_mobile == 1:
                                self.log_obj.info("Generated OTP will receive your email-id".format())
                                receive_otp = 'EMAIL'
                                break
                            elif either_email_mobile == 2:
                                self.log_obj.info("Generated OTP will receive your mobile number".format())
                                receive_otp = 'MOBILE_NUMBER'
                                break
                            else:
                                self.log_obj.info("Given option is invalid!!!".format())
                                break
                        if receive_otp is not None:
                            def verify_otp(*args, **kwargs):
                                """
                                ..codeauthor:: Muthukumar Subramanian
                                verifying generated otp here
                                Usage:
                                    Required argument(s):
                                        :param kwargs: required 'obj' otp object
                                    Optional argument(s):
                                        :param args: default list
                                """
                                totp_key = kwargs.get('obj')
                                start_timestamp = datetime.now()
                                start_time = str(start_timestamp)
                                while True:
                                    collected_otp = (sys.stdin.readline())
                                    collected_otp = collected_otp.strip()
                                    ending_timestamp = datetime.now()
                                    end_time = str(ending_timestamp)
                                    total_time, t1, t2 = self.user_lib_obj.get_execution_time(start_time, end_time)
                                    total_time = str(total_time)
                                    time_sec_convert = sum(
                                        x * int(t) for x, t in zip([3600, 60, 1], total_time.split(":")))
                                    time_sec_convert_int = int(time_sec_convert)
                                    if time_sec_convert_int >= 180 and collected_otp == '':
                                        collected_otp = None
                                        break
                                    if collected_otp != '':
                                        break

                                global exitFlag
                                global otp_success
                                # OTP verified for current time
                                pass_OTP = totp_key.verify(collected_otp, valid_window=1)  # => True
                                if pass_OTP:
                                    self.log_obj.info("OTP is verified successfully: {}".format(pass_OTP))
                                    exitFlag = True
                                    otp_success = True
                                    return True
                                else:
                                    self.log_obj.error("OTP verification is failed: {}".format(collected_otp))
                                    exitFlag = True
                                    return False

                            def generate(*args, **kwargs):
                                """
                                ..codeauthor:: Muthukumar Subramanian
                                Generating pyotp key
                                Usage:
                                    Required argument(s):
                                        :param kwargs: required 'obj' otp object
                                    Optional argument(s):
                                        :param args: default list
                                """
                                totp_key = kwargs.get('obj')
                                global gen_otp
                                gen_otp = totp_key.now()
                                self.log_obj.info("Generated OTP: {}".format(gen_otp))
                                return True

                            def countdown():
                                """
                                ..codeauthor:: Muthukumar Subramanian
                                Displaying countdown time
                                Usage:
                                    Required argument(s):
                                        :param :timeout(global) required timeout value, it is depends on user
                                        :param :exitFlag(global) exit timer countdown
                                    Optional argument(s):
                                        :param args: default list
                                """
                                try:
                                    count_t = time_for_expire
                                    self.log_obj.info("After {} seconds OTP will expire...".format(count_t))
                                    global exitFlag
                                    if count_t:
                                        while count_t >= 0:
                                            if exitFlag:
                                                break
                                            else:
                                                time.sleep(1)
                                                self.log_obj.info("\t {}".format(count_t))
                                                # print(count_t, end='...\r')
                                                count_t -= 1
                                except ValueError as err:
                                    pass

                            def _sms_for_otp(**kwargs):
                                """
                                ..codeauthor:: Muthukumar Subramanian
                                Usage:
                                    Required argument(s):
                                        :param kwargs: default dict, required OTP message,
                                    Optional argument(s):
                                        :param args: default list
                                :return: Boolean
                                """
                                msg = kwargs.get('otp_msg')
                                get_input = {'login_type': either_admin_user, 'forgot_paswd': m_num,
                                             'msg_signup': msg, 'log_obj': self.log_obj, }
                                m_ret = self.Muthu_sms(**get_input)
                                if m_ret is False:
                                    self.log_obj.error("Issues observed while validating Muthu_sms".format())
                                return True

                            def _email_for_otp(**kwargs):
                                """
                                ..codeauthor:: Muthukumar Subramanian
                                Usage:
                                    Required argument(s):
                                        :param kwargs: default dict, required OTP message,
                                    Optional argument(s):
                                        :param args: default list
                                :return: Boolean
                                """
                                msg = kwargs.get('otp_msg')
                                get_input = {'otp_email_msg': msg, 'user_email': e_mail, 'log_obj': self.log_obj}
                                e_ret = self.Muthu_email(**get_input)
                                if e_ret is False:
                                    self.log_obj.error("Issues observed while validating Muthu_email".format())
                                return True

                            dict_k = {'obj': totp}
                            t1 = threading.Thread(target=generate, args=('list'), kwargs=dict_k)
                            t2 = threading.Thread(target=countdown)
                            t4 = threading.Thread(target=verify_otp, kwargs=dict_k)
                            # starting thread 1
                            t1.start()
                            # starting thread 2
                            t2.start()
                            user_name_is = either_admin_user.lower()
                            otp_message = 'Hi %s \n\t %s is the One-Time Password(OTP), you have to %s your password.' \
                                          ' This OTP is usable only once and valid for %s' \
                                          ' minutes/sec from the request...\nThanks,\nAdmin team(Muthu)\n'\
                                % (user_name_is, gen_otp, forgot_password_option, time_for_expire)
                            kwargs_dict = {'otp_msg': otp_message}
                            if receive_otp == 'MOBILE_NUMBER':
                                t3 = threading.Thread(target=_sms_for_otp, kwargs=kwargs_dict)
                                # starting thread 3
                                t3.start()
                                # wait until thread 3 is completely executed
                                t3.join()
                                # starting thread 3
                                t4.start()
                            else:
                                t3 = threading.Thread(target=_email_for_otp, kwargs=kwargs_dict)
                                # starting thread 3
                                t3.start()
                                # wait until thread 3 is completely executed
                                t3.join()
                                # starting thread 4
                                t4.start()
                            # wait until thread 1 is completely executed
                            t1.join()
                            # wait until thread 2 is completely executed
                            t2.join()
                            # wait until thread 4 is completely executed
                            t4.join()
                            if otp_success is True:
                                get_input = {'login_type': either_admin_user, 'log_obj': self.log_obj}
                                (ok_ret, return_op) = self.User_and_admin_signin(**get_input)

                                db_matched_num = None
                                set_num = None
                                which_column = None
                                what_value = None
                                str_which_column = None
                                str_what_value = None
                                for key, value in return_op.items():
                                    if key == m_num:
                                        for key_1, value_2 in value.items():
                                            pat_column = ".*mobile_number"
                                            pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                                            if pat_column_2:
                                                db_matched_num = pat_column_2.group()
                                                set_num = return_op[m_num][db_matched_num]
                                if set_num is None:
                                    self.log_obj.error("Admin entered number is not "
                                                       "found on Data base entry!!!".format())
                                    self.log_obj.info("Try again!!!".format())
                                else:
                                    if either_admin_user == 'USER':
                                        list_str_which_column = ['user_password', 'user_confirm_password']
                                        database_name = 'user_verification'
                                        table_name_db = 'USER_TABLE'
                                    else:
                                        list_str_which_column = ['admin_password', 'admin_confirm_password']
                                        database_name = 'admin_verification'
                                        table_name_db = 'ADMIN_TABLE'
                                    self.log_obj.info("Enter your new password:".format())
                                    user_password = (sys.stdin.readline())
                                    user_password = user_password.strip()
                                    (ret, new_pswd) = self.user_password_validate(_input_pwd=user_password)
                                    if ret is False:
                                        self.log_obj.error("Issues observed while validating Func--> "
                                                           "user_password_validate".format())
                                    if list_str_which_column and new_pswd and new_pswd != 'FAIL':
                                        new_pswd = str(new_pswd)
                                        update_success = True
                                        for each_which_column in list_str_which_column:
                                            query = "UPDATE " + database_name + ".dbo." + table_name_db + \
                                                " SET " + each_which_column + " = \'" + new_pswd + "\' WHERE " \
                                                + db_matched_num + " = \'" + set_num + "\'"
                                            get_input['string_query'] = query
                                            get_input['exec_table_name'] = table_name_db
                                            (ret) = self.Access_query(**get_input)
                                            if ret is False:
                                                self.log_obj.error("Issues observed while "
                                                                   "executing Func--> Access_query".format())
                                                update_success = False
                                        if update_success:
                                            set_db_matched_pass = None
                                            set_db_matched_pass_co = None
                                            get_input['login_type'] = either_admin_user
                                            (ok_ret, return_op) = self.User_and_admin_signin(**get_input)
                                            pat_pass = "admin_password|user_password"
                                            pat_pass_con = "admin_confirm_password|user_confirm_password"
                                            for key, value in return_op.items():
                                                if key == m_num:
                                                    for key_1, value_2 in value.items():
                                                        pat_pass_2 = re.match(pat_pass, key_1, re.M | re.I)
                                                        if pat_pass_2 is not None:
                                                            db_matched_pass = pat_pass_2.group()
                                                            set_db_matched_pass = return_op[m_num][db_matched_pass]
                                                        pat_pass_con_2 = re.match(pat_pass_con, key_1, re.M | re.I)
                                                        if pat_pass_con_2 is not None:
                                                            db_matched_pass_co = pat_pass_con_2.group()
                                                            set_db_matched_pass_co = return_op[m_num][
                                                                db_matched_pass_co]
                                            if(new_pswd == set_db_matched_pass
                                               and new_pswd == set_db_matched_pass_co):
                                                self.log_obj.info("New Password is successfully "
                                                                  "updated on your account".format())
                                                e_mail_send = True
                                            else:
                                                self.log_obj.error("New Password change is failed!!!".format())
                                    else:
                                        self.log_obj.error("New Password change is failed!!!".format())
                            else:
                                self.log_obj.error("Unable to change/reset Password!!!".format())
                else:
                    self.log_obj.error("Forgot password operation is failed!!!".format())

        kwargs = {'log_obj': self.log_obj,
                  'user_email': e_mail,
                  'email_send': e_mail_send,
                  'send_file': admin_log}
        self.log_obj.info("***** Forgot password page end *****".format())

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
                                 "[xx-xxxxxxxxxx] \nExample : 91-9566067570 )".format())
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

    def user_password_validate(self, _input_pwd, *args, **kwargs):
        """
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param _input_pwd: get from sys.stdin.readline
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: password it is True, else FAIL
        """
        pat = r"^([-./@#&+\w]+){3,20}$"
        user_pass = re.match(pat, _input_pwd, re.M | re.I)
        if user_pass:
            self.log_obj.info("It's a valid password: {}".format(user_pass.group()))
            return True, user_pass.group()
        else:
            self.log_obj.info("Entered password is invalid: {}".format(_input_pwd))
            i = 0
            self.log_obj.warning("Try again password (You can give use this format:: "
                                 "[Alphabet character and numbers are allowed, "
                                 "minimum 3 character and maximum 20 chracter]".format())
            while True:
                i = i + 1
                user_pass_2 = (sys.stdin.readline())
                user_pass_3 = re.match(pat, user_pass_2, re.M | re.I)
                if user_pass_3:
                    self.log_obj.info("It's a valid password: {}".format(user_pass_3.group()))
                    return True, user_pass_3.group()
                    break
                else:
                    self.log_obj.info("Entered password is invalid: {}".format(user_pass_2))
                    if i == 2:
                        self.log_obj.warning("This is your last attempt".format())
                    if i >= 3:
                        break
        return False, self.fail
