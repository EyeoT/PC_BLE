import pc  #constants related to the central Linux pc
import arduino  # constants related to the Arduino 101 boards
import ble_commands  # hex values of constant BLE commands
from bluetooth.ble import DiscoveryService, GATTRequester


class IoTDevice(object):

    """
    IoTDevice represents a single EyeoT IoT (Arduino 101) BLE device, initialized by one of several authorized MAC
    addresses.

    Input: MAC address of the EyeoT device to control
    """

    def __init__(self, address):
        self.address = address
        self.uuid = arduino.uuid
        self.characteristic = arduino.characteristic
        self.handle = arduino.handle
        self.req = GATTRequester(address, False)  # initialize req but don't connect

    def connect(self):
        print("Connecting...\n")
        self.req.connect(True)
        print("Connection Successful! \n")

    def send(self, command):
        self.req.write_by_handle(arduino.handle, chr(command))
        print("Sent '{0}' command\n".format(ble_commands.commands[command]))

    def receive(self):
        response = int(self.req.read_by_handle(arduino.handle)[0].encode('hex'), 16)
        print("Response '{0}' received!\n".format(ble_commands.commands[response]))


def search_for_authorized_eyeot_devices():

    """
    This function performs a BLE scan, finding all possible devices in range. It compares each device's name and MAC
    address against those already white listed. It returns a list of any authorized devices.

    Input: None

    Output: authorized_devices, a list of authorized MAC addresses to connect to
    """

    authorized_devices = list()
    service = DiscoveryService(pc.hci_num)  # use the USB BLE dongle at hci1, not the integrated Bluetooth card at hci0
    devices = service.discover(2)       # find all possible nearby BLE devices

    for address, name in devices.items():  # for all devices
        # if a discovered device's name and MAC address are pre-approved
        if address in arduino.mac_addresses:  # TODO and name is arduino_name (get Arduino name)
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

    eyeot_devices[0].connect()  # connect to device

    # TODO read current state, check that it can be written to
    eyeot_devices[0].receive()  # read current state
    eyeot_devices[0].send(ble_commands.red_light)
    eyeot_devices[0].receive()  # read current state



