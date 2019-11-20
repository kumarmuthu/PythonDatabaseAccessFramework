# Author: Muthukumar Subramanian
# v2018.05.13.01 - Added function Create_new_table, Insert_query,
#                   User_and_admin_signin, Muthu_db for singup,signin support
# v2018.06.10.01 - Added email support for signin page
__author__ = "Muthukumar Subramanian"
import pyodbc
import sys
import re
# ========================= Date_time and log print =======
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
global fail
fail = "FAIL"
cn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=user_verification;UID=sa;PWD=P@ssword;')
cursor = cn.cursor()
global u_table_name
global u_firstname
global u_secondname
global u_username
global u_email
global u_mobile_number
global u_date_of_birth
global u_cr_password
global u_co_password
global u_METHOD
global a_table_name
global a_username
global a_mobile_number
global a_email
global a_cr_password
global a_co_password
global login_type
global table_call
global table_name_db
global ref_f

# ======== Create new table for new user ===========


def Create_new_table(create_table_name, dir_obj, login_type):
    succ = None
    login_type = login_type
    if(cursor.tables(table=create_table_name, tableType='TABLE').fetchone()):
        print(Log(log_info="Given name:" + ' ' + create_table_name + ' ' + "is "
                  "already exists in user_verification database\n"))
        dir_obj.write(Log.ret_mu)
        return 0
    if(login_type == 'USER'):
        string = "CREATE TABLE user_verification.dbo." + create_table_name + "(user_firstname" \
            " varchar(20), user_secondname varchar(20), user_username varchar(20), " \
            "user_email varchar(65), usermobile_number varchar(50), userdate_of_birth "\
            "varchar(50) , user_password varchar(20), user_confirm_password " \
            "varchar(20), PRIMARY KEY ( usermobile_number))"
    elif(login_type == 'ADMIN'):
        string = "CREATE TABLE admin_verification.dbo." + create_table_name + "(admin_adminname" \
            "varchar(20), admin_email varchar(65), adminmobile_number varchar(50)," \
            "admin_password varchar(20)," \
            "admin_confirm_password varchar(20), PRIMARY KEY (adminmobile_number))"
    try:
        succ = cursor.execute(string)
        cursor.commit()
    except BaseException:
        pyodbc.ProgrammingError
    if(succ):
        print(Log(log_info=" Table :" + ' ' + create_table_name + ' ' + "is created successfully\n"))
        dir_obj.write(Log.ret_mu)
        return 1
    return 0
# ================================================

# ======== Insert_query ==========================


def Insert_query(**get_input):
    succ = None
    text = None
    login_type = get_input['login_type'] if get_input['login_type'] else text
    if(login_type == 'ADMIN'):
        a_table_name = get_input['admin_table_name'] if get_input['admin_table_name'] else text
        table_call = a_table_name
        a_username = get_input['admin_adminname'] if get_input['admin_adminname'] else text
        a_mobile_number = get_input['adminmobile_number'] if get_input['adminmobile_number'] else text
        a_email = get_input['admin_email'] if get_input['admin_email'] else text
        a_cr_password = get_input['admin_password'] if get_input['admin_password'] else text
        a_co_password = get_input['admin_confirm_password'] if get_input['admin_confirm_password'] else text
        string = "INSERT INTO admin_verification.dbo." + a_table_name + "(admin_adminname, admin_email," \
            " adminmobile_number, admin_password, admin_confirm_password) VALUES " \
            "('" + a_username + "', '" + a_email + "', '" + a_mobile_number + "'," \
            "'" + a_cr_password + "', '" + a_co_password + "' )"

    elif(login_type == 'USER'):
        u_table_name = get_input['user_table_name'] if get_input['user_table_name'] else text
        table_call = u_table_name
        u_firstname = get_input['user_firstname'] if get_input['user_firstname'] else text
        u_secondname = get_input['user_secondname'] if get_input['user_secondname'] else text
        u_username = get_input['user_username'] if get_input['user_username'] else text
        u_mobile_number = get_input['usermobile_number'] if get_input['usermobile_number'] else text
        u_date_of_birth = get_input['userdate_of_birth'] if get_input['userdate_of_birth'] else text
        u_email = get_input['user_email'] if get_input['user_email'] else text
        u_cr_password = get_input['user_password'] if get_input['user_password'] else text
        u_co_password = get_input['user_confirm_password'] if get_input['user_confirm_password'] else text
        string = "INSERT INTO user_verification.dbo." + u_table_name + "(user_firstname, user_secondname,"\
            " user_username, user_email, usermobile_number, userdate_of_birth, user_password, "\
            "user_confirm_password) VALUES ('" + u_firstname + "', '" + u_secondname + "',"\
            " '" + u_username + "', '" + u_email + "', '" + u_mobile_number + "'," \
            " '" + u_date_of_birth + "', '" + u_cr_password + "', '" + u_co_password + "' )"
        # string = "INSERT INTO user_verification.dbo." + user_table_name + "
        # "(user_name,user_password,mobile_number) VALUES ('zxc','zxc','91-0123456789')"
        # string = "DELETE " + user_table_name + " WHERE mobile_number = '91-0123456789'"
    dir_obj = get_input['dir_obj'] if get_input['dir_obj'] else text
    try:
        succ = cursor.execute(string)
        cursor.commit()
    except BaseException:
        pyodbc.ProgrammingError
        err_dump = sys.exc_info()
        pat = r".*(Cannot.*\'\.).*"
        for each in err_dump:
            each = str(each)
            matched = re.match(pat, each, re.M | re.I)
            if(matched):
                print(Log(log_info=matched.group(1) + "\n"))
                dir_obj.write(Log.ret_mu)
            else:
                next
        print(Log(log_info="Issues observed while inserting user signup data's\n"))
        dir_obj.write(Log.ret_mu)
    if(succ):
        print(Log(log_info="User signup data's inserted into " + " *** "
                  + table_call + ' ***' + ' ' + "table\n"))
        dir_obj.write(Log.ret_mu)
        return 1
    return 0
# ================================================
# ==============User/Admin Signin ==========================


def User_and_admin_signin(**get_input):
    succ = None
    login_type = get_input.get('login_type')
    if(login_type == 'ADMIN'):
        table_call = get_input.get('admin_table_name', 'ADMIN_TABLE')
        table_name_db = 'admin_verification'
    if(login_type == 'USER'):
        table_call = get_input.get('user_table_name', 'USER_TABLE')
        table_name_db = 'user_verification'
    dir_obj = get_input.get('dir_obj')
    string = "SELECT * FROM " + table_name_db + ".dbo." + table_call
    try:
        cursor.execute(string)
        succ = 1
    except BaseException:
        pyodbc.ProgrammingError
        print(Log(log_info="Issues observed while retrieving user data's from Data base\n"))
        dir_obj.write(Log.ret_mu)
    if(succ):
        print(Log(log_info="Signin data's are collected from" + ' *** ' + table_call + ' ***'
                  + ' ' + "table\n"))
        dir_obj.write(Log.ret_mu)
        results = []
        database_hash = {}
        columns = [column[0] for column in cursor.description]

        def _regex(get_ip):
            pat = r"^(?:(\d{2}-))?(\d{10})$"
            mobile_number = re.match(pat, get_ip, re.M | re.I)
            if mobile_number:
                mobile_num = mobile_number.group()
                return mobile_num

        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        for each in results:
            for key, value in each.items():
                returned_op = _regex(get_ip=value)
                if returned_op:
                    database_hash[returned_op] = each
        return 1, database_hash
    else:
        return 0, fail
# ================================================

# ======== Main function ==========================


def Muthu_db(**get_input):
    text = None
    login_type = get_input['login_type'] if get_input['login_type'] else text
    if(login_type == 'ADMIN'):
        table_call = get_input['admin_table_name'] if get_input['admin_table_name'] else text
    elif(login_type == 'USER'):
        table_call = get_input['user_table_name'] if get_input['user_table_name'] else text

    u_METHOD = get_input['METHOD'] if get_input['METHOD'] else text
    ref_f = get_input['dir_obj'] if get_input['dir_obj'] else text
    skip_table_create = get_input['skip_table_create'] if get_input['skip_table_create'] else text
    if(u_METHOD == 'signup'):
        if(skip_table_create == 'SKIP'):
            if(login_type == 'ADMIN'):
                get_input['admin_table_name'] = 'ADMIN_TABLE'
            elif(login_type == 'USER'):
                get_input['user_table_name'] = 'USER_TABLE'
            (ret) = Insert_query(**get_input)
            if(not ret):
                text = "Issues observed while validating Insert_query"
                return 0, text
        else:
            (ret) = Create_new_table(create_table_name=table_call, dir_obj=ref_f,
                                     login_type=login_type)
            # As of now create table func's are disabled
            if(not ret):
                text = "Issues observed while validating Create_new_table"
                return 0, text
            else:
                (ret) = Insert_query(**get_input)
                if(not ret):
                    text = "Issues observed while validating Insert_query"
                    return 0, text
    elif(u_METHOD == 'signin'):
        skip_table_create = get_input['skip_table_create'] if get_input['skip_table_create'] else text
        if(skip_table_create == 'SKIP'):
            if(login_type == 'ADMIN'):
                get_input['admin_table_name'] = 'ADMIN_TABLE'
                (ret, text) = User_and_admin_signin(**get_input)
                if(not ret):
                    text = "Issues observed while validating User_and_admin_signin"
                    return 0, text
            elif(login_type == 'USER'):
                get_input['user_table_name'] = 'USER_TABLE'
                (ret, text) = User_and_admin_signin(**get_input)
                if(not ret):
                    text = "Issues observed while validating User_and_admin_signin"
                    return 0, text
        else:
            (ret, text) = User_and_admin_signin(**get_input)  # As of now disabled
            if(not ret):
                text = "Issues observed while validating User_and_admin_signin"
                return 0, text
    return 1, text
# =================================================

# ======== Admin access ==========================


def Access_query(**get_input):
    succ = None
    text = None
    login_type = get_input['login_type'] if get_input['login_type'] else text
    string = get_input['string_query'] if get_input['string_query'] else text
    # query_option = get_input['query_option'] if get_input['query_option'] else text
    exec_table_name = get_input['exec_table_name'] if get_input['exec_table_name'] else text
    dir_obj = get_input['dir_obj'] if get_input['dir_obj'] else text
    try:
        succ = cursor.execute(string)
        cursor.commit()
    except BaseException:
        pyodbc.ProgrammingError
        err_dump = sys.exc_info()
        print("err_dump:", err_dump)
        pat = r".*(Cannot.*\'\.).*"
        for each in err_dump:
            each = str(each)
            matched = re.match(pat, each, re.M | re.I)
            if(matched):
                print(Log(log_info=matched.group(1) + "\n"))
                dir_obj.write(Log.ret_mu)
            else:
                next
        print(Log(log_info="Issues observed while executing query\n"))
        dir_obj.write(Log.ret_mu)
    if(succ):
        print(Log(log_info="Query executed Successful on " + ' *** '
                  + exec_table_name + ' ***' + ' ' + "table\n"))
        dir_obj.write(Log.ret_mu)
        return 1
    return 0
# ================================================
