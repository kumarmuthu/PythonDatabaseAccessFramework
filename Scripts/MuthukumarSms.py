'''
    Class MuthukumarSms have Muthu_sms,this function will send sms(through the way2sms) to user/admin mobile.

    HISTORY
    - 2018.06.09.01 - Muthukumar Subramanian
        * Initial release
'''

import way2sms
import sys

__version__ = '2018.06.09.01'
__author__ = 'Muthukumar Subramanian'


class MuthukumarSms(object):
    def __init__(self, *args, **kwargs):
        pass

    def Muthu_sms(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param kwargs: default dict, required login type, admin_mobile_num or user_mobile_num, forgot_paswd,
                                msg_signup, logger object
            Optional argument(s):
                :param args: default list
        :return: Boolean
        '''
        text = None
        login_type = kwargs.get('login_type')
        if login_type == 'ADMIN':
            a_table_num = kwargs.get('admin_mobile_num')
            mobile_number = a_table_num
        elif login_type == 'USER':
            u_table_num = kwargs.get('user_mobile_num')
            mobile_number = u_table_num
        if mobile_number is None:
            mobile_number = kwargs.get('forgot_paswd')
        msg_signup = kwargs.get('msg_signup')
        log_obj = kwargs.get('log_obj')
        (c_code, sender_mobile_no) = mobile_number.split("-")
        msg = msg_signup
        try:
            mobileNo = '9566067570'
            # TODO
            password = 'your way2sms password'
            q = way2sms.Sms(mobileNo, password)
            q.set_cookies_header()
            q.send(sender_mobile_no, msg)
            # q.msgSentToday() # have bug
            q.logout()
            log_obj.info("Sending sms to: {}".format(mobile_number))
        except Exception:
            log_obj.warning("Unable to send sms: {}".format(mobile_number))
            log_obj.warning("Please check yor connectivity!!!".format())
            return False
        return True


if __name__ != '__main__':
    object_sms = MuthukumarSms()
else:
    m_num = '91-9566067570'
    user_name_is = 'User'
    login_type = 'USER'
    kwargs = {'login_type': login_type, 'user_mobile_num': m_num,
              'msg_signup': 'Hi' + user_name_is + ',\n\t Thanks for your signup...\nThanks,\nAdmin team(Muthu)\n'}
    object_sms = MuthukumarSms()
    m_ret = object_sms.Muthu_sms(**kwargs)
    if not m_ret:
        print("Issues observed while validating Muthu_sms\n")
