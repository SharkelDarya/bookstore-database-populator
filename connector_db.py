import sys
import cx_Oracle
import csv
import json

class ConnectorDB:
    def __init__(self):
        user_name = 's102881'
        password = 's102881'

        with open('database_config.json') as f:
            data = json.load(f)
        
        user_name = data['user_name']
        password = data['password']
        host = data['host']
        port = data['port']
        service_name = data['service_name']

        #try add library OracleClient
        try:
            if sys.platform.startswith("darwin"):
                #lib_dir = os.path.join(os.environ.get("HOME"), "Downloads", "instantclient_21_131")
                lib_dir = "c:\instantclient_19_22"
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            elif sys.platform.startswith("win32"):
                lib_dir= "c:\instantclient_19_22"
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        except Exception as err:
            print("Whoops!")
            print(err)
            sys.exit(1)

        #Try to connect to database
        try:
            dsn = cx_Oracle.makedsn(host=host, port=port, service_name=service_name)
            self.connection = cx_Oracle.connect(user=user_name, password=password, dsn=dsn)
            self.cursor = self.connection.cursor()
            print("Connected to SQLDeveloper :)")
        except cx_Oracle.Error as error:
            print("Error occurred while connecting to the database:", error)
            exit()
    
    def insert_csv_to_database(self, table_name, csv_file):
        try:
            with open('data\\' + csv_file) as f:
                reader = csv.reader(f, delimiter=',', quotechar='"')
                i = -1
                for row in reader:
                    if i == -1:
                        field_list = ','.join(row)
                        i += 1
                        continue
                    value_list = ["'%s'" % r for r in row]
                    value_list = ','.join(value_list)
                    try:
                        with open("Inserts.txt", "a", newline="") as file:
                            file.write("insert into %s (%s) values(%s);\n" % (table_name, field_list, value_list))

                        self.cursor.execute("insert into %s (%s) values(%s)" % (table_name, field_list, value_list))
                        i += 1
                    except cx_Oracle.Error as error:
                        print("Cannot insert: insert into %s (%s) values(%s)" % (table_name, field_list, value_list))
                        print("Error:", error)
        except Exception as e:
            print("Cannot insert data to table:", e)

    def select_query(self, table_name, colum):
        try:
            self.cursor.execute("SELECT %s FROM %s" % (colum, table_name))
            ids = [row[0] for row in self.cursor.fetchall()]
        except cx_Oracle.Error as error:
            print("SELECT %s FROM %s" % (colum, table_name))
            print('Error: ', error)
        return ids

    def close_connection(self):
        self.connection.commit()
        self.connection.close()