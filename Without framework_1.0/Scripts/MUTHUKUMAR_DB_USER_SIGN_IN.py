# Author: Muthukumar Subramanian
# v2018.05.19.01 - Developed user signin funtions
# v2018.05.27.01 - Added lib function 'Create_dir' for log file
# v2018.06.10.01 - Added email support for signin page
__author__ = "Muthukumar Subramanian"
import sys
import re

# ========================= Database import ===============
from MUTHUKUMAR_DB import *
# =========================================================
# ========================= Date_time and log print =======
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
# ================ Muthu_email for send an email ==========
from MUTHUKUMAR_EMAIL import *
# =========================================================
user_log = 'MUTHUKUMAR_APP_USER_SIGNIN_LOG'
(ok, ref_f) = Create_dir(dir_name=user_log)
global fail
fail = "FAIL"
u_name = None
m_num = None
user_email_id = None
E_mail_failed = 1
E_mail_send = None
username_ck = 0
password_ck = 0
mobile_number_ck = 0
cr_pass = fail
print(Log(log_info="***** User SIGNIN page start *****\n"))
ref_f.write(Log.ret_mu)
print(Log(log_info="Enter user name: [Alphabet character only allowed,"
          " minimum 3 character to maximum 20 chracter]\n"))
ref_f.write(Log.ret_mu)
user_username = (sys.stdin.readline())
# print(user_username)


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
                  "format:: [Alphabet character only allowed, minimum 3 "
                  "character to maximum 20 chracter]\n"))
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

print(Log(log_info="Enter your Mobile Number: country code(2 digit) "
          "and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570\n"))
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
                  "[xx-xxxxxxxxxx] Example : 91-9566067570)\n"))
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

print(Log(log_info="Enter your password: [Alphabet character and numbers "
          "are allowed, minimum 3 character and maximum 20 chracter]\n"))
ref_f.write(Log.ret_mu)
user_password = (sys.stdin.readline())


def user_password_validate(_input_pwd):
    pat = r"^([-./@#&+\w]+){3,20}$"
    user_pass = re.match(pat, user_password, re.M | re.I)
    password_cr = None
    password_co = None
    if user_pass:
        print(Log(log_info="Valid password : " + user_pass.group() + "\n"))
        ref_f.write(Log.ret_mu)
        return 1, user_pass.group()
    else:
        print(Log(log_info="Entered password is invalid:" + ' ' + _input_pwd))
        ref_f.write(Log.ret_mu)
        i = 0
        print(Log(log_info="Try again password (You can give use this "
                  "format:: [Alphabet character and numbers are allowed, minimum 3 "
                  "character and maximum 20 chracter]\n"))
        ref_f.write(Log.ret_mu)
        while True:
            i = i + 1
            user_pass_2 = (sys.stdin.readline())
            user_pass_3 = re.match(pat, user_pass_2, re.M | re.I)
            if user_pass_3:
                print(Log(log_info="Valid user password : " + user_pass_3.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, user_pass_3.group()
                break
            else:
                print(Log(log_info="Entered user password is invalid:" + ' ' + user_pass_2))
                ref_f.write(Log.ret_mu)
                if(i == 2):
                    print(Log(log_info="This is your last attempt\n"))
                    ref_f.write(Log.ret_mu)
                if(i >= 3):
                    break
    return 0, fail


(ret, cr_pass) = user_password_validate(_input_pwd=user_password)
if(not ret):
    print(Log(log_info="Issues observed while validating user password\n"))
    ref_f.write(Log.ret_mu)
if(u_name == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL"):
    print(Log(log_info="Sorry your signin process is failed!!! Try again signin\n"))
    ref_f.write(Log.ret_mu)
else:
    print(Log(log_info="Inprogress your signin ... please wait a moments... \n"))
    ref_f.write(Log.ret_mu)
    time.sleep(5)
    get_input = {'login_type': 'USER', 'skip_table_create': 'SKIP',
                 'dir_obj': ref_f, 'METHOD': 'signin',
                 'user_table_name': u_name, 'user_username': u_name,
                 'usermobile_number': m_num, 'user_password': cr_pass}
    (ret, ref) = Muthu_db(**get_input)
    if(not ret):
        print(Log(log_info=ref + "\n"))
        ref_f.write(Log.ret_mu)
    else:
        for key, value in ref.items():
            if(key == m_num):
                mobile_number_ck = 1
                for key2, value2 in value.items():
                    if(key2 == 'user_username'):
                        if(value2 == u_name):
                            username_ck = 1
                    if(key2 == 'user_password'):
                        if(value2 == cr_pass):
                            password_ck = 1
                    if(key2 == 'user_email'):
                        user_email_id = value2
if(username_ck and password_ck and mobile_number_ck):
    print(Log(log_info="Entered user mobilenumber, username and userpassword are matched.\n"))
    ref_f.write(Log.ret_mu)
    E_mail_failed = 0
else:
    print(Log(log_info="Entered user mobilenumber, username and userpassword are not matched!!!."
              " please check your credentials.\n"))
    ref_f.write(Log.ret_mu)
print(Log(log_info="***** User SIGNIN page end *****\n"))
ref_f.write(Log.ret_mu)
if(not E_mail_failed):
    print(Log(log_info="If you want to sending email, please give your option: (Yes/y or No/n)\n"))
    ref_f.write(Log.ret_mu)
    loop_count = 0
    while True:
        loop_count = loop_count + 1
        email_skip = (sys.stdin.readline())
        print(Log(log_info="Selected option is:" + email_skip))
        ref_f.write(Log.ret_mu)
        if(re.match(r'Yes|y', email_skip, re.M | re.I)):
            print(Log(log_info="Email will send to user Email-id for backup...\n"))
            ref_f.write(Log.ret_mu)
            E_mail_send = 1
            break
        elif(re.match(r'No|n', email_skip, re.M | re.I)):
            print(Log(log_info="Email will not send to user Email-id!.\n"))
            ref_f.write(Log.ret_mu)
            break
        else:
            print(Log(log_info="User gave invalid option!!!.\n"))
            ref_f.write(Log.ret_mu)
            if(loop_count == 2):
                print(Log(log_info="This is your last attempt\n"))
                ref_f.write(Log.ret_mu)
            if(loop_count >= 3):
                break
ref_f.close()
if(E_mail_send):
    if(user_email_id is not None):
        get_input = {'user_email': user_email_id, 'log_dir': user_log}
        e_ret = Muthu_email(**get_input)
        if(not e_ret):
            print(Log(log_info="Issues observed while validating Muthu_email\n"))
    else:
        print(Log(log_info="User given EMAIL-ID is invalid/empty, hence "
                  "unable to send an email to user email id...! \n"))
else:
    print(Log(log_info="Unable to send an email...! \n"))
# ========================= End page ================
