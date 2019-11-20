from pprint import pprint
import inspect
from oslo_utils import importutils
import os,sys

#cwd = os.getcwd()
#print(cwd)
#import numpy.random
__version__ = '2019.07.23.01'
__author__ = 'Muthukumar Subramanian'

class main_class_for_import_utils(object):
    def __init__(self, module_list=None,  *args, **kwargs):
        self.dict_store = {}
        self.module_list = module_list
        print("***** main_class_for_import_utils init list:{} *******".format(self.module_list))
    def import_function(self, *args, **kwargs):
        print("##### printing import_function init #######")
        s_dict = {}
        if args:
            args = list(args)
            print("import a file(s), it is given by runtime import method \n File: {}".format(args))
        else:
            if isinstance(self.module_list, list) and len(self.module_list) !=0:
                args = self.module_list
            else:
                raise  "module_list is Empty!!! or unsupported format.."
        for myfile in args:
            os.path.exists(myfile)
            os.path.isfile(myfile)
            pathname, filename = os.path.split(myfile)
            sys.path.append(os.path.abspath(pathname))
            modname = os.path.splitext(filename)[0]
            #print("FN: ",filename)
            #imported_module_name = importutils.import_object(filename,*args,**kwargs)
            #aa = inspect.getmembers(modname)
            #import pdb;pdb.set_trace()
            #print("num",numpy.random.__file__)
            #a=inspect.getsourcefile(myfile)
            
            imported_module_name = importutils.import_module(modname)
            #print("imported_module_name: ",imported_module_name)

            for class_name, class_method_type in inspect.getmembers(imported_module_name):
                if not class_name.startswith('__'):
                    #print("class_name: ",class_name, type(class_name))
                    #print("class_method_type: ",class_method_type, type(class_method_type))
    
                    if callable(class_method_type):
                        class_name = class_method_type(**s_dict)
                        for def_name, def_method_type in inspect.getmembers(class_name):
                            if not def_name.startswith('__') :
                                #print("def_name: ",def_name, type(def_name))
                                #print("def_method_type: ",def_method_type, type(def_method_type))
                                setattr(self, def_name, def_method_type)
                                if inspect.ismethod(getattr(self, def_name)):
                                    self.dict_store.update({ def_name: def_method_type})   
        
        return True, self.dict_store
    
obj =main_class_for_import_utils()
if __name__ == '__main__':
    # execute all the def if run this file (inspect_try.py)
    try:
        list_methods=[]
        myfile = 'F://Python//script//New folder//banner.py'
        myfile_2 = 'F://Python//script//New folder//kwarg_args.py'
        myfile_3 = 'F://Python//script//New folder//example_1.py'

        list_mod =[myfile,myfile_2,myfile_3]
        ret_code, dict_def = obj.import_function(*list_mod)
        list_methods = [attr for attr in dir(obj) if inspect.ismethod(getattr(obj, attr)) and not attr.startswith('__')]
        for j in list_methods:
            if j in obj.dict_store:
                if callable(obj.dict_store[j]):
                    # print("obj.dict_store :",obj.dict_store)
                    ret_code, ret_ref = obj.dict_store[j]()
                    print("Callable_func O/p:",ret_code ,ret_ref)
    except Exception as err:
        print("Observed exception while executing import_function : {}".format(err))

else:
    print("Imported from another class!!!")
    
