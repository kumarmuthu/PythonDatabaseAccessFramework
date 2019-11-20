# Author: Muthukumar Subramanian
# v2018.07.15.01 - Developed Database_access function to update/read/delete specific user/admin credentials
__author__ = "Muthukumar Subramanian"
import sys
import re
# from beautifultable import BeautifulTable
from prettytable import PrettyTable
# ========================= Database import ===============
from MUTHUKUMAR_DB import *
# =========================================================
# ========================= Date_time and log print =======
from MUTHUKUMAR_TIME_DATE import *
# =========================================================
# ================ Muthu_email for send an email ==========
from MUTHUKUMAR_EMAIL import *
# =========================================================
admin_log = 'MUTHUKUMAR_APP_ADMIN_ACCESS_LOG'
(ok, ref_f) = Create_dir(dir_name=admin_log)
global fail
fail = "FAIL"
global get_input
E_mail_failed = 1
E_mail_send = None
access_option = None
int_table_option = None
selected_query_access = None
print(Log(log_info="***** admin ACCESS page start *****\n"))
ref_f.write(Log.ret_mu)


# ######################     READ   ######################
def _read_query(**get_input):
    text = None
    return_op = get_input['return_op'] if(get_input['return_op']) else text
    login_type = get_input['login_type'] if(get_input['login_type']) else text
    table = PrettyTable()
    LIST_key = []
    LIST_value = []
    LIST_value_final = []
    for key, value in return_op.items():
        for key_1, value_1 in value.items():
            LIST_key.append(key_1)
            LIST_value.append(value_1)
    # removing duplicated column ofget_input['all_query_access'] list
    sordered_key = []
    for i in LIST_key:
        if i not in sordered_key:
            sordered_key.append(i)
    length_column = len(sordered_key)
    # split with DB table column count
    for i in range(0, len(LIST_value), length_column):
        LIST_value_final.append(LIST_value[i:i + length_column])
    table.field_names = sordered_key
    for j in LIST_value_final:
        table.add_row(j)
    print(Log(log_info="Displaying" + " " + login_type + " " + "data base Data(s):\n" + str(table)))
    ref_f.write(Log.ret_mu)
    return 1


def Database_access(**get_input):
    query_option = get_input['query_option']
    login_type = get_input['login_type']
    get_input['dir_obj'] = ref_f
    count_break = get_input['count_break']
    table_name = None
    text = None
    if(login_type == 'USER'):
        database_name = 'user_verification'
        table_name = get_input['user_table_name'] if(get_input['user_table_name']) else text
    else:
        database_name = 'admin_verification'
        table_name = get_input['admin_table_name'] if(get_input['admin_table_name']) else text
    (ok_ret, return_op) = User_and_admin_signin(**get_input)
    if(count_break < 20):
        if(query_option == 'read'):
            get_input['return_op'] = return_op
            ret_q = _read_query(**get_input)
            if(not ret_q):
                print(Log(log_info="Issues observed while executing Func--> _read_query \n"))
                ref_f.write(Log.ret_mu)
            print(Log(log_info="\n***** Admin selected option is : READ ,so next query "
                      "execution is denied. Login/Run again and continue your access *****\n"))
            ref_f.write(Log.ret_mu)
            return (1, 'break')
        # ######################     INSERT   ######################
        elif(query_option == 'insert'):
            print(Log(log_info="####### Implement later #######"))
            ref_f.write(Log.ret_mu)
            # string = "INSERT INTO user_verification.dbo." + user_table_name + "
            # "(user_name,user_password,mobile_number) VALUES ('zxc','zxc','91-0123456789')"

        # ######################   UPDATE   #######################
        elif(query_option == 'update'):
            get_input['return_op'] = return_op
            ret_q = _read_query(**get_input)
            if(not ret_q):
                print(Log(log_info="Issues observed while executing Func--> _read_query \n"))
                ref_f.write(Log.ret_mu)
            print(Log(log_info="Please enter mobile number to make an update \n"))
            ref_f.write(Log.ret_mu)
            finalmobile_number = None
            input_mn = (sys.stdin.readline())
            pat = r"^(\d{2})-(\d{10})$"
            mobile_number = re.match(pat, input_mn, re.M | re.I)
            if mobile_number:
                print(Log(log_info="Its a valid Mobile Number :" + mobile_number.group() + "\n"))
                ref_f.write(Log.ret_mu)
                finalmobile_number = mobile_number.group()
            else:
                print(Log(log_info="Entered Mobile Number is Invalid:" + ' ' + input_mn + "\n"))
                ref_f.write(Log.ret_mu)
                print(Log(
                    log_info="Try again Mobile Number ((You can use this format:: "
                    "country code(2 digit) and Number(10 digit) [xx-xxxxxxxxxx] "
                    "Example : 91-9566067570 )\n"))
                ref_f.write(Log.ret_mu)
                i = 0
                while True:
                    i = i + 1
                    mobile_number_2 = (sys.stdin.readline())
                    mobile_number_3 = re.match(pat, mobile_number_2, re.M | re.I)
                    if mobile_number_3:
                        print(Log(log_info="Its a valid Mobile Number :" + mobile_number_3.group() + "\n"))
                        ref_f.write(Log.ret_mu)
                        finalmobile_number = mobile_number_3.group()
                        break
                    else:
                        print(Log(log_info="Given mobile number is invalid:" + ' ' + mobile_number_2 + "\n"))
                        ref_f.write(Log.ret_mu)
                        if(i == 2):
                            print(Log(log_info="This is your last attempt\n"))
                            ref_f.write(Log.ret_mu)
                        if(i >= 3):
                            break
            db_matched_num = None
            set_num = None
            which_column = None
            what_value = None
            str_which_column = None
            str_what_value = None
            for key, value in return_op.items():
                if(key == finalmobile_number):
                    for key_1, value_2 in value.items():
                        pat_column = ".*mobile_number"
                        pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                        if(pat_column_2):
                            db_matched_num = pat_column_2.group()
                            set_num = return_op[finalmobile_number][db_matched_num]
            if(set_num is None):
                print(Log(log_info="Admin entered number is not found on Data base entry!!!\n"))
                ref_f.write(Log.ret_mu)
                print(Log(log_info="Try again!!!\n"))
                ref_f.write(Log.ret_mu)
            else:
                print(Log(log_info="Which column need to update!\n"))
                ref_f.write(Log.ret_mu)
                which_column = (sys.stdin.readline())
                which_column = which_column.strip()
                try:
                    str_which_column = str(which_column)
                except ValueError as err:
                    pass
                print(Log(log_info="What value need to replace!\n"))
                ref_f.write(Log.ret_mu)
                what_value = (sys.stdin.readline())
                what_value = what_value.strip()
                try:
                    str_what_value = str(what_value)
                except ValueError as err:
                    pass
                if(str_which_column and str_what_value):
                    query = "UPDATE " + database_name + ".dbo." + table_name + " SET " + str_which_column + \
                        " = \'" + str_what_value + "\' WHERE " + db_matched_num + " = \'" + set_num + "\'"
                    get_input['string_query'] = query
                    get_input['exec_table_name'] = table_name
                    (ret) = Access_query(**get_input)
                    if(not ret):
                        print("Issues observed while executing Func--> Access_query \n")
                        ref_f.write(Log.ret_mu)
                    else:
                        (ok_ret, return_op) = User_and_admin_signin(**get_input)
                        get_input['return_op'] = return_op
                        ret_q = _read_query(**get_input)
                        if(not ret_q):
                            print(Log(log_info="Issues observed while executing Func--> _read_query \n"))
                            ref_f.write(Log.ret_mu)
                else:
                    print(Log(log_info="Try again!!!\n"))
                    ref_f.write(Log.ret_mu)
        # ######################      DELETE      #######################
        elif(query_option == 'delete'):
            ref_f.write(Log.ret_mu)
            # string = "DELETE " + user_table_name + " WHERE mobile_number = '91-0123456789'"
            get_input['return_op'] = return_op
            ret_q = _read_query(**get_input)
            if(not ret_q):
                print(Log(log_info="Issues observed while executing Func--> _read_query \n"))
                ref_f.write(Log.ret_mu)
            print(Log(log_info="Please enter mobile number to delete a Admin\\User account \n"))
            ref_f.write(Log.ret_mu)
            finalmobile_number = None
            input_mn = (sys.stdin.readline())
            pat = r"^(\d{2})-(\d{10})$"
            mobile_number = re.match(pat, input_mn, re.M | re.I)
            if mobile_number:
                print(Log(log_info="Its a valid Mobile Number :" + mobile_number.group() + "\n"))
                ref_f.write(Log.ret_mu)
                finalmobile_number = mobile_number.group()
            else:
                print(Log(log_info="Entered Mobile Number is Invalid:" + ' ' + input_mn + "\n"))
                ref_f.write(Log.ret_mu)
                print(Log(
                    log_info="Try again Mobile Number ((You can use this format::"
                    " country code(2 digit) and Number(10 digit) [xx-xxxxxxxxxx] "
                    "Example : 91-9566067570 )\n"))
                ref_f.write(Log.ret_mu)
                i = 0
                while True:
                    i = i + 1
                    mobile_number_2 = (sys.stdin.readline())
                    mobile_number_3 = re.match(pat, mobile_number_2, re.M | re.I)
                    if mobile_number_3:
                        print(Log(log_info="Its a valid Mobile Number :" + mobile_number_3.group() + "\n"))
                        ref_f.write(Log.ret_mu)
                        finalmobile_number = mobile_number_3.group()
                        break
                    else:
                        print(Log(log_info="Given mobile number is invalid:" + ' ' + mobile_number_2 + "\n"))
                        ref_f.write(Log.ret_mu)
                        if(i == 2):
                            print(Log(log_info="This is your last attempt\n"))
                            ref_f.write(Log.ret_mu)
                        if(i >= 3):
                            break
            db_matched_num_of_column = None
            set_num = None
            which_column = None
            which_num_del = None
            str_which_column = None
            str_which_num_del = None
            for key, value in return_op.items():
                if(key == finalmobile_number):
                    for key_1, value_2 in value.items():
                        pat_column = ".*mobile_number"
                        pat_column_2 = re.match(pat_column, key_1, re.M | re.I)
                        if(pat_column_2):
                            db_matched_num_of_column = pat_column_2.group()
                            set_num = return_op[finalmobile_number][db_matched_num_of_column]
            if(set_num is None):
                print(Log(log_info="Admin entered number is not found on Data base entry!!!\n"))
                ref_f.write(Log.ret_mu)
                print(Log(log_info="Try again!!!\n"))
                ref_f.write(Log.ret_mu)
            else:
                print(Log(log_info="Re-enter->>>(confirmation) Which mobile number need to delete!\n"))
                ref_f.write(Log.ret_mu)
                which_num_del = (sys.stdin.readline())
                which_num_del = which_num_del.strip()
                try:
                    str_which_num_del = str(which_num_del)
                except ValueError as err:
                    pass
                if(set_num == str_which_num_del):
                    query = "DELETE " + database_name + ".dbo." + table_name + " WHERE " + \
                        db_matched_num_of_column + " = \'" + str_which_num_del + "\'"
                    get_input['string_query'] = query
                    get_input['exec_table_name'] = table_name
                    (ret) = Access_query(**get_input)
                    if(not ret):
                        print("Issues observed while executing Func--> Access_query \n")
                        ref_f.write(Log.ret_mu)
                    else:
                        (ok_ret, return_op) = User_and_admin_signin(**get_input)
                        get_input['return_op'] = return_op
                        ret_q = _read_query(**get_input)
                        if(not ret_q):
                            print(Log(log_info="Issues observed while executing Func--> _read_query \n"))
                            ref_f.write(Log.ret_mu)
                else:
                    print(Log(log_info="Miss matched Try again!!!\n"))
                    ref_f.write(Log.ret_mu)

    elif(count_break >= 20):
        print(Log(log_info="***** Access denied while using more than 20(tms) *****\n"))
        ref_f.write(Log.ret_mu)
        return (1, 'break')

    return (1, 'unbreak')


print(Log(log_info="***** Selected table to access Database query: User_Table[1] Admin_Table[2]*****\n"))
ref_f.write(Log.ret_mu)
while_control = 1
while True:
    table_option = (sys.stdin.readline())
    table_option = table_option.strip()
    try:
        int_table_option = int(table_option)
    except ValueError as err:
        pass
    if(int_table_option == 1):
        get_input = {'login_type': 'USER', 'user_table_name': 'USER_TABLE'}
        print(Log(log_info="User_Table will access\n"))
        ref_f.write(Log.ret_mu)
        break
    elif(int_table_option == 2):
        get_input = {'login_type': 'ADMIN', 'admin_table_name': 'ADMIN_TABLE'}
        print(Log(log_info="Admin_Table will access\n"))
        ref_f.write(Log.ret_mu)
        break
    else:
        get_input = None
        while_control = 0
        print(Log(log_info="Admin gave an invalid option!!!.\n"))
        ref_f.write(Log.ret_mu)
        break

count_break = 0
if(while_control):
    print(Log(log_info="Note: Admin Access will denied while using more than 20(tms)\n"))
    ref_f.write(Log.ret_mu)
    while True:
        print(Log(log_info="<<<<<*** Choose your operation ***>>>>>\n"))
        ref_f.write(Log.ret_mu)
        print(Log(log_info="SELECT-1 [READ], SELECT-2 [INSERT], SELECT-3 [UPDATE], "
                "SELECT-4 [DELETE], SELECT-5 [EXIT] =======\n"))
        ref_f.write(Log.ret_mu)
        int_access_option = None
        exec_option = {'1': 'read', '2': 'insert', '3': 'update', '4': 'delete', '5': 'exit'}
        access_option = (sys.stdin.readline())
        access_option = access_option.strip()
        try:
            int_access_option = int(access_option)
        except ValueError as err:
            pass
        count_break = count_break + 1
        if(int_access_option):
            if((int_access_option > 5) or (int_access_option == -1) or (int_access_option == 0)):
                get_input = 0
                break
            elif(int_access_option == 5):
                print(Log(log_info="Exiting Database access...\n"))
                ref_f.write(Log.ret_mu)
                break
            else:
                query_option_selected = exec_option[str(int_access_option)]
                get_input['query_option'] = query_option_selected
                get_input['exec_option'] = exec_option
                get_input['count_break'] = count_break
                # Func -> Database_access
                (ret, ref_dba) = Database_access(**get_input)
                if(not ret):
                    print(Log(log_info="Issues observed while validating Database_access\n"))
                    break
                else:
                    E_mail_failed = 0
                    if(ref_dba == 'break'):
                        break
        else:
            break


print(Log(log_info="***** admin ACCESS page end *****\n"))
ref_f.write(Log.ret_mu)
if(not E_mail_failed):
    print(Log(log_info="If you want to send an email, please give your option: (Yes/y or No/n)\n"))
    ref_f.write(Log.ret_mu)
    loop_count = 0
    while True:
        loop_count = loop_count + 1
        email_skip = (sys.stdin.readline())
        print(Log(log_info="Selected option is: " + email_skip))
        ref_f.write(Log.ret_mu)
        if(re.match(r'Yes|y', email_skip, re.M | re.I)):
            print(Log(log_info="Email will send to admin Email-id for backup...\n"))
            ref_f.write(Log.ret_mu)
            print(Log(log_info="Enter admin Email-id: \n"))
            ref_f.write(Log.ret_mu)
            E_mail_send = 1
            admin_email_id = (sys.stdin.readline())
            print(Log(log_info="Entered admin Email-id is: " + admin_email_id + '\n'))
            ref_f.write(Log.ret_mu)
            break
        elif(re.match(r'No|n', email_skip, re.M | re.I)):
            print(Log(log_info="Email will not send to admin Email-id!.\n"))
            ref_f.write(Log.ret_mu)
            break
        else:
            print(Log(log_info="admin gave invalid option!!!.\n"))
            ref_f.write(Log.ret_mu)
            if(loop_count == 2):
                print(Log(log_info="This is your last attempt\n"))
                ref_f.write(Log.ret_mu)
            if(loop_count >= 3):
                break
ref_f.close()
if(E_mail_send):
    if(admin_email_id is not None):
        get_input = {'user_email': admin_email_id, 'log_dir': admin_log}
        e_ret = Muthu_email(**get_input)
        if(not e_ret):
            print(Log(log_info="Issues observed while validating Muthu_email\n"))
    else:
        print(Log(log_info="Admin given EMAIL-ID is invalid/empty, hence unable "
                  "to send an email to admin email id...! \n"))
else:
    print(Log(log_info="Unable to send an email...! \n"))
# ========================= End page ================
