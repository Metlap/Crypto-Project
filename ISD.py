from Utils.utils import Utils
import sqlite3
from sqlite3 import Error
from datetime import datetime
import math


class ISD:
    def __init__(self, isdName):
        self.isdName = isdName
        self.sid = Utils.rand_160()
        self.__Skey = -1

    def store(self, Skey):
        self.__Skey = Skey
        self.__conn = None 
        
        print("Storing in ISD TABLE")
        try:
            self.__conn = sqlite3.connect("./db/ISD.db")
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO ISDTABLE (ISDNAME,SIDJ,SKEYJ) values (?,?,?)",
                           (str(self.isdName), str(self.sid), str(Skey)))
            self.__conn.commit()
            # self.__XGWn = cursor.fetchall()[0][0]
            # print("XGWn: " + str(self.__XGWn))
        except Error as e:
            print(e)

    def authenticateinISD(self, message2):
        TS2_dash = datetime.now()
        threshold = 1000
        c = (TS2_dash-message2[0][4]).total_seconds()
        if (c > threshold):
            print("Timestamps vary by larger than threshold value. Hence access denied")
            return False
        else:
            DIDi = Utils.concat_hash(
                str(message2[1][0]) + str(self.__Skey), message2[0][4]) ^ message2[0][2]
            Ei = message2[0][3] ^ Utils.concat_hash(
                str(self.__Skey), message2[0][4])
            Ag_dash = self.__Skey ^ message2[0][0]
            VSNj_calculated = Utils.concat_hash(str(
                self.__Skey) + str(self.sid) + str(Ag_dash) + str(message2[0][0]), message2[0][4])
            if (VSNj_calculated != message2[0][1]):
                print("Failed at ISDj authentication")
            else:
                rj = Utils.rand_160()
                TS3 = datetime.now()
                Nj = 0  # chebyshev polynomial
                SKij = math.cos(
                    rj*math.acos(str(DIDi) + str(message2[1][0]) + str(Ei)))

    def isdeployed(self):
        return self.__Skey != -1

    def __str__(self):
        return str(self.sid)

    def __repr__(self):
        return str(self.sid)
