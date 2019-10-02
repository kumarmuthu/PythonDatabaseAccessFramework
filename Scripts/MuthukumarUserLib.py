'''
    Class MuthukumarUserLib have get_execution_time, Time_Date, Create_dir, Logger,
    pretty_table_to_html_table_convertor functions. get_execution_time function is used to get a time difference
    between endtime - starttime. Time_Date function is used to get formated time.
    Create_dir function is used to create new directory for current execution of the script.
    Logger function is used to create logger object for filehandler and streamhandler log.
    pretty_table_to_html_table_convertor is used to convert two different handler [HTML and txt]

    HISTORY
    - 2018.05.13.01 - Muthukumar Subramanian
        * Initial release
'''

import time
import os
import sys
import re
import logging
import logging.config
from HtmlLog import HtmlLog  # from HTMLLogger import HTMLLogger
from bs4 import BeautifulSoup

__version__ = '2019.07.27.01'
__author__ = 'Muthukumar Subramanian'


class MuthukumarUserLib(object):
    def __init__(self, *args, **kwargs):
        pass
        self.count = 0
        self.mkdir_count = 0
        # If handler_as_root is 'True', log file will write with root handler,
        # If handler_as_root is 'False', log file will write with user given log name
        # Default as 'False'
        self.handler_as_root = False

    def get_execution_time(self, time1, time2, *args, **kwargs):
        '''
         ..codeauthor:: Muthukumar Subramanian
         Usage:
                Required argument(s):
                    :param time1: we can get start time
                    :param time2: we can get end time
                Optional argument(s):
                    :param args: default list
                    :param kwargs: default dict
        :return: t, t1, t2
        '''
        from datetime import datetime
        time11 = time1.split('.')
        time12 = time11[0].split(' ')
        time13 = time12[0].split('-')
        time14 = time12[1].split(':')
        t1 = datetime(int(time13[0]), int(time13[1]), int(
            time13[2]), int(time14[0]), int(time14[1]), int(time14[2]))
        time21 = time2.split('.')
        time22 = time21[0].split(' ')
        time23 = time22[0].split('-')
        time24 = time22[1].split(':')
        t2 = datetime(int(time23[0]), int(time23[1]), int(
            time23[2]), int(time24[0]), int(time24[1]), int(time24[2]))
        t = t2 - t1
        return (t, t1, t2)

    def Time_Date(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
         Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: final_date_time, current_date, date_a, dt
        '''
        from time import localtime, strftime
        current_date = strftime("%d/%m/%Y", localtime())
        current_time = strftime("%H:%M:%S", localtime())
        from datetime import datetime
        d = datetime.strptime(current_time, "%H:%M:%S")
        converted_current_time = d.strftime("%I:%M:%S %p")
        final_time = current_time + ' ' + '(' + '12 hours format: ' + converted_current_time + ')'
        final_date_time = current_date + ' ' + '-' + ' ' + current_time
        from datetime import datetime as dt
        date_a = dt.strptime(current_date, "%d/%m/%Y")
        return final_date_time, current_date, date_a, dt

    # =========== This decorator will support while we are collecting normal filehandler log ===========
    @staticmethod
    def LOG(log_info):
        (a, b, c, d) = Time_Date()
        ret_log = a + ' ' + '|' + ' ' + log_info
        return ret_log

    def muthu(func):
        def kumar_s(*ar, **kwarg):
            return func(kumar_s, *ar, **kwarg)
        return kumar_s

    @muthu
    def Log(mu, log_info):
        RET = LOG(log_info)
        mu.ret_mu = RET
        return RET
    # ==================================================================================================

    def Create_dir(self, file_name, logger_enabled=None, add_handler=None, append_log=None, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param file_name: we need to send a required file name
            Optional argument(s):
                :param logger_enabled: if it is True logger filehandler write all the printing line(s), otherwise
                                        normal filehandler will write(as of now this hanldler will not support)
                :param add_handler: if it is True, Logger filehandler will be add a new handler
                :param append_log: if it is True, existing handler will remove and re-open that existing log file
                                    and append all the printing into that log file
                :param args: default list
                :param kwargs: default dict
        :return: filehandler_object
        '''
        self.mkdir_count += 1
        from time import localtime, strftime
        current_time = strftime("%H_%M_%S", localtime())
        get_current_date = strftime("%d_%m_%Y", localtime())
        date_and_time = get_current_date + '_' + current_time
        pid = str(os.getpid())
        end_stamp = '_' + date_and_time + '_' + pid
        if self.mkdir_count == 1:
            newpath = 'F:\\Python\\Run_log_for_python\\' + file_name + end_stamp
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                changedir = os.chdir(newpath)

        if append_log is True:
            cwd1 = os.getcwd()
            list_all = os.listdir(cwd1)
            for each_file in list_all:
                reg_log = re.match(r'(MUTHUKUMAR_DB_EXECUTE_TEST_LOG.*).log$', each_file, flags=re.I)
                if reg_log:
                    dir_name = cwd1 + '\\' + reg_log.group(1)
        else:
            cwd2 = os.getcwd()
            dir_name = cwd2 + '\\' + file_name + end_stamp
        filehandler_object = None
        if logger_enabled is True:
            try:
                filehandler_object = self.Logger(dir_name, file_name, add_handler, append_log)
            except Exception as Err:
                print("Observed exception while create Logger object! {}".format(Err))
        else:
            # deprecated txt file open
            filehandler_object = open(file_name + ".txt", "w")
        return True, filehandler_object

    def Logger(self, dir_name, file_name, add_handler=None, append_log=None, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param dir_name: created directory name is required
                :param file_name: we need to send a required file name
            Optional argument(s):
                :param add_handler: if it is True, Logger filehandler will be add a new handler
                :param append_log: if it is True, existing handler will remove and re-open that existing log file
                                    and append all the printing into that log file
                :param args: default list
                :param kwargs: default dict
        :return: log_obj
        '''

        if self.handler_as_root is True:
            file_name = 'root'
        else:
            file_name = file_name

        # HTML setup
        Keyword_Italic = True
        Keyword_FontSize = 2
        msg_color = dict(
            err_color="red",
            warn_color="magenta",
            info_color="green",
            dbg_color="orange")
        log_format = '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s'
        HtmlmaxBytes = 1024 * 1024 * 5
        console_log = False
        html_title = file_name

        # Time for directory
        from time import localtime, strftime
        current_time = strftime("%H_%M_%S", localtime())

        # Setup for logger
        formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')  # %I:%M:%S %p AM|PM format
        # from colored_log import ColoredFormatter
        # cf = ColoredFormatter("[%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
        logging.basicConfig(filename='%s.log' % (dir_name),
                            format='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S', filemode='w', level=logging.INFO)
        log_obj = logging.getLogger(file_name)
        if add_handler:
            if len(log_obj.handlers) == 4 and append_log is None:
                # below code should work when we creating a file as 'root'
                try:
                    log_obj.removeHandler(log_obj.handlers[3])
                    log_obj.removeHandler(log_obj.handlers[2])
                except Exception as err_remove_handler:
                    log_obj.error("Observed exception while remove handler!: {}".format(err_remove_handler))
                    pass
                file_handler = logging.FileHandler('%s.log' % (dir_name), mode='w')
                file_handler.setFormatter(formatter)
                logging.getLogger(file_name).addHandler(file_handler)
            else:
                if append_log:
                    # removing existing file handler obj for 'MUTHUKUMAR_DB_EXECUTE_TEST_LOG',
                    # if we are not removing previous 'StreamHandler' console will print a with multiple times
                    if isinstance(log_obj.handlers, list):
                        for intex, j in enumerate(log_obj.handlers):
                            if re.search(r'StreamHandler', str(j), flags=re.I):
                                log_obj.removeHandler(log_obj.handlers[intex])
                                log_obj.removeHandler(log_obj.handlers[(intex - 1)])
                    try:
                        file_handler = logging.FileHandler('%s.log' % (dir_name), mode='a')
                        file_handler.setFormatter(formatter)
                        logging.getLogger(file_name).addHandler(file_handler)
                    except Exception as Err:
                        log_obj.error("Observed exception while append file! {}".format(Err))
                    # below code should work when we creating a file as 'root'
                    if len(log_obj.handlers) == 3:
                        try:
                            log_obj.removeHandler(log_obj.handlers[1])
                        except Exception as err:
                            log_obj.error("Observed exception while remove handler! {}".format(err))
                            pass
                else:
                    try:
                        file_handler = logging.FileHandler('%s.log' % (dir_name), mode='w')
                        file_handler.setFormatter(formatter)
                        logging.getLogger(file_name).addHandler(file_handler)
                    except Exception as Err:
                        log_obj.error("Observed exception while create a log file! {}".format(Err))
            # console printer
            screen_handler = logging.StreamHandler(stream=sys.stdout)  # stream=sys.stdout is similar to normal print
            screen_handler.setFormatter(formatter)
            logging.getLogger(file_name).addHandler(screen_handler)
        try:
            # Skiping html file create for 'MUTHUKUMAR_DB_EXECUTE_TEST_LOG', because we already created that file.
            if re.search(r'MUTHUKUMAR_DB_EXECUTE_TEST_LOG', dir_name, flags=re.I):
                self.count += 1
                if self.count <= 1:
                    logger = HtmlLog(name=file_name, html_filename=dir_name + '.html', mode='w',
                                     html_title=html_title, root_level=logging.DEBUG,
                                     HtmlmaxBytes=HtmlmaxBytes, encoding=None, delay=False,
                                     html_format=log_format, msg_color=msg_color,
                                     Keyword_Italic=Keyword_Italic, Keyword_FontSize=Keyword_FontSize,
                                     console_log=console_log,
                                     Html_Rotating=True, Html_backupCount=5)
                    logging.getLogger(file_name).addHandler(logger)
            else:
                logger = HtmlLog(name=file_name, html_filename=dir_name + '.html', mode='w',
                                 html_title=html_title, root_level=logging.DEBUG,
                                 HtmlmaxBytes=HtmlmaxBytes, encoding=None, delay=False,
                                 html_format=log_format, msg_color=msg_color,
                                 Keyword_Italic=Keyword_Italic, Keyword_FontSize=Keyword_FontSize,
                                 console_log=console_log,
                                 Html_Rotating=True, Html_backupCount=5)
                logging.getLogger(file_name).addHandler(logger)
        except Exception as Err:
            log_obj.error("Observed exception while create a HTML file! {}".format(Err))
        log_obj.info("Logger object created for: {}".format(file_name))
        return log_obj

    def pretty_table_to_html_table_convertor(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param kwargs: default dict, required pretty table object and logger object
            Optional argument(s):
                :param args: default list
        :return: Boolean
        '''
        table_obj = kwargs.get('table_obj')
        log_obj = kwargs.get('log_obj')
        html_format = table_obj.get_html_string()
        pretty_format = table_obj.get_string()
        return_data = None
        soup = BeautifulSoup(features='xml')
        body = soup.new_tag('body')
        soup.insert(0, body)

        list_2 = list(html_format.split('\n'))
        list_2.reverse()
        for line in list_2:
            if re.search(r'<table>', line):
                line = re.sub(r'<table>', '<table  border = "3">', line)
            soup.insert(0, line.strip())
        try:
            if isinstance(log_obj.handlers, list):
                for intex, j in enumerate(log_obj.handlers):
                    if re.search(r'StreamHandler', str(j), flags=re.I):
                        return_data = pretty_format
                        log_obj.handlers[intex].stream.write("\n%s\n" % (return_data))
                    elif re.search(r'FileHandler', str(j), flags=re.I):
                        return_data = pretty_format
                        log_obj.handlers[intex].stream.write("\n%s\n" % (return_data))
                        log_obj.handlers[intex].flush()
                    else:
                        return_data = (soup.prettify(formatter=None))
                        log_obj.handlers[intex].info("{} {}".format("\n", return_data))
        except Exception as pretty_html_convert_err:
            return False
        return True


user_lib_obj = MuthukumarUserLib()
