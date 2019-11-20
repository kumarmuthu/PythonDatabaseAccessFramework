# Author: Muthukumar Subramanian
# v2018.05.28.01 - Created function 'Muthu_email' for sending email body with attachment
__author__ = "Muthukumar Subramanian"
import smtplib
import pdb
import sys
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def Muthu_email(**kwargs):
    otp_email_msg = kwargs.get('otp_email_msg', None)
    user_email = kwargs.get('user_email', None)
    log_dir = kwargs.get('log_dir', None)
    body_details = None
    sender = 'noreplymuthukumar@gmail.com'
    # sender = 'kumarmuthuece5@gmail.com'
    gmail_password = '9566067570no'
    recipients = ['noreplymuthukumar@gmail.com', user_email]
    # print("user_email:",user_email)
    COMMASPACE = ', '
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'This log is from MUTHUKUMAR_DB_USER_(SIGNIP/SIGNIN) python script!!!.'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    if(otp_email_msg is not None):
        body_details = otp_email_msg
    else:
        body_details = "Hi Guest!,\n\tThis message from python script.\n\tPlease find "
        "your attachment of log.\nThanks,\nAdmin team(Muthu)\n"
    body = MIMEText(body_details)
    outer.attach(body)
    if(otp_email_msg is None):
        changedir = os.chdir("F:\\Python\\Run_log_for_python")
        # filename = 'MUTHUKUMAR_APP_LOG.txt'
        filename = log_dir + '.txt'
        # Add the attachments to the message
        try:
            fp = open(filename, 'rb')
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))

            outer.attach(msg)
        except BaseException:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0] + "\n")
            raise

    composed = outer.as_string()
    try:
        # pdb.set_trace()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender, gmail_password)
        print("Sending mail to:" + ' ' + user_email + "\n")
        server.sendmail(sender, recipients, composed)
        server.quit()
    except BaseException:
        print("Failed to send mail:" + ' ' + user_email)

    return 1
# user_email = 'noreplymuthukumar@gmail.com'
# log_dir = 'MUTHUKUMAR_APP_ADMIN_SIGNIN_LOG'
# ret = Muthu_email(user_email,log_dir)
# print(ret)
