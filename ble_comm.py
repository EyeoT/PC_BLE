from bluetooth.ble import DiscoveryService, GATTRequester

import arduino  # constants related to the Arduino 101 boards
import ble_consts  # hex values of constant BLE commands
import pc  # constants related to the central Linux pc


class IoTDevice(object):

    """
    IoTDevice represents a single EyeoT IoT (Arduino 101) BLE device, initialized by one of several authorized MAC
    addresses.

    Input: MAC address of the EyeoT device to control

    Output: Initialized EyeoT device containing the proper MAC address, service UUID, tx_command and rx_response
    characteristic UUIDs, tx_handle, and GATTRequester
    """

    def __init__(self, address):
        self.address = address
        self.uuid = arduino.uuid
        self.tx_command = arduino.tx_command
        self.rx_response = arduino.rx_response
        self.tx_handle = arduino.tx_handle
        self.req = GATTRequester(address, False)  # initialize req but don't connect
        self.response = ble_consts.not_ready  # initialize to not ready

    def connect(self):
        print("Connecting...\n")
        self.req.connect(True)
        print("Connection Successful! \n")

    def send_command(self, command):
        self.req.write_by_handle(arduino.tx_handle, chr(command))
        print("Sent '{0}' command\n".format(ble_consts.commands[command]))

    def receive_response(self):
        self.response = int(self.req.read_by_uuid(arduino.rx_response)[0].encode('hex'), 16)
        print("Response '{0}' received!\n".format(ble_consts.commands[self.response]))


def search_for_authorized_eyeot_devices():

    """
    This function performs a BLE scan, finding all possible devices in range. It compares each device's name and MAC
    address against those already white listed. It returns a list of any authorized devices.

    Input: authorized_devices, a list containing the current MAC addresses of valid EyeoT devices in range

    Output: authorized_devices, a list containing the current MAC addresses of valid EyeoT devices in range
    """
    auth_devices = list()  # initialize empty
    service = DiscoveryService(pc.hci_num)  # use the USB BLE dongle at hci1, not the integrated Bluetooth card at hci0
    devices = service.discover(2)       # find all possible nearby BLE devices

    for address, name in devices.items():  # for all devices
        # if a discovered device's name and MAC address are pre-approved
        if address in arduino.mac_addresses:  # TODO: (filter also by Arduino name?)
            print("Authorized EyeoT device: {} at MAC address: {}".format(name, address))
            auth_devices.append(address)
        else:
            print("Rejected Device: {} at MAC address: {}".format(name, address))
    return auth_devices


if __name__ == '__main__':

    eyeot_devices = list()

    authorized_devices = search_for_authorized_eyeot_devices()  # get all EyeoT devices in range
    for address in authorized_devices:  # for each valid EyeoT device
        eyeot_devices.append(IoTDevice(address))  # initialize an IoTDevice object representing its state

    # TODO: implement Pupil functionality to determine which device to control, assume first device selected

    eyeot_devices[0].connect()  # connect to device

    while eyeot_devices[0].response() != ble_consts.ready:  # wait until device is ready
        eyeot_devices[0].receive_response()

    # TODO: implement Pupil functionality to determine which command to send
    eyeot_devices[0].send_command(ble_consts.red_light)  # example command

    # TODO: time the response time of receiving commands, insert timer to kill process if time is exceeded
    while eyeot_devices[0].response() != ble_consts.command_ack:  # wait for command to be Rx
        eyeot_devices[0].receive_response()

    # TODO: time the response time of executing commands, insert timer to kill process if time is exceeded
    # wait for command to be executed
    while eyeot_devices[0].response != (ble_consts.command_success or ble_consts.command_failure):
        eyeot_devices[0].receive_response()

        # if(eyeot_devices[0].response == ble_commands_and_responses.command_success):

        # else:
