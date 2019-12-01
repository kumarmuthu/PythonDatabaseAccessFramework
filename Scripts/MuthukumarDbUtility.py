'''
    Class MuthukumarDbUtility will import given module/.py file and return a dict with all the methods and functions,
    we can execute all the methods and functions, dict value should be a copy of bound method object reference

    HISTORY
    - 2019.07.23.01 - Muthukumar Subramanian
        * Initial release
'''

import inspect
from oslo_utils import importutils
import os
import sys
import re
import pprint
from MuthukumarUserLib import *

__version__ = '2019.07.23.01'
__author__ = 'Muthukumar Subramanian'

if user_lib_obj.handler_as_root:
    add_han = False
else:
    add_han = True
utlity_log = 'MUTHUKUMAR_DB_UTILITY_LOG'
(ok, log_obj) = user_lib_obj.Create_dir(file_name=utlity_log, logger_enabled=True, add_handler=add_han)


class MuthukumarDbUtility(object):
    def __init__(self, module_list=None, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        '''
        self.dict_store = {}
        self.version_dict = {}
        self.module_list = module_list
        self.i = 0
        ppoutput = pprint.pformat(self.module_list, indent=4)
        log_obj.info("***** MuthukumarDbUtility init list: {} *******".format(ppoutput))

    def import_function(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian

        This module will import user given file(s)
        Usage:
            Required argument(s):
                :param args: get import file from *args
            Optional argument(s):
                :param kwargs: dict
        :return: self.dict_store
        '''
        imported_module_name = None
        if args:
            args = list(args)
            log_obj.info("import a file(s), it is given by runtime import method \n File: {}".format(args))
        else:
            if isinstance(self.module_list, list) and len(self.module_list) != 0:
                args = self.module_list
            else:
                return False, self.dict_store
        for myfile in args:
            exists = os.path.exists(myfile)
            isfile = os.path.isfile(myfile)
            if exists is False or isfile is False:
                return False, self.dict_store
            pathname, filename = os.path.split(myfile)
            sys.path.append(os.path.abspath(pathname))
            modname = os.path.splitext(filename)[0]

            try:
                ver = None
                imported_module_name = importutils.import_module(modname)
                try:
                    if imported_module_name.__version__ is not None:
                        ver = imported_module_name.__version__
                except Exception as e:
                    pass
                imported_module_name_str = str(imported_module_name)
                if re.search(r'.*\\.*', str(imported_module_name_str)):
                    file_name_list = imported_module_name_str.split('\\')
                else:
                    file_name_list = imported_module_name
                file_name_list = [re.sub(r'.py|\\|\'|<|\"|\>', r"", i, flags=re.I) for i in file_name_list if
                                  re.match(r'.*.py', i, flags=re.I)]
                log_obj.info("File '{}' Current version is \"{}\" ".format(file_name_list[0], ver))
                self.version_dict.update({file_name_list[0]: ver})
            except Exception as err:
                log_obj.error("Observed exception while import a file: {}".format(err))
                return False, self.dict_store
            else:
                class_name = getattr(imported_module_name, modname, None)
                log_obj.info("Class is: {}".format(class_name))
                try:
                    if class_name is None:
                        log_obj.info("No class {} found in this file {}.py. Executing as a module.".format(modname,
                                                                                                           modname))
                        execute_class = imported_module_name
                    else:
                        log_obj.info("Class is {} found in this file {}.py."
                                     "Executing this class.".format(modname, modname))
                        # Automatically execute imported file, def __init__ will be execute
                        execute_class = class_name(self, *args, **kwargs)
                except Exception as err_execute_class:
                    log_obj.error("Observed exception while executing imported file: {}".format(err_execute_class))
                    return False, self.dict_store
            if imported_module_name:
                for class_name, class_method_type in inspect.getmembers(imported_module_name):
                    if not class_name.startswith('__'):
                        if callable(class_method_type):
                            setattr(self, class_name, class_method_type)
                            if inspect.isclass(getattr(self, class_name)) and re.match(r'muthukumar.*', class_name,
                                                                                       flags=re.I):
                                class_name = class_method_type(self, *args, **kwargs)
                                for def_name, def_method_type in inspect.getmembers(class_name):
                                    if not def_name.startswith('__'):
                                        setattr(self, def_name, def_method_type)
                                        if inspect.ismethod(getattr(self, def_name)):
                                            if def_name in self.dict_store and re.match(r'test_run|setup', def_name):
                                                self.i = self.i + 1
                                                self.dict_store.update({"%s_%s" % (def_name, self.i): def_method_type})
                                            else:
                                                self.dict_store.update({def_name: def_method_type})
        return True, self.dict_store


obj = MuthukumarDbUtility()
if __name__ == '__main__':
    try:
        list_methods = []
        myfile = 'F://Python//script//New folder//banner.py'
        myfile_2 = 'F://Python//script//New folder//kwarg_args.py'
        myfile_3 = 'F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py'

        list_mod = [myfile, myfile_2, myfile_3]
        ret_code, dict_def = obj.import_function(*list_mod)
        list_methods = [attr for attr in dir(obj) if inspect.ismethod(getattr(obj, attr)) and not attr.startswith('__')]
        for j in list_methods:
            if j in obj.dict_store:
                if callable(obj.dict_store[j]):
                    ret_code, ret_ref = obj.dict_store[j]()
                    log_obj.info("Callable_func O/p: {} {}".format(ret_code, ret_ref))
    except Exception as err:
        log_obj.info("Observed exception while executing import_function : {}".format(err))

else:
    log_obj.info("Imported from another class!!!".format())
