from datetime import datetime
from Utils.utils import Utils
import sqlite3
from sqlite3 import Error
# fastpbkdf2 - Not compatible with windows for fuzzy Extractor


class SmartCard:
    def __init__(self, Ci, hash_string="sha1"):
        self.__Ci = Ci
        self.hash_function = hash_string

    def imprint(self, bio, b, m1, m2, usrname, pwd):
        self.__sigma = 0
        self.tau = 0
        self.extractor = 0
        self.threshold = 0
        self.L = b ^ Utils.concat_hash(self.__sigma, pwd)
        self.Rb = Utils.concat_hash((usrname + str(self.__sigma)), pwd)
        self.Cd = (self.__Ci ^ m1 ^ m2) ^ Utils.concat_hash(
            self.__sigma, usrname)
        self.__conn = None
        try:
            self.__conn = sqlite3.connect("./db/SC.db")
            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO SMARTCARDTABLE(LI, RBI, CIDASH, HASHVAL, TAUI, T) VALUES(?,?,?,?,?,?)", (
                self.L,
                self.Rb,
                self.Cd,
                self.hash_function,
                self.extractor,
                self.tau,
                self.threshold,
            ))
            self.__XGWn = int(cursor.fetchall()[0][0])
            print("XGWn: " + str(self.__XGWn))
        except Error as e:
            print(e)
        return (
            self.L,
            self.Rb,
            self.Cd,
            self.hash_function,
            self.extractor,
            self.tau,
            self.threshold,
        )

    def verify(self, username, pwd, bio_info):
        self.Dpw = Utils.concat_hash(username, pwd)
        self.__sigmas = 0

        self.bs = self.L ^ Utils.concat_hash(self.__sigmas, pwd)

        if self.Rb == Utils.concat_hash((username + str(self.__sigmas)), pwd):
            self.C = self.Cd ^ Utils.concat_hash(self.__sigmas, username)
            self.Did = Utils.concat_hash(username, self.bs)
            self.J = self.C ^ self.Did ^ self.Dpw
            input_isd_number = input("Enter an ISD Device number : ")
            input_isd_name = "ISD" + str(input_isd_number)
            self.__conn = None
            try:
                self.__conn = sqlite3.connect("./db/ISD.db")
                cursor = self.__conn.cursor()
                cursor.execute(
                    "SELECT SIDJ FROM ISDTABLE WHERE ISDNAME = (?)", (str(input_isd_name),))
                sid = int(cursor.fetchall()[0][0])
                print("sid: " + str(sid))
            except Error as e:
                print(e)
            # sid = input("ENTER DEVICE ID: ")
            self.r = Utils.rand_160()
            self.Ts = datetime.now()  # 32 bits timestamp
            self.E = Utils.concat_hash(
                str(self.J)+str(Utils.concat_hash(self.__sigmas, pwd)), self.Ts)
            self.Ag = 0  # Chebyshev Polynomial
            self.G = self.Ag ^ Utils.concat_hash(
                str(self.Did)+str(self.J), self.Ts)
            self.VGWN = Utils.concat_hash(
                str(self.Did)+str(self.Ag) + str(self.G) + str(sid), self.Ts)
            self.Ed = self.E ^ Utils.concat_hash(
                str(self.Did)+str(self.J), self.Ts)
            self.Didd = self.Did ^ Utils.concat_hash(
                str(self.Ed)+str(self.J), self.Ts)
            self.sidd = int(sid) ^ Utils.concat_hash(self.Did, self.Ts)

            return (self.Ed, self.Didd, self.VGWN, self.G, self.sidd, self.Ts)

    def __str__(self):
        return str(self.__Ci) + " " + str(self.hash_function)
