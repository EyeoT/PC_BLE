# coding=utf-8  # encoding declaration (needed)

# defined commands (constant) that the Arduino needs to receive
no_light = 0x00  # turn off all indicator lights
red_light = 01  # turn indicator lights red
green_light = 0x02  # turn indicator lights green
blue_light = 0x03  # turn indicator lights blue
servo_on = 0x04  # move light switch into on position
servo_off = 0x05  # move light switch into off position
not_ready = 0x06  # the Arduino is busy executing a previous command, don't send it new commands
ready = 0x07  # the Arduino has finished executing previous commands, send it new commands when ready
command_ack = 0x08  # response acknowledgement from IoT device
command_success = 0x09  # response from IoT device saying command executed successfully
command_failure = 0x10  # response from IoT device saying command failed to be properly executed

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

responses = {
    0x06: 'Arduino is not yet ready for a new command',
    0x07: 'Arduino ready for next command',
    0x08: 'Command acknowledged by IoT device',
    0x09: 'Command successfully carried out by IoT device',
    0x10: 'Command failed to be carried out by IoT device'
}
