# Author: Muthukumar Subramanian
# v2018.03.25.01 - Developed ADMIN_SIGNUP
# v2018.07.15.01 - Added support for admin dedicated/default table CREATE and INSERT query
__author__ = "Muthukumar Subramanian"
import sys
import re
import requests

# ============== Database import ==========================
from MUTHUKUMAR_DB import *
# =========================================================
# ============== Date_time and log print ==================
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
# ============= Muthu_email for send an email =============
from MUTHUKUMAR_EMAIL import *
# =========================================================
# ======= Muthu_sms for send a sms to admin mobile =========
from MUTHUKUMAR_SMS import *
# =========================================================
admin_log = 'MUTHUKUMAR_APP_ADMIN_SIGNUP_LOG'
(ok, ref_f) = Create_dir(dir_name=admin_log)
global fail
fail = "FAIL"

a_name = None
e_mail = None
m_num = None
cr_pass = fail
co_pass = fail
print(Log(log_info="***** admin SIGNUP page start *****\n"))
ref_f.write(Log.ret_mu)

print(Log(log_info="Enter admin name: [Alphabet character only allowed, minimum 3 character to maximum 20 chracter]\n"))
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
        print(Log(log_info="Try again admin name (You can give use this "
                  "format:: [Alphabet character only allowed, minimum 3 "
                  "character to maximum 20 chracter]\n"))
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


(ret, a_name) = admin_adminname_validate(_input_adminname=admin_adminname)
if(not ret):
    print(Log(log_info="Issues observed while validating adminname\n"))
    ref_f.write(Log.ret_mu)

print(Log(log_info="Enter email-id: [Alphabet character,numbers "
          "and special characters [ '-' and/or '.' ] are allowed] "
          "Example: abcd_5.kum@gmail.com, noreplymuthukumar@gmail.com\n"))
ref_f.write(Log.ret_mu)
admin_email = (sys.stdin.readline())
# print(admin_email)


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


def admin_email_validate(_input_email):
    pat = r"^([a-zA-Z][\w\_\.]{3,50})\@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,4})$"
    admin_email = re.match(pat, _input_email, re.M | re.I)
    retry_valid = 0
    if admin_email:
        domain = admin_email.group(2)
        em_domain_length = len(domain)
        enable_valid = _email(domain, em_domain_length)
        if enable_valid:
            print(Log(log_info="Its a valid Email ID : " + admin_email.group() + "\n"))
            ref_f.write(Log.ret_mu)
            return 1, admin_email.group()
        else:
            retry_valid = 1
    else:
        retry_valid = 1
    if(retry_valid):
        print(Log(log_info="Entered admin Email ID is invalid:" + ' ' + _input_email))
        ref_f.write(Log.ret_mu)
        i = 0
        print(Log(log_info="Try again email-id (You can give use this "
                  "format:: [Alphabet character only allowed, minimum 3"
                  " character to maximum 50 chracter]\n"))
        ref_f.write(Log.ret_mu)
        while True:
            i = i + 1
            retry_valid = 0
            enable_valid = 0
            admin_email_2 = (sys.stdin.readline())
            admin_email_3 = re.match(pat, admin_email_2, re.M | re.I)
            if admin_email_3:
                domain = admin_email_3.group(2)
                em_domain_length = len(domain)
                enable_valid = _email(domain, em_domain_length)
                retry_valid = 1
            else:
                retry_valid = 1
            if(retry_valid):
                if enable_valid:
                    print(Log(log_info="Its a valid Email ID : " + admin_email_3.group() + "\n"))
                    ref_f.write(Log.ret_mu)
                    return 1, admin_email_3.group()
                else:
                    print(Log(log_info="Entered admin Email ID is invalid:" + ' ' + admin_email_2))
                    ref_f.write(Log.ret_mu)
                    if(i == 2):
                        print(Log(log_info="This is your last attempt\n"))
                        ref_f.write(Log.ret_mu)
                    if(i >= 3):
                        break

    return 0, fail


(ret, e_mail) = admin_email_validate(_input_email=admin_email)
if(not ret):
    print(Log(log_info="Issues observed while validating email\n"))
    ref_f.write(Log.ret_mu)

print(Log(log_info="Enter your Mobile Number: country code(2 digit)"
          " and Number(10 digit) [xx-xxxxxxxxxx] Example : 91-9566067570 \n"))
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
        print(Log(log_info="Try again admin Mobile Number ((You can use this "
                  "format:: country code(2 digit) and Number(10 digit)"
                  " [xx-xxxxxxxxxx] Example : 91-9566067570 )\n"))
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

j = 0
while True:
    j = j + 1
    if(j == 2):
        print(Log(log_info="Password and confirm password have last attempt\n"))
        ref_f.write(Log.ret_mu)
    if(j <= 2):
        print(Log(log_info="Enter your password: [Alphabet character and numbers"
                  " are allowed, minimum 3 character and maximum 20 chracter]\n"))
        ref_f.write(Log.ret_mu)
        admin_password = (sys.stdin.readline())
        pat = r"^([-./@#&+\w]+){3,20}$"
        admin_pass = re.match(pat, admin_password, re.M | re.I)
        password_cr = None
        password_co = None
        if admin_pass:
            print(Log(log_info="Valid password : " + admin_pass.group() + "\n"))
            ref_f.write(Log.ret_mu)
            password_cr = admin_pass.group()
        else:
            print(Log(log_info="Entered password is invalid:" + ' ' + admin_password))
            ref_f.write(Log.ret_mu)
            i = 0
            print(Log(log_info="Try again password (You can give use this format:: "
                      "[Alphabet character and numbers are allowed, minimum 3 "
                      "character and maximum 20 chracter]\n"))
            ref_f.write(Log.ret_mu)
            while True:
                i = i + 1
                admin_pass_2 = (sys.stdin.readline())
                admin_pass_3 = re.match(pat, admin_pass_2, re.M | re.I)
                if admin_pass_3:
                    print(Log(log_info="Valid admin password : " + admin_pass_3.group() + "\n"))
                    ref_f.write(Log.ret_mu)
                    password_cr = admin_pass_3.group()
                    break
                else:
                    print(Log(log_info="Entered admin password is invalid:" + ' ' + admin_pass_2))
                    ref_f.write(Log.ret_mu)
                    if(i == 2):
                        print(Log(log_info="This is your last attempt\n"))
                        ref_f.write(Log.ret_mu)
                    if(i >= 3):
                        break

        print(Log(log_info="Enter your confirm password: [Alphabet character and numbers"
                  " are allowed, minimum 3 character and maximum 20 chracter]\n"))
        ref_f.write(Log.ret_mu)
        admin_confirm_password = (sys.stdin.readline())
        admin_confirm_pass = re.match(pat, admin_confirm_password, re.M | re.I)
        if admin_confirm_pass:
            global cm_pass
            cm_pass = admin_confirm_pass.group()
            print(Log(log_info="Valid confirm password : " + admin_confirm_pass.group() + "\n"))
            ref_f.write(Log.ret_mu)
            password_co = admin_confirm_pass.group()
        else:
            print(Log(log_info="Entered confirm password is invalid:" + ' ' + admin_confirm_password))
            ref_f.write(Log.ret_mu)
            i = 0
            print(Log(log_info="Try again confirm password (You can give use this "
                      "format:: [Alphabet character and numbers are allowed, minimum 3 "
                      "character and maximum 20 chracter] \n"))
            ref_f.write(Log.ret_mu)
            while True:
                i = i + 1
                admin_confirm_pass_2 = (sys.stdin.readline())
                admin_confirm_pass_3 = re.match(pat, admin_confirm_pass_2, re.M | re.I)
                if admin_confirm_pass_3:
                    print(Log(log_info="Valid confirm password : " + admin_confirm_pass_3.group() + "\n"))
                    ref_f.write(Log.ret_mu)
                    password_co = admin_confirm_pass_3.group()
                    break
                else:
                    print(Log(log_info="Entered confirm password is invalid:" + ' ' + admin_confirm_pass_2))
                    ref_f.write(Log.ret_mu)
                    if(i == 2):
                        print(Log(log_info="This is your last attempt\n"))
                        ref_f.write(Log.ret_mu)
                    if(i >= 3):
                        break
        if(password_cr == password_co and password_cr is not None and password_co is not None):
            cr_pass = password_cr
            co_pass = password_co
            print(Log(log_info="Verified password and confirm password is equal \n"))
            ref_f.write(Log.ret_mu)
            break
        else:
            print(Log(log_info="Password and confirm password is not equal !!!\n"))
            ref_f.write(Log.ret_mu)
    if(j >= 3):
        break

if(a_name == "FAIL" or e_mail == "FAIL" or m_num == "FAIL" or cr_pass == "FAIL" or co_pass == "FAIL"):
    print(Log(log_info="Sorry your Signup process is failed !!! Try again signup\n"))
    ref_f.write(Log.ret_mu)
else:
    print(Log(log_info="Inprogress your signup ... please wait a moments... \n"))
    ref_f.write(Log.ret_mu)
    time.sleep(5)
    get_input = {
        'login_type': 'ADMIN',
        'skip_table_create': 'SKIP',
        'dir_obj': ref_f,
        'METHOD': 'signup',
        'admin_table_name': a_name,
        'admin_adminname': a_name,
        'admin_email': e_mail,
        'adminmobile_number': m_num,
        'admin_password': cr_pass,
        'admin_confirm_password': co_pass}
    (ret, ref) = Muthu_db(**get_input)
    if(not ret):
        print(Log(log_info="Error:" + ref))
        ref_f.write(Log.ret_mu)
    else:
        email_send = 1
print(Log(log_info="***** admin SIGNUP page end *****\n"))
ref_f.write(Log.ret_mu)

# ===================== Send sms ======================
if(m_num != "FAIL"):
    if(a_name != "FAIL"):
        admin_name_is = a_name
    else:
        admin_name_is = 'Admin'
    get_input = {'login_type': 'ADMIN', 'admin_mobile_num': m_num, 'msg_signup': 'Hi' +
                 ' ' + admin_name_is + ',\n\t Thanks for your signup...\nThanks,\nAdmin team(Muthu)\n'}
    m_ret = Muthu_sms(**get_input)
    if(not m_ret):
        print(Log(log_info="Issues observed while validating Muthu_sms\n"))
        ref_f.write(Log.ret_mu)
else:
    print(Log(log_info="Unable to send a sms to admin mobile number...! \n"))
    ref_f.write(Log.ret_mu)
# =====================================================

# ====================== Send email ===================
ref_f.close()
if(e_mail != "FAIL"):
    get_input = {'user_email': e_mail, 'log_dir': admin_log}
    e_ret = Muthu_email(**get_input)
    if(not e_ret):
        print(Log(log_info="Issues observed while validating Muthu_email\n"))
else:
    print(Log(log_info="Unable to send an email to admin email id...! \n"))
# =====================================================

# ========================= End page ==================
