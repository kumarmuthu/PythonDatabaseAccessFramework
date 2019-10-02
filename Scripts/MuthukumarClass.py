import re

__author__ = "Muthukumar Subramanian"


class MuthukumarClass():
    def __init__(self, *args, **kwargs):
        self.fail = "FAIL"
        self.log_obj = None
        self.object_db = None
        self.user_lib_obj = None

    def setup(self, *args, **kwargs):
        self.log_obj.info("Do some setup")
        self.log_obj.warning("warning")
        self.log_obj.debug("debug")
        self.log_obj.error("Error")
        return True, 2500

    def test_run(self, *args, **kwargs):
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
        myclass_log = 'MUTHUKUMAR_DB_MYCLASS_LOG'
        log_obj = None
        try:
            (ok, self.log_obj) = self.user_lib_obj.Create_dir(
                file_name=myclass_log, logger_enabled=True, add_handler=True)
        except Exception as test_err:
            print("test_err: ", test_err)
        ret, ref = self.setup()
        self.log_obj.info("YES, I am test func of muthu_class ")
        if self.log_obj.handlers:
            for index, each_handler in reversed(list(enumerate(self.log_obj.handlers))):
                # each_handler = str(each_handler)
                # if re.search(r'%s' % (myclass_log), each_handler, flags=re.I):
                self.log_obj.removeHandler(self.log_obj.handlers[index])

        return True, 400


if __file__ != "main":
    obj_class = MuthukumarClass()
