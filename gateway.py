# from main import deploy
import os
import sys
import pickle
import hashlib
import sqlite3
from Utils.utils import Utils
from smart_card import SmartCard
from sqlite3 import Error
from datetime import datetime
import datetime


class Gateway:
    def __init__(self, gname):
        self.gwnName = gname
        # a = {"key": 23}
        # pickle.dump(a, open("./GatewayData/isd_data.pickle", "wb"))
        # print(self.__XGWn.bit_length())
        self.__conn = None
        # self.__GWNid = 'G0'
        try:
            self.__conn = sqlite3.connect("./db/GWN.db")
            cursor = self.__conn.cursor()
            self.__Xgwn = Utils.rand_160()
            cursor.execute(
                "INSERT INTO XGWN(GWNNAME, XGWN) VALUES (?,?)", (str(self.gwnName), str(self.__Xgwn)))
            self.__conn.commit()
            print(cursor.execute("SELECT * FROM XGWN"))
            self.__conn.commit()
        except Error as e:
            print(e)

    def deployISD(self, isd):
        # isd_dict = pickle.load(open("./GatewayData/isd_data.pickle", "rb"))
        try:
            self.__conn = sqlite3.connect("./db/GWN.db")
            cursor = self.__conn.cursor()
            cursor.execute(
                "SELECT * FROM GWNTABLE WHERE SIDJ = (?)", (str(isd.sid),))
            # First check if it is already deployed if not deploy
            isd_list = cursor.fetchall()
            print(isd_list)
            if len(isd_list) == 0:
                SKey = Utils.concat_hash(isd.sid, self.__Xgwn)
                Key = SKey ^ self.__Xgwn
                print(f"Skey = {SKey}")
                print(f"Key = {Key}")
                # print(f"SKey = {Key^self.__XGWn}")
                cursor = self.__conn.cursor()
                cursor.execute(
                    "INSERT INTO GWNTABLE(GWNNAME,SIDJ, KEYJ) VALUES (?,?,?)", (str(self.gwnName), str(isd.sid), str(Key)))
                self.__conn.commit()

                isd.store(SKey)
                # isd_dict[isd.sid] = Key
                # f = open("./GatewayData/isd_data.pickle", "r+")
                # f.truncate(0)
                # f.close()
                # pickle.dump(isd_dict, open("./GatewayData/isd_data.pickle", "wb"))
                return 1
            return 0
        except Error as e:
            print(e)

    def registerUser(self, username, reg_msg):
        # Check if Did exists --- How? table having all users -> search for this username in that table
        cursor = self.__conn.cursor()
        cursor.execute(
            "SELECT * FROM USER WHERE IDI = (?)", (str(username),))
        user_list = cursor.fetchall()
        self.Xgwn_Ui = Utils.rand_160()  # Key Exchannge required here?
        Ci = None
        if len(user_list) == 0:
            Ci = (
                reg_msg[0]
                ^ reg_msg[1]
                ^ Utils.concat_hash(self.__Xgwn, Utils.concat_hash(self.Xgwn_Ui, ""))
            )

            # Insert into database
            cursor.execute("INSERT INTO USER (IDI) VALUES (?)",
                           (str(username),))
            self.__conn.commit()
            # Issue SmartCard
            smart_card = SmartCard(Ci, "sha1")
            return smart_card
        return None

    def loginUser(self, a):
        pass

    def authenticate(self, msg1):
        self.ts2 = datetime.datetime.now()
        print("blah hsh")
        b = msg1[5]
        threshold = 1000
        c = (self.ts2-b).total_seconds()
        if (c > threshold):
            print("Timestamps vary by larger than threshold value. Hence access denied")
            return False
        else:
            self.Mi = Utils.concat_hash(
                self.__Xgwn, Utils.concat_hash(self.Xgwn_Ui, ""))
            self.Didi = (msg1[1]) ^ Utils.concat_hash(
                str(msg1[0]) + str(self.Mi), msg1[5])
            self.Agstar = msg1[3] ^ Utils.concat_hash(
                str(self.Didi) + str(self.Mi), msg1[5])
            self.Sidj = msg1[4] ^ Utils.concat_hash(str(self.Didi), msg1[5])
            VGWN_calculated = Utils.concat_hash(
                str(self.Didi) + str(self.Agstar) + str(msg1[3]) + str(self.Sidj), msg1[5])
            print(VGWN_calculated)
            print(msg1[2])
            if (msg1[2] != VGWN_calculated):
                print("Denied access due to invalid message 1 from user to GWN")
                return False
            else:
                Ei = msg1[0] ^ Utils.concat_hash(
                    str(self.Mi) + str(self.Didi), msg1[5])
                self.__conn = None
                Skeyj = 0
                try:
                    self.__conn = sqlite3.connect("./db/GWN.db")
                    cursor = self.__conn.cursor()
                    cursor.execute(
                        f"SELECT KEYJ FROM GWNTABLE WHERE SIDJ LIKE \"{self.Sidj}\"")
                    Skeyj = int(cursor.fetchall()[0][0])
                    print("SKeyj: " + str(Skeyj))
                except Error as e:
                    print(e)
                TS2 = datetime.datetime.now()
                SIDj_double_dash = Utils.concat_hash(
                    str(self.Sidj) + str(Skeyj), TS2) ^ self.Didi
                Hj = Skeyj ^ self.Agstar
                VSNj = Utils.concat_hash(
                    str(Skeyj) + str(self.Sidj) + str(self.Agstar) + str(Hj), TS2)
                Ei_double_dash = Ei ^ Utils.concat_hash(Skeyj, TS2)
                print(Hj, VSNj, SIDj_double_dash, Ei_double_dash, TS2)
                # current_device = self.deployISD(self.Sidj)
                return((Hj, VSNj, SIDj_double_dash, Ei_double_dash, TS2), self.Sidj)
