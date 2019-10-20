from ImportLib import ImportFile

__version__ = "2019.10.20.01"
__author__ = "Muthukumar Subramanian"


def main():
    '''
    ..codeauthor:: Muthukumar Subramanian
    '''
    # logger code here
    # argparse code here
    # email code here

    # I Just parsing hardcoded value(hardcoded values are from above code returned output)
    logger = 'logger'
    argparse = 'argparse'
    email = 'email'
    # Note: MuthuClass.py file we can get from argparse
    modname = 'F:\\Python\\script\\IMPORT_MODULE\\update\\MuthuClass.py'
    Obj = ImportFile(modname)
    # Run execute_test
    ret_boolean = Obj.execute_test(logger, argparse, email)
    if ret_boolean is False:
        print("Observed exception while executing 'execute_test' function")


if __name__ == "__main__":
    main()
