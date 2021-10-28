import getpass
import random
from Utils.utils import Utils
import sqlite3
from sqlite3 import Error


class User:
    def __init__(self, username, pwd, b, m1, m2, Did, Dpw):
        self.__username = username
        self.__password = pwd
        self.__b = b
        self.__m1 = m1
        self.__m2 = m2
        self.__Did = Did
        self.__Dpw = Dpw
        print("Password       b            m1          m2")
        print("-----------    -----        -----       -----")
        print(
            f"{self.__password}        {self.__b}       {self.__m1}       {self.__m2}"
        )
        self.__bio = Utils.rand_160()
        self.__conn = None
        print("Storing in USER TABLE")
        try:
            self.__conn = sqlite3.connect("./db/USER.db")
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO USERTABLE (DIDI, DPWI, IDI, BI, MI1, MI2) VALUES (?,?,?,?,?,?)", (str(
                self.__Did), str(self.__Dpw), str(self.__username), str(self.__b), str(self.__m1), str(self.__m2)))
            self.__conn.commit()
        except Error as e:
            print(e)

    def addnoise(self, threshold):
        # return int(self.__bio) + int(str(bin(2 ** threshold + 1) - 1))
        return self.__bio - 1

    @staticmethod
    def register(gateway):
        username = input("Enter Username: ")
        pwd = getpass.getpass("Password: ")
        # conn = None
        # try:
        #     conn = sqlite3.connect("./db/USER.db")
        #     cursor = conn.cursor()
        #     cursor.execute(
        #         f"SELECT * FROM USERTABLE WHERE IDI = (?)", (str(username),))
        #     if (len(cursor.fetchall()[0][0]) > 0):
        #         print("User already registered. Proceed to login")
        #     conn.commit()
        # except Error as e:
        #     print(e)
        # Generate 3 random numbers
        b = Utils.rand_160()
        m1 = Utils.rand_160()
        m2 = Utils.rand_160()

        # compute DID and DPW
        Did = Utils.concat_hash(username, b)
        Dpw = Utils.concat_hash(username, pwd)

        print(f' DIDi = {Did}')
        print(f' DPWi = {Dpw}')

        reg_msg1 = (Did ^ m1, Dpw ^ m2)
        # Check validity of both from the gateway
        smart_card = gateway.registerUser(username, reg_msg1)
        if smart_card == None:
            print("Already registered Ui with GWN")
            return None, None
        print(smart_card)
        u = User(username, pwd, b, m1, m2, Did, Dpw)

        # imprint the biometric information
        smart_card.imprint(u.__bio, u.__b, u.__m1, u.__m2,
                           u.__username, u.__password)
        return smart_card, u

    def login(self, smart_card):
        print(f"bio :{self.__bio}")
        print(f"noise :{self.addnoise(5)}")
        msg1 = smart_card.verify(self.__username,
                                 self.__password, self.addnoise(5))
        print(msg1)
        return(msg1)
