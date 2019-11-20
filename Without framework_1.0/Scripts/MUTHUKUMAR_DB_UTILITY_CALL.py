from MUTHUKUMAR_DB_UTILITY import main_class_for_import_utils
import inspect
from collections import OrderedDict
global module_map

__version__ = '2019.07.23.01'
__author__ = 'Muthukumar Subramanian'

class sub_class_for_import_utils(main_class_for_import_utils):
    def __init__(self, module_list=None,  *args, **kwargs):
      # super(sub_class_for_import_utils, self).__init__(m, *args, **kwargs)
      self.list_append =[]
      if module_list is not None:
          for each_loop in module_list:
            self.list_append.append(module_map.get(each_loop))
      elif module_list is None:
        raise "module_list is Empty!!!.."
         
      main_class_for_import_utils.__init__(self, module_list =self.list_append, *args, **kwargs)
    def subclass_method(self, execute_all_def=None, ignore_list=None):
        print('printing subclass_method')
        dict_ret ={}
        ret_c ,mod_defs = main_class_for_import_utils.import_function(self)
        list_methods = [attr for attr in dir(self) if inspect.ismethod(getattr(self, attr)) and not attr.startswith('__')]
        if execute_all_def is True:
            print("execute all method(s)") 
            if list_methods and mod_defs:
                for j in list_methods:
                    if j in mod_defs and j not in ignore_list:
                        if callable(mod_defs[j]):
                            ret_code, ret_ref = mod_defs[j]()
                            print("Callable_func O/p:", ret_code, ret_ref)
        else:
            print("execute user defined method(s)") 
        dict_ret = {'support_def_list': list_methods, 'available_def_list': mod_defs}

        return True, dict_ret
    
    def run_time_import(self, *args, **kwargs):
        print("O/P is ^^^^^^^^^^^^^^^^^^^: ")
        ret_c, ret_dicexecute_funct = self.import_function(*args)
        return True, ret_dicexecute_funct

# importable files are mapping here
module_map = OrderedDict({'ex': 'F://Python//script//New folder//example_1.py',
                           'myc': 'F://Python//script//IMPORT_MODULE//update',
                          'ban': 'F://Python//script//New folder//banner.py',
                          'kwa': 'F://Python//script//New folder//kwarg_args.py',
                        })

#subclass_method_obj = sub_class_for_import_utils()

##if __name__ == '__main__':
##   print("inside class")

   

