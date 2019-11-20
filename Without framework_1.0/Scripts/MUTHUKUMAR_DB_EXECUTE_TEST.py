import timeit
import re
start = timeit.default_timer()
from  MUTHUKUMAR_DB_UTILITY_CALL import sub_class_for_import_utils

__version__ = '2019.07.23.01'
__author__ = 'Muthukumar Subramanian'

class myclass(sub_class_for_import_utils):
    def __init__(self, import_mod_name=None, *args, **kwargs):
        self.list = import_mod_name
        sub_class_for_import_utils.__init__(self, module_list=self.list, *args, **kwargs)
   
    def test(self, *args, **kwargs):
        print("### Executing test method ###")
        if kwargs:
            mod_support_list = kwargs.get('support_def_list')
            available_defs = kwargs.get('available_def_list')
        if mod_support_list and available_defs:
            if callable(available_defs['muthu']):
                ret_code, ret_ref = available_defs['muthu'](self,*args, **kwargs)
                print("Callable_func O/p:", ret_code, ret_ref)
        else:
            False
        return True

file_name = __file__
file_name_list = file_name.split('\\')
file_name_list = [ re.sub(r'.py', "", i, flags=re.I) for i in file_name_list if re.match(r'.*.py', i, flags=re.I) ]

print("File '{}' Current version is \"{}\" ".format(file_name_list[0],__version__))
 
# import script mentioned file(s), but it is depending on mapped modules path 
list_1=['ex']
obj=myclass(import_mod_name = list_1)

# import script given file(s), we can import middle of the script 
li =['F://Python//script//New folder//kwarg_args.py']
obj.run_time_import(*li)

# execute all method(s)
ignore_list_var =['sss','qqq']
ret_ch, ret_dict =obj.subclass_method(execute_all_def = True, ignore_list= ignore_list_var)

# execute user defined method(s)
ret_ch, ret_dict = obj.subclass_method()
print("ret_ch: ",ret_ch)
print("ret_dict: ",ret_dict)
obj.test(**ret_dict)

stop = timeit.default_timer()
total_time = stop - start
total_time = round(total_time,2)
print("Execution Time: {}".format(total_time))
print("**************** END ****************")




