# python_database_access
Python database access created for windows, need changes if you want to execute this script on linux.

Script Main execution file name:
* MuthukumarDbExecuteTest.py

Have two framework utility:
* MuthukumarDbUtility.py      -->>>>> import file
* MuthukumarDbUtilityCall.py  -->>>>> default script dict map is there

User library:
* MuthukumarUserLib.py

Database library:
* MuthukumarDb.py

Example class file:
* MuthukumarClass.py

Script execution:

	1) How to execute the script form Pycharm: with runtime argument(argparse)
	
	edit configurations =>>>
	Script path: F:\Python\script\DB_Scripts\09_sep_2019\MuthukumarDbExecuteTest.py

	Parameters: --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignin.py,F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	Example 1: (single script execution)
	Parameters: --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	Example 2: (space after comma)
	Parameters: --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignin.py ,F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	Example 3: (comma after space)
	Parameters: --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignin.py, F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	Example 3: (with space)
	Parameters: --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarDbAdminSignin.py F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	2) Run from windows command prompt:

 	C:\Users\muthukumar>python F:\Python\script\DB_Scripts\09_sep_2019\MuthukumarDbExecuteTest.py --email noreplymuthukumar@gmail.com --script-path F://Python//script//DB_Scripts//09_sep_2019//MuthukumarClass.py

	3) without runtime argument(argparse):
	C:\Users\muthukumar>python F:\Python\script\DB_Scripts\09_sep_2019\MuthukumarDbExecuteTest.py

	Notes: We can execute any one of the script from dict map(mapping dict is available in this scriptMuthukumarDbUtilityCall.py)

Log:
        View link🔗: http://htmlpreview.github.io/

	If you want to see HTML log on web browser, please use this link. Just copy and paste full path. 

	View link🔗: http://htmlpreview.github.io/
	1) Go to log location:
	python_database_access/Logs

	2) Select any folder:
	python_database_access/Logs/MUTHUKUMAR_DB_UTILITY_LOG_02_10_2019_19_58_26_5776/

	3) Open any HTML log:
	MUTHUKUMAR_DB_EXECUTE_TEST_LOG_02_10_2019_19_58_26_5776.html

	Then copy full URI path and paste that link into http://htmlpreview.github.io/ 🔗:

	https://github.com/kumarmuthu/python_database_access/blob/master/Logs/MUTHUKUMAR_DB_UTILITY_LOG_02_10_2019_19_58_26_5776/MUTHUKUMAR_DB_EXECUTE_TEST_LOG_02_10_2019_19_58_26_5776.html

	Example is available on: 
	HTML log viewer snapshot
