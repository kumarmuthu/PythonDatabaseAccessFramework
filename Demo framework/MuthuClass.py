__version__ = "2019.10.20.01"
__author__ = "Muthukumar Subramanian"


class MuthuClass(object):
    def __init__(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                None
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        '''
        print("I am from MuthuClass init")

    def muthu(self, *args, **kwargs):
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
        print("I am from method muthu")
        return True

    def test(self, *args, **kwargs):
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
        print("I am from method 'test'")
        print("Imported file executing here")
        print("kwargs: {}".format(kwargs))
        return True
