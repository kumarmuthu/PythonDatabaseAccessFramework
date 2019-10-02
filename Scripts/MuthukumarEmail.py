'''
    Class MuthukumarEmail have Muthu_email,this function will send an email with attachment to user/admin email-id.

    HISTORY
    - 2018.05.08.01 - Muthukumar Subramanian
        * Initial release
'''

__version__ = '2018.05.08.01'
__author__ = 'Muthukumar Subramanian'

import smtplib
import pdb
import sys
import os
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MuthukumarEmail(object):
    def __init__(self, *args, **kwargs):
        pass

    def Muthu_email(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param kwargs: default dict, required otp_email_msg, user_email, send_file, email_send,
                                send_all_file, logger object
            Optional argument(s):
                :param args: default list
        :return: Boolean
        '''
        otp_email_msg = kwargs.get('otp_email_msg')
        user_email = kwargs.get('user_email')
        send_file = kwargs.get('send_file')
        email_send = kwargs.get('email_send')
        send_all_file = kwargs.get('send_all_file')
        log_obj = kwargs.get('log_obj')
        filename = None
        if user_email is None:
            print("Failed to send mail: {}".format(user_email))
            return False
        body_details = None
        sender = 'noreplymuthukumar@gmail.com'
        # sender = 'muthukumarece5@gmail.com'
        gmail_password = 'your gmail password'
        if send_all_file is None:
            recipients = ['noreplymuthukumar@gmail.com', user_email]
        else:
            recipients = ['noreplymuthukumar@gmail.com']
        COMMASPACE = ', '
        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = 'This log is from MUTHUKUMAR_DB_USER_(SIGNIP/SIGNIN) python script!!!.'
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        if otp_email_msg is not None:
            body_details = otp_email_msg
        else:
            body_details = "Hi Guest!,\n\tThis message from python script.\n\tPlease find " \
                           "your attachment of log.\nThanks,\nAdmin team(Muthu)\n"
        body = MIMEText(body_details)
        outer.attach(body)
        if otp_email_msg is None:
            cwd1 = os.getcwd()
            list_all = os.listdir(cwd1)
            if email_send:
                if isinstance(send_file, list):
                    for each_py_file in send_file:
                        if re.search(r'.*.py', str(each_py_file)):
                            filename_sub = re.sub(r'//', r"\\", str(each_py_file), flags=re.I)
                            filename_list = filename_sub.split('\\')
                            file_name_list_f = [re.sub(r'(.*).py', r"\1", i, flags=re.I) for i in filename_list if
                                                re.match(r'.*.py', i, flags=re.I)]
                            for j in list_all:
                                rr = re.search(r'%s.*%s' % (file_name_list_f[0], '.log$'), j, flags=re.I)
                                if rr is not None:
                                    filename = cwd1 + '\\' + j
                            if filename is None:
                                continue
                else:
                    for j in list_all:
                        rr = re.search(r'%s.*%s' % (send_file, '.log$'), j, flags=re.I)
                        if rr is not None:
                            filename = cwd1 + '\\' + j
                if filename is None:
                    raise"File is not found"
                # Add the attachments to the message
                try:
                    with open(filename, mode='rb') as each_line:
                        msg = MIMEBase('application', "octet-stream")
                        msg.set_payload(each_line.read())
                        encoders.encode_base64(msg)
                        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))
                        outer.attach(msg)
                except Exception as open_err:
                    print("Unable to open one of the attachments. Error: {}".format(open_err))
                    raise
            else:
                if list_all:
                    list_all_log = [i for i in list_all if re.match(r'muthu.*.log$|muthu.*.html$', i, flags=re.I)
                                    and i != 'MUTHUKUMAR_DB_EXECUTE_TEST_LOG.*.html']
                    for each_log in list_all_log:
                        # Add the attachments to the message
                        try:
                            filename = cwd1 + '\\' + each_log
                            with open(filename, mode='rb') as each_line:
                                msg = MIMEBase('application', "octet-stream")
                                msg.set_payload(each_line.read())
                                encoders.encode_base64(msg)
                                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))
                                outer.attach(msg)
                        except Exception as open_err:
                            print("Unable to open one of the attachments. Error: {}".format(open_err))
                            raise
        composed = outer.as_string()
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(sender, gmail_password)
            if user_email is not None:
                print("Sending mail to: {}".format(user_email))
            server.sendmail(sender, recipients, composed)
            server.quit()
        except Exception as err_mail_send:
            if user_email is not None:
                print("Gmail login Exception as: {}".format(err_mail_send))
                print("Failed to send mail: {}".format(user_email))
            else:
                print("Gmail login Exception as: {}".format(err_mail_send))
                print("Failed to send mail: {}".format(user_email))
            return False
        return True


if __name__ != '__main__':
    object_email = MuthukumarEmail()
else:
    object_email = MuthukumarEmail()
    kwargs = {'email_send': None,
              'send_all_file': True}
    object_email.Muthu_email(**kwargs)
