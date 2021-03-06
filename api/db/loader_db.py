
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# python standard library

# local pret classes
from sql_operation import *
import mytime
from modules import getinfo
from sqlconn import *

#database = "api/db/MODULESDATA"  #Database Name
#db = connect_db(database)  #Connect Database
#sql_exec = sql(db)        
#times = mytime.Mytime()   #Get My Time

class conn_db(object):
    def __init__(self):
        self.database = "api/db/PLDATA"  #Database Name
        self.db = connect_db(self.database)  #Connect Database
        self.sql_exec = sql(self.db)        
        self.times = mytime.Mytime()   #Get My Time

class loadDB(object):

    '''
    @ init PWD
    '''
    def __init__(self,PWD):
        self.PWD = PWD
        self.conn_db = conn_db()
    '''
    @ Check Module Exist
    '''
    def check_modules(self):
        #sql_up = "UPDATE STATUS set FLAG = 'True' WHERE ID = 1"
        sql = "SELECT FLAG FROM STATUS WHERE ID =1"
        flag_get = self.conn_db.sql_exec.select(sql)
        for row in flag_get:
            flag = row[0]
        if flag == "False":
            sqlexec = SqlExec(self.PWD,self.conn_db.times,self.conn_db.sql_exec) 
            sqlexec.insert_poc_name()
        if flag == "True":
            sqlexec = SqlExec(self.PWD,self.conn_db.times,self.conn_db.sql_exec) 
            sqlexec.exist_poc()

    def show_modules(self):
        #Load pl_show_all_poc_info Function
        show = ShowSql(self.conn_db.sql_exec)
        show.pl_show_all_poc_info()

    def search_modules(self,POC_NAME):
        #Load print_poc_name_info Function
        search = ShowSql(self.conn_db.sql_exec)
        search.print_poc_name_info(POC_NAME)


#=================================================================
def test():
    cursor = sql_exec.select()
    for row in cursor:
        print "poc_name = ", row[0]
        print "poc_name_path = ", row[1]
        print "date = ", row[2]
    sql_exec.db_close()
    #cursor = sql_exec.insert(poc_name,poc_name_path,date)
    #insert_module()



    
