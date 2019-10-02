'''
    Class MuthukumarDbUtilityCall have execute_file_import and run_time_import methods, we can import a file
    from argparse or module_map dict. The ‘run_time_import’ method is used to import a file when we need to execute
    a file while middle of the script execution. Method 'get_version_DB' will collect all the imported files versions

    HISTORY
    - 2019.07.27.01 - Muthukumar Subramanian
        * Initial release
'''
from MuthukumarDbUtility import *
import inspect
import re
from collections import OrderedDict
global module_map

__version__ = '2019.07.27.01'
__author__ = 'Muthukumar Subramanian'


class sub_class_for_import_utils(MuthukumarDbUtility):
    def __init__(self, module_list=None, *args, **kwargs):
        self.list_append = []
        self.module_map = module_map
        if module_list:
            for each_loop in module_list:
                self.list_append.append(module_map.get(each_loop))
        elif module_list is None:
            pass
        # super(sub_class_for_import_utils, self).__init__(m, *args, **kwargs)
        # or
        MuthukumarDbUtility.__init__(self, module_list=self.list_append, *args, **kwargs)

    def execute_file_import(self, execute_all_def=None, ignore_list=None, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param execute_all_def: if you want to execute all the methods and functions
                                        we can pass as 'True', here execute all the def
                :param ignore_list: we can ignore specific method/function
                :param args: default list
                :param kwargs: default dict
        :return: dict_ret
        '''
        dict_ret = {}
        ret_c, mod_defs = MuthukumarDbUtility.import_function(self, *args, **kwargs)
        if ret_c is False:
            return ret_c, mod_defs
        list_methods = [attr for attr in dir(self) if
                        inspect.ismethod(getattr(self, attr)) and not attr.startswith('__')]
        if execute_all_def is True:
            log_obj.info("execute all method(s)".format())
            if list_methods and mod_defs:
                for j in list_methods:
                    if j in mod_defs and j not in ignore_list:
                        if callable(mod_defs[j]):
                            ret_code, ret_ref = mod_defs[j]()
                            log_obj.info("Callable_func O/p: {} {}".format(ret_code, ret_ref))
        else:
            log_obj.info("execute user defined method(s)".format())
        dict_ret = {'support_def_list': list_methods, 'available_def_list': mod_defs, 'user_lib_obj': user_lib_obj,
                    'log_obj': log_obj}

        return True, dict_ret

    def run_time_import(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param args: get import file from *args
            Optional argument(s):
                :param kwargs: default dict
        :return: ret_imported_func
        '''
        log_obj.info("run_time_import method(s)".format())
        ret_c, ret_imported_func = self.import_function(*args)
        return True, ret_imported_func

    def get_version_DB(self, file_name=None, version=None, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param file_name: we can send .py file into this method,it will return expected file name
                :param version: it will return parsed version
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: file_name_list and version
        '''
        if file_name is not None:
            file_name_list = file_name.split('\\')
            file_name_list = [re.sub(r'.*\/(.*).py', r"\1", i, flags=re.I) for i in file_name_list if
                              re.match(r'.*.py', i, flags=re.I)]
            return True, file_name_list[0], version
        else:
            False, None, None


# importable files are mapping here
module_map = OrderedDict(
    {'ex': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py',
     'myc': 'F://Python//script//IMPORT_MODULE//update',
     'ban': 'F://Python//script//New folder//banner.py',
     'kwa': 'F://Python//script//New folder//kwarg_args.py',
     'user signup': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbUserSignup.py',
     'user signin': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbUserSignin.py',
     'admin signin': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignin.py',
     'admin signup': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignup.py',
     'forgot password': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbForgotPassword.py',
     'admin access': 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminAccess.py',
     })
