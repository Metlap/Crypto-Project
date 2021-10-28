import os
from gateway import Gateway
from Utils.utils import Utils
from user import User
from ISD import ISD
from deploy_ISD import deploy_iot_dev_to_gateway
gateway = 0


def create_gatewaynodes(n):
    # create and store a number of gateway nodes in db
    gwnList = {}
    for i in range(n):
        gatewaynodeName = 'GWN' + str(i)
        # will create 160bit master key for this GWN
        gateway = Gateway(gatewaynodeName)
        gwnList[gatewaynodeName] = gateway
    return gwnList
    # note all these gateway nodes can be stored in a single table


def create_ISD_devices(n):
    isdList = {}
    for i in range(n):
        isd_name = 'ISD' + str(i)
        # create a row with "isdname" (human readable like ISD0)and "isdId" (160 bit id created randomly)
        isdi = ISD(isd_name)
        isdList[isd_name] = isdi  # not the isdi value in the list
    return isdList

# def initISDs():
#     isdList = []
#     for i in range(1, 3):
#         isdList.append(ISD())
#     return isdList


def deploy(isdList, gwnname):
    deploy_iot_dev_to_gateway(isdList, gwnname)


def register(gwn):
    print("Entering User Mode")
    return User.register(gwn)


def login(smartcard, user):
    return(user.login(smartcard))


def authenticate(g, message):
    msg2, current_device = g.authenticate(message)


if __name__ == "__main__":
    # create and store a number of GWNs in db
    num_gwns = input("Enter number of GWNs: ")
    gwnList = create_gatewaynodes(int(num_gwns))
    # create and store a number of IoT devices in db
    num_isds = input("Enter number of ISD devices: ")
    isdList = create_ISD_devices(int(num_isds))
    gwnno = input("Enter a number for GWN: ")
    gwnname = "GWN" + str(gwnno)
    if (gwnname not in gwnList):
        print("Enter a valid gwnName")
    else:
        deploy(isdList, gwnList[gwnname])
    smartcard, user = register(gwnList[gwnname])
    msg1 = login(smartcard, user)
    authenticate(gwnList[gwnname], msg1)
