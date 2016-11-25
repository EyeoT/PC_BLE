# coding=utf-8  # encoding declaration (needed)

# defined commands (constant) that the Arduino needs to receive
no_light = 0x00  # turn off all indicator lights
red_light = 01  # turn indicator lights red
green_light = 0x02  # turn indicator lights green
blue_light = 0x03  # turn indicator lights blue
servo_on = 0x04  # move light switch into on position
servo_off = 0x05  # move light switch into off position
command_ack = 0x97  # response acknowledgement from IoT device
command_success = 0x98  # response from IoT device saying command executed successfully
command_failure = 0x99  # response from IoT device saying command failed to be properly executed

# dict for printing verbose descriptions
commands = {
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
