# Code to send raw joystick data via XBee to the RPi3 to then control the thrusters
from digi.xbee.devices import XBeeDevice
REMOTE_NODE_ID = "REMOTE"
MESSAGE = "Hello from COORD"

# Must set both devices to API[1] Mode in XCTU
coord = XBeeDevice("COM4", 9600) # Open device on COM4 with 9600 Baud, Instantiate a local coordinator device object
coord.open() # Open the serial connection

xbee_network = coord.get_network()  # Get XBee network
remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
while True:
    try:
        if remote_device is None:
            print("Couldn't find coordinator!")
            coord.close()
            break
        print("Sending %s to %s at %s" % (MESSAGE, REMOTE_NODE_ID, remote_device.get_64bit_addr()))  # Shows user address of coord

        #coord.send_data(remote_device, MESSAGE)  # Sends the message to remote device
    except KeyboardInterrupt:
        coord.close()
        break