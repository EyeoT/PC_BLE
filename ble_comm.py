# bluetooth low energy scan
from bluetooth.ble import DiscoveryService, GATTRequester
import sys

class Reader(object):
   def __init__(self, address):
       self.requester = GATTRequester(address, False)
       self.connect()
       self.request_data()


   def connect(self):
       print("Connecting...")
       sys.stdout.flush()


       self.requester.connect(True)
       print("OK!")


   def request_data(self):
       data = self.requester.read_by_uuid(
           board_uuid)[0]
       try:
           print("Device name: " + data.decode("utf-8"))
       except AttributeError:
           print("Device name: " + data)


service = DiscoveryService("hci1")
devices = service.discover(2)
host_MAC_address = '98:4F:EE:0F:7B:A2'
host_MAC_address2 = '98:4F:EE:0F:89:69'
linux_box_MAC_address = '08:3E:8E:E4:E9:58'
board_uuid = '19B10000-E8F2-537E-4F6C-D104768A1214'
board_characteristic = '19B10001-E8F2-537E-4F6C-D104768A1214'


Reader(host_MAC_address2)


#for address, name in devices.items():
   #print("name: {}, address: {}".format(name, address))


req = GATTRequester(host_MAC_address2)
#name = req.read_by_uuid("19B10000-E8F2-537E-4F6C-D104768A1214")
req.write_by_handle(0x0b, "") # handle 0x0b is required
# ON :  # 0x04 as a string
# OFF : # 0x05 as a string


