# coding=utf-8
# import hardware_constants
# from ble_commands import Commands
from bluetooth.ble import DiscoveryService, GATTRequester
import sys

#  defined commands (constant)
no_light = 0x00  # turn off all indicator lights
red_light = 0x01  # turn indicator lights red
green_light = 0x02  # turn indicator lights green
blue_light = 0x03  # turn indicator lights blue
servo_on = 0x04  # move light switch into on position
servo_off = 0x05  # move light switch into off position
command_ack = 0x97  # response acknowledgement from IoT device
command_success = 0x98  # response from IoT device saying command executed successfully
command_failure = 0x99  # response from IoT device saying command failed to be properly executed

ble_commands_text = {
        0x00: 'Turn colors off',
        0x01: 'Turn color red',
        0x02: 'Turn color green',
        0x03: 'Turn color blue',
        0x04: 'Turn light on',
        0x05: 'Turn light of',
        0x97: 'Command acknowledged by IoT device',
        0x98: 'Command successfully carried out by IoT device',
        0x99: 'Command failed to be carried out by IoT device'
    }

ble_commands_hex = {
    no_light: "",
    red_light: "",
    green_light: "",
    blue_light: "",
    servo_on: "",
    servo_off: "",
    command_ack: "",
    command_success: "",
    command_failure: ""
    }



# constant values from Arduino 101 and Ubuntu laptop
eyeot_macs = ['98:4F:EE:0F:7B:A2','98:4F:EE:0F:89:69']  # MAC addresses of authorized Arduino 101 BLE boards
laptop_MAC_address = '08:3E:8E:E4:E9:58' # MAC address of authorized master BLE - enabled laptop
laptop_hci_num = 'hci0'  # which Bluetooth radio to use
arduino_uuid = '19B10000-E8F2-537E-4F6C-D104768A1214'  # static UUID of Arduino 101 BLE service
arduino_characteristic = '19B10001-E8F2-537E-4F6C-D104768A1214'  # static UUID of Arduino 101 BLE characteristic
arduino_handle = 0x0b  # static characteristic handle to read to and write from
arduino_name = 'LightSwitch' # name all Arduino boards should broadcast

"""
IoTDevice represents a single Eyeot IoT (Arduino 101) BLE device, initialized by one of several authorized MAC
addresses.

Input:

Values:

"""


class IoTDevice(object):
    def __init__(self, address):
        self.address = address
        self.uuid = arduino_uuid
        self.characteristic = arduino_characteristic
        self.handle = arduino_handle

# for testing only, replacing DiscoveryService on mac os


#class devices(object):
        #def __init__(self):

class BLEMaster(object):
   def __init__(self, address):
       self.requester = GATTRequester(address, False)
       self.connect()
       #self.request_data()


   def connect(self):
       print("Connecting...")
       sys.stdout.flush()


       self.requester.connect(True)
       print("OK!")


   def request_data(self):
       data = self.requester.read_by_uuid(arduino_uuid)[0]
       try:
           print("Device name: " + data.decode("utf-8"))
       except AttributeError:
           print("Device name: " + data)

"""
This function performs a BLE scan, finding all possible devices in range. It compares each device's name and MAC
address against those already whitelisted. It returns a list of any authorized devices.

Input: None

Output: authorized_devices, a list of authorized MAC addresses to connect to
"""


def search_for_authorized_eyeot_devices():
    authorized_devices = list()
    service = DiscoveryService(laptop_hci_num)  # use the USB BLE dongle at hci1, not the integrated Bluetooth card at hci0
    devices = service.discover(2)       # find all possible nearby BLE devices

    for address, name in devices.items():  # for all devices
        # if a discovered device's name and MAC address are pre-approved
        if address in eyeot_macs:  # TODO and name is arduino_name (get Arduino name)
            print("Authorized EyeoT device: {} at MAC address: {}".format(name, address))
            authorized_devices.append(address)
        else:
            print("Rejected Device: {} at MAC address: {}".format(name, address))
    return authorized_devices

if __name__ == '__main__':

    authorized_devices = search_for_authorized_eyeot_devices()  # get all EyeoT devices in range
    eyeot_devices = list()
    for address in authorized_devices:  # for each valid EyeoT device
        eyeot_devices.append(IoTDevice(address))  # initialize an IoTDevice object representing its state

    # TODO implement EYEOT functionality to determine which device to control, assume first device selected

    req = GATTRequester(eyeot_devices[0].address)  # connect to device
    # TODO read current state, check that it can be written to

    command = ble_commands_hex[red_light]
    req.write_by_handle(0x0b, command)  # handle 0x0b is required
    print("{0}\n".format(command))

#BLEMaster(host_MAC_address2)


