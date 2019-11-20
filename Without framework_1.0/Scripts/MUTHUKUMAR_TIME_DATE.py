# Author: Muthukumar Subramanian
# v2018.05.13.01 - Functions _Time_Date and _Log can call any file
# v2018.05.27.01 - Created function 'Create_dir' for log file
import time
import os,sys
import logging
import logging.config
#========================= Time and Date =================
def Time_Date ():
    from time import localtime,strftime
    current_date = strftime("%d/%m/%Y",localtime())
    current_time = strftime("%H:%M:%S",localtime())
    from datetime import datetime
    d = datetime.strptime(current_time,"%H:%M:%S")
    converted_current_time = d.strftime("%I:%M:%S %p")
    final_time = current_time + ' '+'(' + '12 hours format: '+ converted_current_time + ')'
    #print ("Current Time:", current_time)
    final_date_time = current_date +  ' ' + '-' + ' ' + current_time
    from datetime import datetime as dt
    date_a = dt.strptime(current_date,"%d/%m/%Y")
    return (final_date_time, current_date, date_a, dt)

#=========================================================
#========================= Log print =================

def LOG (log_info):
    (a,b,c,d) = Time_Date()
    ret_log = a + ' ' + '|' +' ' + log_info
    return ret_log

def muthu(func):
    def kumar_s(*ar, **kwarg):
        return func(kumar_s, *ar, **kwarg)
    return kumar_s
@muthu
#mu is self
def Log (mu,log_info):
    RET = LOG(log_info)
    mu.ret_mu = RET
    return RET
#=========================================================
def Create_dir(dir_name, logger_enabled = None):
    changedir = os.chdir("F:\\Python\\Run_log_for_python")
    cwd1 = os.getcwd()
    file_name = cwd1 +'\\'+ dir_name
    if logger_enabled is True:
        f = Logger(file_name)
    else:
        f = open(file_name + ".txt" ,"w")
    return True,f
#=========================================================

#================== Logger ================================
def Logger(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
    logging.basicConfig(filename = '%s.log' %(file_name),format= '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S', filemode = 'w', level = logging.INFO)
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.DEBUG)
    # log_obj = logging.getLogger().addHandler(logging.StreamHandler())
    
    # console printer
    screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)
    
    log_obj.info("Logger object created successfully..")
    return log_obj
#=========================================================


'''
def with_this(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@with_this
def hi(this):
    # other code...
    this.bye = 42  # Create function attribute.
    sigh = 10

hi()
print(hi.bye)

def Logger(file_name):
    formatter = logging.Formatter(fmt='%(asctime)s  %(levelname)8s %(module)s,line: %(lineno)d | %(message)s',
                                  datefmt='%Y/%m/%d %H:%M:%S')
    file_handler = logging.FileHandler('%s.log' %(file_name), mode='w')
    file_handler.setFormatter(formatter)
    # console print
    screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)
    return logger
'''








    
