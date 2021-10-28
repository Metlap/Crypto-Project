import sqlite3
from sqlite3 import Error
from Utils.utils import Utils


class Initializer:
    @staticmethod
    def gwn_db():
        conn = None
        try:
            conn = sqlite3.connect("./db/GWN.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE GWNTABLE(
                            GWNNAME TEXT,
                            SIDJ TEXT,
                            KEYJ TEXT  
            )""")
            cursor.execute("""CREATE TABLE USER(
                            IDI TEXT
            )""")
            cursor.execute("""CREATE TABLE ISD(
                            ISDNAME TEXT,
                            SIDJ TEXT 
            )""")
            cursor.execute("""CREATE TABLE XGWN(
                            GWNNAME TEXT,
                            XGWN TEXT 
            )""")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()

    # @staticmethod
    # def myfunc():
    #     conn = sqlite3.connect("./db/GWN.db")
    #     cursor = conn.cursor()
    #     xgwn = Utils.rand_160()
    #     cursor.execute(
    #         "INSERT INTO XGWN(XGWN) VALUES (?)", (str(xgwn),))
    #     conn.commit()
    #     print(cursor.execute("SELECT * FROM XGWN"))
    #     conn.commit()

    @staticmethod
    def isd_db():
        conn = None
        try:
            conn = sqlite3.connect("./db/ISD.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE ISDTABLE(
                            ISDNAME TEXT,
                            SIDJ TEXT,
                            SKEYJ TEXT  
            )""")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()

    @staticmethod
    def user_db():
        conn = None
        try:
            conn = sqlite3.connect("./db/USER.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE USERTABLE(
                            DIDI TEXT,
                            DPWI TEXT,
                            IDI TEXT,
                            BI TEXT,
                            MI1 TEXT,
                            MI2 TEXT  
            )""")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()

    @staticmethod
    def sc_db():
        conn = None
        try:
            conn = sqlite3.connect("./db/SC.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE SMARTCARDTABLE(
                            LI TEXT,
                            RBI TEXT,
                            CIDASH TEXT,
                            HASHVAL TEXT,
                            TAUI TEXT,
                            T TEXT  
            )""")
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()


if __name__ == '__main__':
    Initializer.gwn_db()
    Initializer.sc_db()
    Initializer.user_db()
    Initializer.isd_db()
    # Initializer.myfunc()
