import sys
import os
from oslo_utils import importutils

__version__ = "2019.10.20.01"
__author__ = "Muthukumar Subramanian"


class ImportFile(object):
    def __init__(self, modname, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param modname: Execute file name is required
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        '''
        self.myfile = modname
        self.modulename = None
        print("I am from class 'ImportFile' init")

    def execute_test(self, logger, argparse, email, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param modname: Execute file path is required
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
                :param logger: <user choice, implement here if u want to do something>
                :param argparse: <user choice, implement here if u want to do something>
                :param email: <user choice, implement here if u want to do something>
        :return: ret_boolean
        '''
        print("Before 'run_test' run")
        kwargs.update({'logger': logger,
                       'argparse': argparse,
                       'email': email})
        ret_boolean = self.run_test(self, *args, **kwargs)
        print("After 'run_test' run")
        print("Exit test case")
        return ret_boolean

    def run_test(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: Boolean
        '''
        print("I am from method 'run_test'")
        class_obj = None
        exists = os.path.exists(self.myfile)
        isfile = os.path.isfile(self.myfile)
        if exists is False or isfile is False:
            print("provided file is invalid: {}".format(self.myfile))
            return False
        pathname, filename = os.path.split(self.myfile)
        sys.path.append(os.path.abspath(pathname))
        self.modulename = os.path.splitext(filename)[0]
        try:
            imported_module_name = importutils.import_module(self.modulename)
        except Exception as err:
            print("Observed exception while import a file: {}".format(err))
            return False
        else:
            cls = getattr(imported_module_name, self.modulename, None)
            print("Class is: {}".format(cls))
            try:
                if cls is None:
                    print("No class {} found in file {}.py. Executing as a module.".format(self.modulename,
                                                                                           self.modulename))
                    class_obj = imported_module_name
                else:
                    print("Class {} found in file {}.py. Executing as a class.".format(self.modulename,
                                                                                       self.modulename))
                    # Automatically execute imported file, def __init__ will be execute
                    class_obj = cls(self, *args, **kwargs)
            except Exception as err_test_to_run:
                print("Observed exception while executing imported file: {}".format(err_test_to_run))
                return False
            # Execute the 'test' function in Execute function
            output = class_obj.test(self, *args, **kwargs)

        return True
