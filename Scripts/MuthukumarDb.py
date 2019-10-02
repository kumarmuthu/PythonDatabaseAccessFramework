'''
    Class MuthukumarDb is used to create pyodbc cursor object and we do any one the operation read|insert|update|delete
    for admin/user table. Create_new_table will create new table for individual admin/user signup, it will take
    much memory usage on database so we disabled this, we can use when it is required.
    Insert_query will insert a data into our database table admin/user. User_and_admin_signin will collect a user/admin
    table entries for validation. Muthu_db is main function of the file, this function will redirecting to either
    signup or signin for admin/user when we are executing admin/user signup|in script.
    Access_query function will execute when we need to do insert|update|delete query on database

    HISTORY
    - 2018.05.13.01 - Muthukumar Subramanian
        * Initial release
    - v2019.07.20.01 - Muthukumar Subramanian
        * Added logger support
'''


import sys
import re
import pyodbc


__version__ = "2019.07.20.01"
__author__ = "Muthukumar Subramanian"


def SqlObjCreate(func):
    def wrapped(class_obj, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Usage:
            Required argument(s):
                :param class_obj: We can use any variable here instead of 'class_obj',
                                executed class object will be present here.
                                Example: <__main__.SqlDecoratorSkipCheck object at 0x0000023BA70B7EF0>
                :param args: default list
                :param kwargs: default dict
                :return: SqlDecoratorSkipCheck.<called method|function>,
                         Example: <function SqlDecoratorSkipCheck.test at 0x0000023BA70B60D0>
            Optional argument(s):
                None
        '''
        if class_obj.object_db.cursor_obj is None:
            # we can do any operation here before actual execution
            class_obj.log_obj.info("From decorator function, Creating new cursor object here!".format())
            class_obj.log_obj.debug("Function name is: {}".format(func))
            try:
                class_obj.sql_con_obj = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=user_verification;UID=sa;PWD=P@ssword;')
                class_obj.object_db.cursor_obj = class_obj.sql_con_obj.cursor()
                class_obj.log_obj.info("pyobdc object is created successfully...".format())
                # print("pyobdc object is created successfully...".format())
            except Exception as err_pyodc:
                class_obj.log_obj.error("Observed exception: {}".format(err_pyodc))
                # print("Observed exception: {}".format(err_pyodc))
        else:
            class_obj.log_obj.debug("cursor object is already created...")
        return func(class_obj, *args, **kwargs)
    return wrapped


class OptionalDecoratorManage(object):
    def __init__(self, decorator):
        '''
        ..codeauthor:: Muthukumar Subramanian
        :param decorator: Actually def 'SqlObjCreate' will present here,
                        Example: @OptionalDecoratorManage(SqlObjCreate)
        '''
        self.deco = decorator

    def __call__(self, func):
        '''
        ..codeauthor:: Muthukumar Subramanian
        :param func: SqlDecoratorSkipCheck.test(.*|2|3|4)
        :return:
        '''
        # self.deco(func) --> SqlObjCreate(SqlDecoratorSkipCheck.test(|2|3|4)),
        # decorator function will execute, then normal def will call
        self.deco = self.deco(func)
        self.func = func  # SqlDecoratorSkipCheck.test, here normal def will call

        def wrapped(*args, **kwargs):
            if kwargs.get("skip_decorator") is True:
                return self.func(*args, **kwargs)  # test will present
            else:
                return self.deco(*args, **kwargs)  # SqlObjCreate will present
        return wrapped


class MuthukumarDb(object):
    def __init__(self, *args, **kwargs):
        self.fail = "FAIL"
        self.log_obj = None
        self.user_lib_obj = None
        if kwargs:
            self.user_lib_obj = kwargs.get('user_lib_obj')
            self.log_obj = kwargs.get('log_obj')
        self.cn = None
        self.cursor_obj = None
        # try:
        #     self.cn = pyodbc.connect(
        #         'DRIVER={SQL Server};SERVER=localhost;DATABASE=user_verification;UID=sa;PWD=P@ssword;')
        #     self.cursor_obj = self.cn.cursor()
        #     # self.log_obj.info("pyobdc object is created successfully...".format())
        #     print("pyobdc object is created successfully...".format())
        # except Exception as err_pyodc:
        #     # self.log_obj.error("Observed exception: {}".format(err_pyodc))
        #     print("Observed exception: {}".format(err_pyodc))

    @OptionalDecoratorManage(SqlObjCreate)
    def Create_new_table(self, create_table_name, login_type, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Create new table for new user admin/user, as now it is disabled
        Usage:
            Required argument(s):
                :param create_table_name: required table name
                :param login_type: either admin or user table
            Optional argument(s):
                :param args: default list
                :param kwargs: default dict
        :return: Boolean
        '''
        succ = None
        login_type = login_type
        if(self.cursor_obj.tables(table=create_table_name, tableType='TABLE').fetchone()):
            self.log_obj.error("Given name: {} is already exists in user_verification "
                               "database".format(create_table_name))
            return False
        if login_type == 'USER':
            string = "CREATE TABLE user_verification.dbo." + create_table_name + "(user_firstname" \
                " varchar(20), user_secondname varchar(20), user_username varchar(20), " \
                "user_email varchar(65), usermobile_number varchar(50), userdate_of_birth "\
                "varchar(50) , user_password varchar(20), user_confirm_password " \
                "varchar(20), PRIMARY KEY ( usermobile_number))"
        elif login_type == 'ADMIN':
            string = "CREATE TABLE admin_verification.dbo." + create_table_name + "(admin_adminname" \
                "varchar(20), admin_email varchar(65), adminmobile_number varchar(50)," \
                "admin_password varchar(20)," \
                "admin_confirm_password varchar(20), PRIMARY KEY (adminmobile_number))"
        try:
            succ = self.cursor_obj.execute(string)
            self.cursor_obj.commit()
        except BaseException:
            pyodbc.ProgrammingError
        if succ:
            self.log_obj.info("Table : {} is created successfully...".format(create_table_name))
            return True
        return False

    @OptionalDecoratorManage(SqlObjCreate)
    def Insert_query(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Insert_query will insert a data into our database table
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'login_type' either admin or user table,
                                required 'admin_table_name', 'admin_adminname' etc... for admin table,
                                required 'user_table_name', 'user_firstname' etc... for user table
            Optional argument(s):
                :param args: default list
        :return: Boolean
        '''
        succ = None
        table_call = None
        login_type = kwargs.get('login_type')
        if login_type == 'ADMIN':
            a_table_name = kwargs.get('admin_table_name')
            table_call = a_table_name
            a_username = kwargs.get('admin_adminname')
            a_mobile_number = kwargs.get('adminmobile_number')
            a_email = kwargs.get('admin_email')
            a_cr_password = kwargs.get('admin_password')
            a_co_password = kwargs.get('admin_confirm_password')
            string = "INSERT INTO admin_verification.dbo." + a_table_name + "(admin_adminname, admin_email," \
                " adminmobile_number, admin_password, admin_confirm_password) VALUES " \
                "('" + a_username + "', '" + a_email + "', '" + a_mobile_number + "'," \
                "'" + a_cr_password + "', '" + a_co_password + "' )"
        elif login_type == 'USER':
            u_table_name = kwargs.get('user_table_name')
            table_call = u_table_name
            u_firstname = kwargs.get('user_firstname')
            u_secondname = kwargs.get('user_secondname')
            u_username = kwargs.get('user_username')
            u_mobile_number = kwargs.get('usermobile_number')
            u_date_of_birth = kwargs.get('userdate_of_birth')
            u_email = kwargs.get('user_email')
            u_cr_password = kwargs.get('user_password')
            u_co_password = kwargs.get('user_confirm_password')
            string = "INSERT INTO user_verification.dbo." + u_table_name + "(user_firstname, user_secondname,"\
                " user_username, user_email, usermobile_number, userdate_of_birth, user_password, "\
                "user_confirm_password) VALUES ('" + u_firstname + "', '" + u_secondname + "',"\
                " '" + u_username + "', '" + u_email + "', '" + u_mobile_number + "'," \
                " '" + u_date_of_birth + "', '" + u_cr_password + "', '" + u_co_password + "' )"
        log_obj = kwargs.get('log_obj')
        try:
            succ = self.object_db.cursor_obj.execute(string)
            self.object_db.cursor_obj.commit()
        except BaseException:
            pyodbc.ProgrammingError
            err_dump = sys.exc_info()
            pat = r".*(Cannot.*\'\.).*"
            for each in err_dump:
                each = str(each)
                matched = re.match(pat, each, re.M | re.I)
                if matched:
                    self.log_obj.error("{}".format(matched.group(1)))
            self.log_obj.error("Issues observed while inserting table values!!!".format())
        if succ:
            self.log_obj.info("User signup data's inserted into *** {} *** table".format(table_call))
            return True
        return False

    @OptionalDecoratorManage(SqlObjCreate)
    def User_and_admin_signin(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        User_and_admin_signin will collect a user/admin table list for validation
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'login_type' either admin or user table,
                                required 'admin_table_name' for admin table,
                                required 'user_table_name' for user table
            Optional argument(s):
                :param args: default list
        :return: database_hash if it executed successfully else self.fail
        '''
        succ = None
        login_type = kwargs.get('login_type')
        if login_type == 'ADMIN':
            table_call = kwargs.get('admin_table_name', 'ADMIN_TABLE')
            table_name_db = 'admin_verification'
        if login_type == 'USER':
            table_call = kwargs.get('user_table_name', 'USER_TABLE')
            table_name_db = 'user_verification'
        log_obj = kwargs.get('log_obj')
        string = "SELECT * FROM " + table_name_db + ".dbo." + table_call
        try:
            self.object_db.cursor_obj.execute(string)
            succ = True
        except BaseException:
            pyodbc.ProgrammingError
            self.log_obj.error("Issues observed while retrieving user/admin data's from Data base!!!".format())
        if succ:
            self.log_obj.info("Signin data's are collected from *** {} *** table".format(table_call))
            results = []
            database_hash = {}
            columns = [column[0] for column in self.object_db.cursor_obj.description]

            def _regex(get_ip):
                pat = r"^(?:(\d{2}-))?(\d{10})$"
                mobile_number = re.match(pat, get_ip, re.M | re.I)
                if mobile_number:
                    mobile_num = mobile_number.group()
                    return mobile_num

            for row in self.object_db.cursor_obj.fetchall():
                results.append(dict(zip(columns, row)))
            for each in results:
                for key, value in each.items():
                    returned_op = _regex(get_ip=value)
                    if returned_op:
                        database_hash[returned_op] = each
            return True, database_hash
        else:
            return False, self.fail

    @OptionalDecoratorManage(SqlObjCreate)
    def Muthu_db(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Muthu_db is main function of the file, this function will redirecting to either signup or signin for admin/user
        when we are executing admin/user signup|in script
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'login_type' either admin or user table,
                                required 'admin_table_name' for admin table,
                                required 'user_table_name' for user table,
                                required 'METHOD' either signup or signin for admin/user,
                                required 'skip_table_create' now default value is 'SKIP'
            Optional argument(s):
                :param args: default list
        :return: ret_var
        '''
        ret_var = None
        login_type = kwargs.get('login_type')
        if login_type == 'ADMIN':
            table_call = kwargs.get('admin_table_name')
        elif login_type == 'USER':
            table_call = kwargs.get('user_table_name')
        u_METHOD = kwargs.get('METHOD')
        ref_f = kwargs.get('log_obj')
        skip_table_create = kwargs.get('skip_table_create', 'SKIP')

        if u_METHOD == 'signup':
            if skip_table_create == 'SKIP':
                if login_type == 'ADMIN':
                    kwargs['admin_table_name'] = 'ADMIN_TABLE'
                elif login_type == 'USER':
                    kwargs['user_table_name'] = 'USER_TABLE'
                (ret) = self.Insert_query(self, *args, **kwargs)
                if not ret:
                    ret_var = "Issues observed while validating Insert_query"
                    return False, ret_var
            else:
                ret = self.Create_new_table(self, create_table_name=table_call, log_obj=ref_f,
                                            login_type=login_type)
                # As of now create table func's are disabled
                if not ret:
                    ret_var = "Issues observed while validating Create_new_table"
                    return False, ret_var
                else:
                    ret = self.Insert_query(self, *args, **kwargs)
                    if not ret:
                        ret_var = "Issues observed while validating Insert_query"
                        return False, ret_var
        elif u_METHOD == 'signin':
            skip_table_create = kwargs.get('skip_table_create')
            if skip_table_create == 'SKIP':
                if login_type == 'ADMIN':
                    kwargs['admin_table_name'] = 'ADMIN_TABLE'
                    (ret, ret_var) = self.User_and_admin_signin(self, *args, **kwargs)
                    if not ret:
                        ret_var = "Issues observed while validating User_and_admin_signin"
                        return False, ret_var
                elif login_type == 'USER':
                    kwargs['user_table_name'] = 'USER_TABLE'
                    (ret, ret_var) = self.User_and_admin_signin(self, *args, **kwargs)
                    if not ret:
                        ret_var = "Issues observed while validating User_and_admin_signin"
                        return False, ret_var
            else:
                (ret, ret_var) = self.User_and_admin_signin(self, *args, **kwargs)  # As of now disabled
                if not ret:
                    ret_var = "Issues observed while validating User_and_admin_signin"
                    return False, ret_var
        return True, ret_var

    @OptionalDecoratorManage(SqlObjCreate)
    def Access_query(self, *args, **kwargs):
        '''
        ..codeauthor:: Muthukumar Subramanian
        Access_query function will execute when we need to do insert|update|delete query on database
        Usage:
            Required argument(s):
                :param kwargs: default dict, required 'login_type' either admin or user table,
                                required 'string_query' which query we need to execute on database,
                                required 'exec_table_name' which table we need to access,
                                required 'log_obj' logger object
            Optional argument(s):
                :param args: default list
        :return: Boolean
        '''
        succ = None
        login_type = kwargs.get('login_type')
        string = kwargs.get('string_query')
        exec_table_name = kwargs.get('exec_table_name')
        log_obj = kwargs.get('log_obj')
        try:
            succ = self.object_db.cursor_obj.execute(string)
            self.object_db.cursor_obj.commit()
        except BaseException:
            pyodbc.ProgrammingError
            err_dump = sys.exc_info()
            print("err_dump:", err_dump)
            pat = r".*(Cannot.*\'\.).*"
            for each in err_dump:
                each = str(each)
                matched = re.match(pat, each, re.M | re.I)
                if matched:
                    self.log_obj.error("{}".format(matched.group(1)))
            self.log_obj.error("Issues observed while executing query!!!".format())
        if succ:
            self.log_obj.info("Query executed Successful on *** {} *** table".format(exec_table_name))
            return True
        return False


if __name__ != '__main__':
    object_db = MuthukumarDb()
