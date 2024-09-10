# Under development
import mysql.connector
from logging import info

class MysqlUtil:

    def __init__(self, mysql_host, mysql_user_name, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_user_name = mysql_user_name
        self.mysql_password = mysql_password
        self.conn = mysql.connector.connect(host=mysql_host,
                                       user=mysql_user_name,
                                       passwd=mysql_password,
                                       auth_plugin='mysql_native_password')

    def update_records_query(self,sql_query=""):
        info("Starting DB connection")
        cursor = self.conn.cursor()
        cursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;')
        cursor.execute(sql_query)
        cursor.close()

    def get_records_from_query(self,sql_query=""):
        info("Starting DB connection")
        cursor = self.conn.cursor()
        cursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;')
        cursor.execute(sql_query)
        all_records = cursor.fetchall()
        records_count = cursor.rowcount
        info("Total records found {}".format(records_count))
        cursor.close()
        return all_records
