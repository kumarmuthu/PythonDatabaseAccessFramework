# Author: Muthukumar Subramanian
# v2018.07.15.01 - Developed ADMIN_SIGNIN
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
admin_log = 'MUTHUKUMAR_APP_ADMIN_SIGNIN_LOG'
(ok, ref_f) = Create_dir(dir_name=admin_log)
global fail
fail = "FAIL"
u_name = None
m_num = None
admin_email_id = None
E_mail_failed = 1
E_mail_send = None
adminname_ck = 0
password_ck = 0
mobile_number_ck = 0
cr_pass = fail
print(Log(log_info="***** admin SIGNIN page start *****\n"))
ref_f.write(Log.ret_mu)
print(Log(log_info="Enter admin name: [Alphabet character only"
          " allowed, minimum 3 character to maximum 20 chracter]\n"))
ref_f.write(Log.ret_mu)
admin_adminname = (sys.stdin.readline())
# print(admin_adminname)


def admin_adminname_validate(_input_adminname):
    pat = r"^[a-zA-Z0-9\_]{3,20}$"
    admin_adminname = re.match(pat, _input_adminname, re.M | re.I)
    if admin_adminname:
        print(Log(log_info="Valid admin name : " + admin_adminname.group() + "\n"))
        ref_f.write(Log.ret_mu)
        return 1, admin_adminname.group()
    else:
        print(Log(log_info="Entered admin name is invalid:" + ' ' + _input_adminname))
        ref_f.write(Log.ret_mu)
        i = 0
        print(Log(log_info="Try again admin name (You can give use this format::"
                  " [Alphabet character only allowed, minimum 3 character "
                  "to maximum 20 chracter]\n"))
        ref_f.write(Log.ret_mu)
        while True:
            i = i + 1
            admin_adminname_2 = (sys.stdin.readline())
            admin_adminname_3 = re.match(pat, admin_adminname_2, re.M | re.I)
            if admin_adminname_3:
                print(Log(log_info="Valid admin name : " + admin_adminname_3.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, admin_adminname_3.group()
            else:
                print(Log(log_info="Entered admin name is invalid:" + ' ' + admin_adminname_2))
                ref_f.write(Log.ret_mu)
                if(i == 2):
                    print(Log(log_info="This is your last attempt\n"))
                    ref_f.write(Log.ret_mu)
                if(i >= 3):
                    break
    return 0, fail


(ret, u_name) = admin_adminname_validate(_input_adminname=admin_adminname)
if(not ret):
    print(Log(log_info="Issues observed while validating adminname\n"))
    ref_f.write(Log.ret_mu)

print(Log(log_info="Enter your Mobile Number: country code(2 digit)"
          " and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570\n"))
ref_f.write(Log.ret_mu)
adminmobile_number = (sys.stdin.readline())
# print(adminmobile_number)


def adminmobile_number_validate(_input_mn):
    pat = r"^(\d{2})-(\d{10})$"
    adminmobile_number = re.match(pat, _input_mn, re.M | re.I)
    if adminmobile_number:
        print(Log(log_info="Its a valid Mobile Number :" + adminmobile_number.group() + "\n"))
        ref_f.write(Log.ret_mu)
        return 1, adminmobile_number.group()
    else:
        print(Log(log_info="Entered Mobile Number is Invalid:" + ' ' + _input_mn))
        ref_f.write(Log.ret_mu)
        print(Log(log_info="Try again admin Mobile Number (You can use this"
                  " format:: country code(2 digit) and Number(10 digit)"
                  " [xx-xxxxxxxxxx] Example : 91-9566067570)\n"))
        ref_f.write(Log.ret_mu)
        i = 0
        while True:
            i = i + 1
            adminmobile_number_2 = (sys.stdin.readline())
            adminmobile_number_3 = re.match(pat, adminmobile_number_2, re.M | re.I)
            if adminmobile_number_3:
                print(Log(log_info="Its a valid Mobile Number :" + adminmobile_number_3.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, adminmobile_number_3.group()
            else:
                print(Log(log_info="admin given mobile number is invalid:" + ' ' + adminmobile_number_2))
                ref_f.write(Log.ret_mu)
                if(i == 2):
                    print(Log(log_info="This is your last attempt\n"))
                    ref_f.write(Log.ret_mu)
                if(i >= 3):
                    break
    return 0, fail


(ret, m_num) = adminmobile_number_validate(_input_mn=adminmobile_number)
if(not ret):
    print(Log(log_info="Issues observed while validating mobile number\n"))
    ref_f.write(Log.ret_mu)

print(Log(log_info="Enter your password: [Alphabet character and numbers"
          " are allowed, minimum 3 character and maximum 20 chracter]\n"))
ref_f.write(Log.ret_mu)
admin_password = (sys.stdin.readline())


def admin_password_validate(_input_pwd):
    pat = r"^([-./@#&+\w]+){3,20}$"
    admin_pass = re.match(pat, admin_password, re.M | re.I)
    password_cr = None
    password_co = None
    if admin_pass:
        print(Log(log_info="Valid password : " + admin_pass.group() + "\n"))
        ref_f.write(Log.ret_mu)
        return 1, admin_pass.group()
    else:
        print(Log(log_info="Entered password is invalid:" + ' ' + _input_pwd))
        ref_f.write(Log.ret_mu)
        i = 0
        print(Log(log_info="Try again password (You can give use this"
                  " format:: [Alphabet character and numbers are allowed, "
                  "minimum 3 character and maximum 20 chracter]\n"))
        ref_f.write(Log.ret_mu)
        while True:
            i = i + 1
            admin_pass_2 = (sys.stdin.readline())
            admin_pass_3 = re.match(pat, admin_pass_2, re.M | re.I)
            if admin_pass_3:
                print(Log(log_info="Valid admin password : " + admin_pass_3.group() + "\n"))
                ref_f.write(Log.ret_mu)
                return 1, admin_pass_3.group()
                break
            else:
                print(Log(log_info="Entered admin password is invalid:" + ' ' + admin_pass_2))
                ref_f.write(Log.ret_mu)
                if(i == 2):
                    print(Log(log_info="This is your last attempt\n"))
                    ref_f.write(Log.ret_mu)
                if(i >= 3):
                    break
    return 0, fail


(ret, cr_pass) = admin_password_validate(_input_pwd=admin_password)
if(not ret):
    print(Log(log_info="Issues observed while validating admin password\n"))
    ref_f.write(Log.ret_mu)
if(u_name == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL"):
    print(Log(log_info="Sorry your signin process is failed!!! Try again signin\n"))
    ref_f.write(Log.ret_mu)
else:
    print(Log(log_info="Inprogress your signin ... please wait a moments... \n"))
    ref_f.write(Log.ret_mu)
    time.sleep(5)
    get_input = {'login_type': 'ADMIN', 'skip_table_create': 'SKIP',
                 'dir_obj': ref_f, 'METHOD': 'signin',
                 'admin_table_name': u_name, 'admin_adminname': u_name,
                 'adminmobile_number': m_num, 'admin_password': cr_pass}
    (ret, ref) = Muthu_db(**get_input)
    if(not ret):
        print(Log(log_info=ref + "\n"))
        ref_f.write(Log.ret_mu)
    else:
        for key, value in ref.items():
            if(key == m_num):
                mobile_number_ck = 1
                for key2, value2 in value.items():
                    if(key2 == 'admin_adminname'):
                        if(value2 == u_name):
                            adminname_ck = 1
                    if(key2 == 'admin_password'):
                        if(value2 == cr_pass):
                            password_ck = 1
                    if(key2 == 'admin_email'):
                        admin_email_id = value2
if(adminname_ck and password_ck and mobile_number_ck):
    print(Log(log_info="Entered admin mobilenumber, adminname and "
              "adminpassword are matched.\n"))
    ref_f.write(Log.ret_mu)
    E_mail_failed = 0
else:
    print(Log(log_info="Entered admin mobilenumber, adminname and "
              "adminpassword are not matched!!!. please check your credentials.\n"))
    ref_f.write(Log.ret_mu)
print(Log(log_info="***** Admin SIGNIN page end *****\n"))
ref_f.write(Log.ret_mu)
if(not E_mail_failed):
    print(Log(log_info="If you want to send an email, please give "
              "your option: (Yes/y or No/n)\n"))
    ref_f.write(Log.ret_mu)
    loop_count = 0
    while True:
        loop_count = loop_count + 1
        email_skip = (sys.stdin.readline())
        print(Log(log_info="Selected option is:" + email_skip))
        ref_f.write(Log.ret_mu)
        if(re.match(r'Yes|y', email_skip, re.M | re.I)):
            print(Log(log_info="Email will send to admin Email-id for backup...\n"))
            ref_f.write(Log.ret_mu)
            E_mail_send = 1
            break
        elif(re.match(r'No|n', email_skip, re.M | re.I)):
            print(Log(log_info="Email will not send to admin Email-id!.\n"))
            ref_f.write(Log.ret_mu)
            break
        else:
            print(Log(log_info="Admin gave invalid option!!!.\n"))
            if(loop_count == 2):
                print(Log(log_info="This is your last attempt\n"))
                ref_f.write(Log.ret_mu)
            if(loop_count >= 3):
                break
ref_f.close()
if(E_mail_send):
    if(admin_email_id is not None):
        get_input = {'user_email': admin_email_id, 'log_dir': admin_log}
        e_ret = Muthu_email(**get_input)
        if(not e_ret):
            print(Log(log_info="Issues observed while validating Muthu_email\n"))
    else:
        print(Log(log_info="Admin gave EMAIL-ID is invalid/empty, "
                  "hence unable to send an email to admin email id...! \n"))
else:
    print(Log(log_info="Unable to send an email...! \n"))
# ========================= End page ================
