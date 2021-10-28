import os
from gateway import Gateway
from Utils.utils import Utils
from user import User
from ISD import ISD


# #need a gateway node --> get it from gwn db
# #-----------
# gwn0 = ''

# #need a iot device --> get it from db
# iot_list = []
# purpose is to create a number of Gateway nodes, users and iot devices
def deploy_iot_dev_to_gateway(iot_list, gwn):
    # deploying iot devices to gateway node
    print("Deploying")
    for isd in iot_list.values():
        print("ISD SID: " + isd.__str__())
        gwn.deployISD(isd)
    # expected output is S_keyj
