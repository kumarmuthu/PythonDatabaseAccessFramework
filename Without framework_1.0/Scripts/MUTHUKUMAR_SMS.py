# Author: Muthukumar Subramanian
# v2018.06.09.01 - Developed Muthu_sms for send sms to mobile
__author__ = "Muthukumar Subramanian"
import way2sms
import sys
# ============== Date_time and log print ==================
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
global mobile_number


def Muthu_sms(**get_input):
    text = None
    login_type = get_input['login_type'] if get_input['login_type'] else text
    if(login_type == 'ADMIN'):
        a_table_name = get_input['admin_mobile_num'] if get_input['admin_mobile_num'] else text
        mobile_number = a_table_name
    elif(login_type == 'USER'):
        u_table_name = get_input['user_mobile_num'] if get_input['user_mobile_num'] else text
        mobile_number = u_table_name
    msg_signup = get_input['msg_signup'] if get_input['msg_signup'] else text
    # dir_obj = get_input['dir_obj'] if get_input['dir_obj'] else text
    (c_code, mobile_no) = mobile_number.split("-")
    msg = msg_signup
    try:
        mobileNo = '9566067570'
        # mobile_no = '9566067570'
        password = 'K3632G'
        # msg = 'Hi muthu qwerty'
        q = way2sms.Sms(mobileNo, password)
        q.set_cookies_header()
        q.send(mobile_no, msg)
        # q.msgSentToday() # have bug
        q.logout()
        print(Log(log_info="Sending sms to:" + ' ' + mobile_number + "\n"))
        # dir_obj.write(Log.ret_mu)
    except Exception:
        print(Log(log_info="Unable to send sms:" + ' ' + mobile_number + "\n"))
        # dir_obj.write(Log.ret_mu)
        print(Log(log_info="Please check yor connectivity!!!\n"))
        # dir_obj.write(Log.ret_mu)
        return 0
    return 1


# =========================
'''
m_num = '91-9566067570'
user_name_is = 'User'
login_type = 'USER'
get_input = { 'login_type' : login_type, 'user_mobile_num' : m_num,
'msg_signup' : 'Hi' + user_name_is + ',\n\t Thanks for your signup...\nThanks,
\nAdmin team(Muthu)\n'}
m_ret = Muthu_sms(**get_input)
if(not m_ret):
    print(Log(log_info = "Issues observed while validating Muthu_sms\n"))
'''
