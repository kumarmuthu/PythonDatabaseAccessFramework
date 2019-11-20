#============== Date_time and log print ==================
from MUTHUKUMAR_TIME_DATE import *
#=========================================================
admin_log = "Test_logger"
(ok,log_obj)= Create_dir(dir_name = admin_log, logger_enabled = True)
#print(ok)
# import pdb;pdb.set_trace()

def muthutry(ob):
    ob.info("inside print".format())
    return True
log_obj.info("yes   hfghghg ghgfh".format())
log_obj.critical("CRIC".format())
log_obj.error("ERR".format())
log_obj.warning("WARN".format())
log_obj.debug("debug".format())
log_obj.info("qwerty".format())
log_obj.info("asdfghjkl".format())
log_obj.info("zxcvbnm".format())

log_obj.error("".format())
log_obj.info("".format())
muthutry(log_obj)
log_obj.handlers.clear()
log_obj.info("vvvvvvvvvvvvv".format())
'''
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


