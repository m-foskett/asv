from digi.xbee.devices import XBeeDevice
COORD_NODE_ID = "COORD"
MESSAGE = "Hello from REMOTE"
# Must set both devices to API[1] Mode in XCTU
remote = XBeeDevice("COM3", 9600)  # Instantiate XBeeDevice object on RPi3
remote.open() # Open the serial port connection
#print(remote.get_parameter("AP"))
#remote.set_parameter("AP", bytearray("1", 'utf8'))
#print(remote.get_parameter("AP"))
print(remote.operating_mode)

while True:
    try:
        xbee_network = remote.get_network() # Get XBee network
        coord_device = xbee_network.discover_device(COORD_NODE_ID)
        if coord_device is None:
            print("Couldn't find coordinator!")
            remote.close()
            break
        print("Sending %s to %s at %s" % (MESSAGE, COORD_NODE_ID, coord_device.get_64bit_addr()))# Shows user address of coord
        remote.send_data(coord_device, MESSAGE) # Sends the message to coord device
    except KeyboardInterrupt:
        remote.close() # Close the device
        break