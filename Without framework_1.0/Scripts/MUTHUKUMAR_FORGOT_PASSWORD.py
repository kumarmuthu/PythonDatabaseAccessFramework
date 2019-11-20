# Author: Muthukumar Subramanian
# v2019.01.27.01 - Developed Database_access function for resetting password both user/admin credentials
__author__ = "Muthukumar Subramanian"
import threading
import time
import pdb
import random
import base64
import pyotp
import time
import sys
import re
# ========================= Database import ===============
from MUTHUKUMAR_DB import *
# =========================================================
# ============== Date_time and log print ==================
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
# ============= Muthu_email for send an email =============
from MUTHUKUMAR_EMAIL import *
# =========================================================
# ======= Muthu_sms for send a sms to admin mobile ========
from MUTHUKUMAR_SMS import *
# =========================================================
forgot_pass_log = 'MUTHUKUMAR_APP_FORGOT_PASSWORD_LOG'
(ok, ref_f) = Create_dir(dir_name=forgot_pass_log)
global fail
fail = "FAIL"
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
otp_success = None
global gen_otp
gen_otp = None
password_change_enable = None
password_reset_enable = None
forgot_password_option = None

# ======================= Begin ===========================
print(Log(log_info="***** Are you change your password please select[1]\n "
          "Are you reset your password please select[2] *****\n"))
ref_f.write(Log.ret_mu)
while True:
    select_option = (sys.stdin.readline())
    select_option = select_option.strip()
    try:
        either_change_reset = int(select_option)
    except ValueError as err:
        pass
    if(either_change_reset == 1):
        forgot_password_option = "change"
        print(Log(log_info="Password will {} \n".format(forgot_password_option)))
        ref_f.write(Log.ret_mu)
        password_change_enable = 1
        break
    elif(either_change_reset == 2):
        forgot_password_option = "reset"
        print(Log(log_info="Password will {} \n".format(forgot_password_option)))
        ref_f.write(Log.ret_mu)
        password_reset_enable = 1
        break
    else:
        either_change_reset = None
        print(Log(log_info="Gave an invalid option!!!.\n"))
        ref_f.write(Log.ret_mu)
        break
if(either_change_reset is not None):
    print(Log(log_info="***** Selected categories to change/reset password: User_Table[1] Admin_Table[2]*****\n"))
    ref_f.write(Log.ret_mu)
    while True:
        table_option = (sys.stdin.readline())
        table_option = table_option.strip()
        try:
            either_admin_user_get = int(table_option)
        except ValueError as err:
            pass
        if(either_admin_user_get == 1):
            either_admin_user = 'USER'
            get_input = {'login_type': either_admin_user, 'user_table_name': 'USER_TABLE'}
            print(Log(log_info="User password will {} \n".format(forgot_password_option)))
            ref_f.write(Log.ret_mu)
            break
        elif(either_admin_user_get == 2):
            either_admin_user = 'ADMIN'
            get_input = {'login_type': either_admin_user, 'admin_table_name': 'ADMIN_TABLE'}
            print(Log(log_info="Admin password will {} \n".format(forgot_password_option)))
            ref_f.write(Log.ret_mu)
            break
        else:
            get_input = None
            print(Log(log_info="Admin/User gave an invalid option!!!.\n"))
            ref_f.write(Log.ret_mu)
            break

    if(either_admin_user is not None):
        print(Log(log_info="Enter user name: [Alphabet character only allowed, "
                  "minimum 3 character to maximum 20 character]\n"))
        ref_f.write(Log.ret_mu)
        user_username = (sys.stdin.readline())

        def user_username_validate(_input_username):
            pat = r"^[a-zA-Z0-9\_]{3,20}$"
            user_username = re.match(pat, _input_username, re.M | re.I)
            if user_username:
                print(Log(log_info="Valid user name : " + user_username.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, user_username.group()
            else:
                print(Log(log_info="Entered user name is invalid:" + ' ' + _input_username))
                ref_f.write(Log.ret_mu)
                i = 0
                print(Log(log_info="Try again user name (You can give use this "
                          "format:: [Alphabet character only allowed, minimum 3"
                          " character to maximum 20 character]\n"))
                ref_f.write(Log.ret_mu)
                while True:
                    i = i + 1
                    user_username_2 = (sys.stdin.readline())
                    user_username_3 = re.match(pat, user_username_2, re.M | re.I)
                    if user_username_3:
                        print(Log(log_info="Valid user name : " + user_username_3.group() + "\n"))
                        ref_f.write(Log.ret_mu)
                        return 1, user_username_3.group()
                    else:
                        print(Log(log_info="Entered user name is invalid:" + ' ' + user_username_2))
                        ref_f.write(Log.ret_mu)
                        if(i == 2):
                            print(Log(log_info="This is your last attempt\n"))
                            ref_f.write(Log.ret_mu)
                        if(i >= 3):
                            break
            return 0, fail
        (ret, u_name) = user_username_validate(_input_username=user_username)
        if(not ret):
            print(Log(log_info="Issues observed while validating username\n"))
            ref_f.write(Log.ret_mu)

        print(Log(log_info="Enter email-id: [Alphabet character,numbers "
                  "and special characters [ '-' and/or '.' ] are allowed]"
                  " Example: abcd_5.kum@gmail.com, noreplymuthukumar@gmail.com\n"))
        ref_f.write(Log.ret_mu)
        user_email = (sys.stdin.readline())
        # print(user_email)

        def _email(domain, em_domain_length):
            enable_e = None
            # Matching and displaying the result accordingly
            if(em_domain_length > 63 or em_domain_length < 2):
                print(Log(log_info="According to domain rule Domain length should lie between 3 and 63\n"))
                ref_f.write(Log.ret_mu)
                enable_e = 0
            elif(re.match(r"^\-.*|.*\-$", domain, re.M | re.I)):
                print(Log(log_info="Domain name can't start or end with -\n"))
                ref_f.write(Log.ret_mu)
                enable_e = 0
            elif(re.match(r"^\d+", domain, re.M | re.I)):
                print(Log(log_info="Domain Name can't start with Digit\n"))
                ref_f.write(Log.ret_mu)
                enable_e = 0
            else:
                enable_e = 1

            return enable_e

        def user_email_validate(_input_email):
            pat = r"^([a-zA-Z][\w\_\.]{3,50})\@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,4})$"
            user_email = re.match(pat, _input_email, re.M | re.I)
            retry_valid = 0
            if user_email:
                domain = user_email.group(2)
                em_domain_length = len(domain)
                enable_valid = _email(domain, em_domain_length)
                if enable_valid:
                    print(Log(log_info="Its a valid Email ID : " + user_email.group() + "\n"))
                    ref_f.write(Log.ret_mu)
                    return 1, user_email.group()
                else:
                    retry_valid = 1
            else:
                retry_valid = 1
            if(retry_valid):
                print(Log(log_info="Entered user Email ID is invalid:" + ' ' + _input_email))
                ref_f.write(Log.ret_mu)
                i = 0
                print(Log(log_info="Try again email-id (You can give use this "
                          "format:: [Alphabet character only allowed, minimum 3 "
                          "character to maximum 50 character]\n"))
                ref_f.write(Log.ret_mu)
                while True:
                    i = i + 1
                    retry_valid = 0
                    enable_valid = 0
                    user_email_2 = (sys.stdin.readline())
                    user_email_3 = re.match(pat, user_email_2, re.M | re.I)
                    if user_email_3:
                        domain = user_email_3.group(2)
                        em_domain_length = len(domain)
                        enable_valid = _email(domain, em_domain_length)
                        retry_valid = 1
                    else:
                        retry_valid = 1
                    if(retry_valid):
                        if enable_valid:
                            print(Log(log_info="Its a valid Email ID : " + user_email_3.group() + "\n"))
                            ref_f.write(Log.ret_mu)
                            return 1, user_email_3.group()
                        else:
                            print(Log(log_info="Entered user Email ID is invalid:" + ' ' + user_email_2))
                            ref_f.write(Log.ret_mu)
                            if(i == 2):
                                print(Log(log_info="This is your last attempt\n"))
                                ref_f.write(Log.ret_mu)
                            if(i >= 3):
                                break

            return 0, fail
        (ret, e_mail) = user_email_validate(_input_email=user_email)
        if(not ret):
            print(Log(log_info="Issues observed while validating email\n"))
            ref_f.write(Log.ret_mu)

        print(Log(log_info="Enter your Mobile Number: country code(2 digit) "
                  "and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570 \n"))
        ref_f.write(Log.ret_mu)
        usermobile_number = (sys.stdin.readline())
        # print(usermobile_number)

        def usermobile_number_validate(_input_mn):
            pat = r"^(\d{2})-(\d{10})$"
            usermobile_number = re.match(pat, _input_mn, re.M | re.I)
            if usermobile_number:
                print(Log(log_info="Its a valid Mobile Number :" + usermobile_number.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, usermobile_number.group()
            else:
                print(Log(log_info="Entered Mobile Number is Invalid:" + ' ' + _input_mn))
                ref_f.write(Log.ret_mu)
                print(Log(log_info="Try again user Mobile Number (You can use this "
                          "format:: country code(2 digit) and Number(10 digit) "
                          "[xx-xxxxxxxxxx] Example : 91-9566067570 )\n"))
                ref_f.write(Log.ret_mu)
                i = 0
                while True:
                    i = i + 1
                    usermobile_number_2 = (sys.stdin.readline())
                    usermobile_number_3 = re.match(pat, usermobile_number_2, re.M | re.I)
                    if usermobile_number_3:
                        print(Log(log_info="Its a valid Mobile Number :" + usermobile_number_3.group() + "\n"))
                        ref_f.write(Log.ret_mu)
                        return 1, usermobile_number_3.group()
                    else:
                        print(Log(log_info="User given mobile number is invalid:" + ' ' + usermobile_number_2))
                        ref_f.write(Log.ret_mu)
                        if(i == 2):
                            print(Log(log_info="This is your last attempt\n"))
                            ref_f.write(Log.ret_mu)
                        if(i >= 3):
                            break
            return 0, fail
        (ret, m_num) = usermobile_number_validate(_input_mn=usermobile_number)
        if(not ret):
            print(Log(log_info="Issues observed while validating mobile number\n"))
            ref_f.write(Log.ret_mu)

        if(either_admin_user == 'USER'):
            print(Log(log_info="Enter your date of birth: Example- [dd/mm/yyyy] or [dd-mm-yyyy] or [dd.mm.yyyy]\n"))
            ref_f.write(Log.ret_mu)
            print(Log(log_info="NOTE:- Date of birth is not equal to today or future date!!!\n"))
            ref_f.write(Log.ret_mu)
            (a, today_date, c, d) = Time_Date()
            print(Log(log_info="Today Date : " + today_date + "\n"))
            ref_f.write(Log.ret_mu)
            userdate_of_birth = (sys.stdin.readline())

            def userdate_of_birth_validate(_input_db):
                pat = r"^(3[01]|[12][0-9]|0[1-9])(\-|\.|\/)(1[0-2]|0[1-9])(\-|\.|\/)([0-9]{4})$"
                date_of_birth = re.match(pat, _input_db, re.M | re.I)
                retry_valid = 0
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
                    (a, b, date_a, dt) = Time_Date()
                    if final_date_of_birth:
                        date_b = dt.strptime(final_date_of_birth, "%d/%m/%Y")
                        if(date_b < date_a):
                            print(Log(log_info="Its a valid Date Of Birth :" + final_date_of_birth + "\n"))
                            ref_f.write(Log.ret_mu)
                            return 1, final_date_of_birth
                        else:
                            retry_valid = 1
                else:
                    retry_valid = 1

                if(retry_valid):
                    print(Log(log_info="Entered Date Of Birth is invalid:" + ' ' + _input_db + "\n"))
                    ref_f.write(Log.ret_mu)
                    print(Log(log_info="Try again user Date Of Birth (You can give use this "
                              "format:: [dd/mm/yyyy] or [dd-mm-yyyy] or [dd.mm.yyyy]\n"))
                    ref_f.write(Log.ret_mu)
                    i = 0
                    while True:
                        i = i + 1
                        retry_valid = 0
                        final_date_of_birth = 0
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
                            retry_valid = 1
                        else:
                            retry_valid = 1
                        if(retry_valid):
                            (a, b, date_a, dt) = Time_Date()
                            if final_date_of_birth:
                                date_b = dt.strptime(final_date_of_birth, "%d/%m/%Y")
                                if(date_b < date_a):
                                    print(Log(log_info="Its a valid Date Of Birth :" + final_date_of_birth + "\n"))
                                    ref_f.write(Log.ret_mu)
                                    return 1, final_date_of_birth
                            else:
                                retry_valid = 1
                        if(retry_valid):
                            print(Log(log_info="Entered Date Of Birth is invalid:" + ' ' + date_of_birth_2 + "\n"))
                            ref_f.write(Log.ret_mu)
                            if(i == 2):
                                print(Log(log_info="This is your last attempt\n"))
                                ref_f.write(Log.ret_mu)
                            if(i >= 3):
                                break
                return 0, fail
            (ret, d_birth) = userdate_of_birth_validate(_input_db=userdate_of_birth)
            if(not ret):
                print(Log(log_info="Issues observed while validating Date Of Birth\n"))
                ref_f.write(Log.ret_mu)

        if((d_birth is not None or d_birth != "FAIL") and e_mail != "FAIL" and u_name != "FAIL"):
            get_input = {'login_type': either_admin_user, 'dir_obj': ref_f}
            (ok_ret, return_op) = User_and_admin_signin(**get_input)

            save_user_name = fail
            save_email = fail
            save_date_of_birth = fail
            save_password = fail
            exsits_mobile_number = fail
            exsits_user_name = fail
            exsits_email = fail
            exsits_date_of_birth = fail
            password_success = None
            # Verify mobile number
            if any(m_num in each_num for each_num in return_op.keys()):
                exsits_mobile_number = 1
                for key, value in return_op.items():
                    if(m_num == key):
                        for key_1, value_1 in value.items():
                            pat_column = ".*(username|adminname)"
                            pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                            if(pat_column_2 is not None):
                                db_matched_num = pat_column_2.group()
                                save_user_name = return_op[m_num][db_matched_num]
                            pat_email = ".*email"
                            pat_email_2 = re.match(pat_email, key_1, re.M | re.I)
                            if(pat_email_2 is not None):
                                db_matched_email = pat_email_2.group()
                                save_email = return_op[m_num][db_matched_email]
                            pat_password = "user_password|admin_password"
                            pat_password_2 = re.match(pat_password, key_1, re.M | re.I)
                            if(pat_password_2 is not None):
                                db_matched_password = pat_password_2.group()
                                save_password = return_op[m_num][db_matched_password]
                            if(either_admin_user == 'USER'):
                                pat_date_of_birth = ".*date_of_birth"
                                pat_date_of_birth_2 = re.match(pat_date_of_birth, key_1, re.M | re.I)
                                if(pat_date_of_birth_2 is not None):
                                    db_matched_db_birth = pat_date_of_birth_2.group()
                                    save_date_of_birth = return_op[m_num][db_matched_db_birth]
                print(Log(log_info="Given mobile number is {} exists on Data base\n".format(m_num)))
                ref_f.write(Log.ret_mu)
                # Verify user name
                if(u_name == save_user_name):
                    exsits_user_name = 1
                    print(Log(log_info="Given user_name is {} exists on Data base\n".format(u_name)))
                    ref_f.write(Log.ret_mu)
                else:
                    print(Log(log_info="Given user_name is {} does't exist on Data base\n".format(u_name)))
                    ref_f.write(Log.ret_mu)
                # Verify email
                if(e_mail == save_email):
                    exsits_email = 1
                    print(Log(log_info="Given email is {} exists on Data base\n".format(e_mail)))
                    ref_f.write(Log.ret_mu)
                else:
                    print(Log(log_info="Given email is {} does't exist on Data base\n".format(e_mail)))
                    ref_f.write(Log.ret_mu)
                if(either_admin_user == 'USER'):
                    # Verify date of birth
                    if(d_birth == save_date_of_birth):
                        exsits_date_of_birth = 1
                        print(Log(log_info="Given date of birth is {} exists on Data base\n".format(d_birth)))
                        ref_f.write(Log.ret_mu)
                    else:
                        print(Log(log_info="Given date of birth is {} does't exist on Data base\n".format(d_birth)))
                        ref_f.write(Log.ret_mu)
            else:
                print(Log(log_info="Given mobile number is {} does't exist on Data base\n".format(m_num)))
                ref_f.write(Log.ret_mu)
            get_password = None
            if(either_admin_user == 'USER'):
                if(exsits_mobile_number != 'FAIL' and exsits_user_name != 'FAIL'
                        and exsits_email != 'FAIL'
                        and exsits_date_of_birth != 'FAIL'):
                    get_password = 1
            else:
                if(exsits_mobile_number != 'FAIL' and exsits_user_name != 'FAIL'
                   and exsits_email != 'FAIL'):
                    get_password = 1
            if(get_password is not None):
                if(password_change_enable == 1):
                    print(Log(log_info="Enter your old password: [Alphabet character and "
                              "numbers are allowed, minimum 3 character and maximum 20 "
                              "chracter]\n"))
                    ref_f.write(Log.ret_mu)
                    user_password = (sys.stdin.readline())

                    def user_password_validate(_input_pwd):
                        pat = r"^([-./@#&+\w]+){3,20}$"
                        user_pass = re.match(pat, user_password, re.M | re.I)
                        if user_pass:
                            print(Log(log_info="Valid password : " + user_pass.group() + "\n"))
                            ref_f.write(Log.ret_mu)
                            return 1, user_pass.group()
                        else:
                            print(Log(log_info="Entered old password is invalid:" + ' ' + _input_pwd))
                            ref_f.write(Log.ret_mu)
                            i = 0
                            print(Log(log_info="Try again old password (You can give use this format:: "
                                      "[Alphabet character and numbers are allowed, minimum 3 "
                                      "character and maximum 20 chracter]\n"))
                            ref_f.write(Log.ret_mu)
                            while True:
                                i = i + 1
                                user_pass_2 = (sys.stdin.readline())
                                user_pass_3 = re.match(pat, user_pass_2, re.M | re.I)
                                if user_pass_3:
                                    print(Log(log_info="Valid old password : " + user_pass_3.group() + "\n"))
                                    ref_f.write(Log.ret_mu)
                                    return 1, user_pass_3.group()
                                    break
                                else:
                                    print(Log(log_info="Entered old password is invalid:" + ' ' + user_pass_2))
                                    ref_f.write(Log.ret_mu)
                                    if(i == 2):
                                        print(Log(log_info="This is your last attempt\n"))
                                        ref_f.write(Log.ret_mu)
                                    if(i >= 3):
                                        break
                        return 0, fail
                    (ret, cr_pass) = user_password_validate(_input_pwd=user_password)
                    if(not ret):
                        print(Log(log_info="Issues observed while validating old password\n"))
                        ref_f.write(Log.ret_mu)

                    if(save_password == cr_pass):
                        print(Log(log_info="Given password is {} exists on Data base\n".format(cr_pass)))
                        ref_f.write(Log.ret_mu)
                        password_success = 1
                    else:
                        print(Log(log_info="Given password is {} does't exist on Data base\n".format(cr_pass)))
                        ref_f.write(Log.ret_mu)
            else:
                print(Log(log_info="Given data's are wrong!, so try again forgot password/reset password with"
                          " correct credential.\n"))
                ref_f.write(Log.ret_mu)

            if((password_success is not None and password_change_enable == 1) or(password_reset_enable == 1)
               and get_password is not None):
                receive_otp = None
                print(Log(log_info="***** Generated OTP send through your email-id: "
                          "please select[1]\n Generated OTP send through your mobile"
                          " number: please select[2] *****\n"))
                ref_f.write(Log.ret_mu)
                while True:
                    select_option = (sys.stdin.readline())
                    select_option = select_option.strip()
                    try:
                        either_email_mobile = int(select_option)
                    except ValueError as err:
                        pass
                    if(either_email_mobile == 1):
                        print(Log(log_info="Generated OTP will receive your email-id\n"))
                        ref_f.write(Log.ret_mu)
                        receive_otp = 'EMAIL'
                        break
                    elif(either_email_mobile == 2):
                        print(Log(log_info="Generated OTP will receive your mobile number\n"))
                        ref_f.write(Log.ret_mu)
                        receive_otp = 'MOBILE_NUMBER'
                        break
                    else:
                        get_input = None
                        print(Log(log_info="Gave an invalid option!!!.\n"))
                        ref_f.write(Log.ret_mu)
                        break
                if(receive_otp is not None):
                    def verify_otp(*args, **kwargs):
                        totp_key = kwargs['obj'] if kwargs['obj'] else None
                        time.sleep(0.1)
                        collected_otp = (sys.stdin.readline())
                        collected_otp = collected_otp.strip()
                        global exitFlag
                        global otp_success
                        # OTP verified for current time
                        pass_OTP = totp_key.verify(collected_otp, valid_window=1)  # => True
                        if(pass_OTP):
                            print(Log(log_info="OTP is verified successfully: " + str(pass_OTP) + " \n"))
                            ref_f.write(Log.ret_mu)
                            exitFlag = 1
                            otp_success = 1
                            return 1
                        else:
                            print(Log(log_info="OTP verification is failed: " + str(collected_otp) + " \n"))
                            ref_f.write(Log.ret_mu)
                            exitFlag = 1
                            return 0

                    def generate(*args, **kwargs):
                        totp_key = kwargs['obj'] if kwargs['obj'] else None
                        global gen_otp
                        gen_otp = totp_key.now()
                        print(Log(log_info="Generated OTP:" + gen_otp + " \n"))
                        ref_f.write(Log.ret_mu)

                    def countdown():
                        try:
                            count_t = time_for_expire
                            print(Log(log_info="After " + str(count_t) + " seconds OTP will expire... \n"))
                            ref_f.write(Log.ret_mu)
                            global exitFlag
                            if count_t:
                                while count_t >= 0:
                                    if(exitFlag):
                                        break
                                    else:
                                        print(Log(log_info="\t" + str(count_t) + "\n"))
                                        ref_f.write(Log.ret_mu)
                                        # print(count_t, end='...\r')
                                        time.sleep(1)
                                        count_t -= 1
                        except ValueError as err:
                            pass

                    def _sms_for_otp(**kwargs):
                        msg = kwargs.get('otp_msg')
                        # get_input = {'login_type' : 'ADMIN', 'dir_obj' : ref_f,
                        # 'admin_mobile_num' : m_num, 'msg_signup' : 'Hi'+' '+ admin_name_is
                        #  + ',\n\t Thanks for your signup...\nThanks,\nAdmin team(Muthu)\n'}

                        get_input = {'login_type': either_admin_user, 'admin_mobile_num': m_num, 'msg_signup': 'msg'}
                        m_ret = Muthu_sms(**get_input)
                        if(not m_ret):
                            print(Log(log_info="Issues observed while validating Muthu_sms\n"))
                            ref_f.write(Log.ret_mu)
                        return 1

                    def _email_for_otp(**kwargs):
                        msg = kwargs.get('otp_msg')
                        get_input = {'otp_email_msg': msg, 'user_email': e_mail, 'log_dir': forgot_pass_log}
                        e_ret = Muthu_email(**get_input)
                        if(not e_ret):
                            print(Log(log_info="Issues observed while validating Muthu_email\n"))
                            ref_f.write(Log.ret_mu)
                        return 1

                    dict_k = {'obj': totp}
                    t1 = threading.Thread(target=generate, args=('list'), kwargs=dict_k)
                    t2 = threading.Thread(target=countdown)
                    t4 = threading.Thread(target=verify_otp, kwargs=dict_k)
                    # starting thread 1
                    t1.start()
                    # starting thread 2
                    t2.start()
                    user_name_is = either_admin_user.lower()
                    otp_message = 'Hi' + ' ' + user_name_is + ',\n\t ' + str(gen_otp) + \
                        ' is the One-Time Password(OTP) to ' + forgot_password_option +\
                        ' password. This OTP is usable only once and valid for '\
                        + str(time_for_expire) + ' minutes/sec from the request...\nThanks,' \
                        '\nAdmin team(Muthu)\n'
                    kwargs_dict = {'otp_msg': otp_message}
                    if(receive_otp == 'MOBILE_NUMBER'):
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
                    if(otp_success is not None):
                        get_input = {'login_type': either_admin_user, 'dir_obj': ref_f}
                        (ok_ret, return_op) = User_and_admin_signin(**get_input)

                        db_matched_num = None
                        set_num = None
                        which_column = None
                        what_value = None
                        str_which_column = None
                        str_what_value = None
                        for key, value in return_op.items():
                            if(key == m_num):
                                for key_1, value_2 in value.items():
                                    pat_column = ".*mobile_number"
                                    pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                                    if(pat_column_2):
                                        db_matched_num = pat_column_2.group()
                                        set_num = return_op[m_num][db_matched_num]
                        if(set_num is None):
                            print(Log(log_info="Admin entered number is not found on Data base entry!!!\n"))
                            ref_f.write(Log.ret_mu)
                            print(Log(log_info="Try again!!!\n"))
                            ref_f.write(Log.ret_mu)
                        else:
                            if(either_admin_user == 'USER'):
                                list_str_which_column = ['user_password', 'user_confirm_password']
                                database_name = 'user_verification'
                                table_name_db = 'USER_TABLE'
                            else:
                                list_str_which_column = ['admin_password', 'admin_confirm_password']
                                database_name = 'admin_verification'
                                table_name_db = 'ADMIN_TABLE'
                            print(Log(log_info="Enter your new password: \n"))
                            ref_f.write(Log.ret_mu)
                            what_value = (sys.stdin.readline())
                            what_value = what_value.strip()
                            try:
                                str_what_value = str(what_value)
                            except ValueError as err:
                                pass
                            if(list_str_which_column and str_what_value):
                                for str_which_column in list_str_which_column:
                                    query = "UPDATE " + database_name + ".dbo." + table_name_db + \
                                        " SET " + str_which_column + " = \'" + str_what_value + "\' WHERE " \
                                        + db_matched_num + " = \'" + set_num + "\'"
                                    get_input['string_query'] = query
                                    get_input['exec_table_name'] = table_name_db
                                    (ret) = Access_query(**get_input)
                                    if(not ret):
                                        print("Issues observed while executing Func--> Access_query \n")
                                        ref_f.write(Log.ret_mu)
                                    else:
                                        set_db_matched_pass = None
                                        set_db_matched_pass_co = None
                                        (ok_ret, return_op) = User_and_admin_signin(**get_input)
                                        for key, value in return_op.items():
                                            if(key == m_num):
                                                for key_1, value_2 in value.items():
                                                    pat_pass = "admin_password|user_password"
                                                    pat_pass_con = "admin_confirm_password|user_confirm_password"
                                                    pat_pass_2 = re.match(pat_pass, key_1, re.M | re.I)
                                                    if(pat_pass_2 is not None):
                                                        db_matched_pass = pat_pass_2.group()
                                                        set_db_matched_pass = return_op[m_num][db_matched_pass]
                                                    pat_pass_con_2 = re.match(pat_pass_con, key_1, re.M | re.I)
                                                    if(pat_pass_con_2 is not None):
                                                        db_matched_pass_co = pat_pass_con_2.group()
                                                        set_db_matched_pass_co = return_op[m_num][db_matched_pass_co]
                                        if(str_what_value == set_db_matched_pass
                                           and str_what_value == set_db_matched_pass_co):
                                            print(Log(log_info="New Password is successfully "
                                                      "updated on your account\n"))
                                            ref_f.write(Log.ret_mu)
                            else:
                                print(Log(log_info="Try again!!!\n"))
                                ref_f.write(Log.ret_mu)

                            ref_f.close()
# ====================== Send email ===================
                            if(e_mail is not None or e_mail != "FAIL"):
                                get_input = {'user_email': e_mail, 'log_dir': forgot_pass_log}
                                e_ret = Muthu_email(**get_input)
                                if(not e_ret):
                                    print(Log(log_info="Issues observed while validating Muthu_email\n"))
                            else:
                                print(Log(log_info="Unable to send an email to admin email id...! \n"))
# =====================================================
ref_f.close()
# ========================= End page ==================
