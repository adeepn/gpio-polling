#!/usr/bin/python

import gpiod
import sys
import time
import os

DEBUG = False


def onchange(cmd, value):
    if DEBUG:
        print(f'Get new value: {value}')
    os.system(cmd + f' {value}')


if __name__ == '__main__':
    if len(sys.argv) > 3:
        GPIO_CHIP = sys.argv[1]
        GPIO_LINE = int(sys.argv[2])
        GPIO_CMD = sys.argv[3]
    else:
        print(f'''Usage:
        python3 {sys.argv[0]} <chip> <line offset> <cmd to exec on input change>
        gpio line must be unexported from sysfs before use''')
        sys.exit()
    chip = gpiod.chip(GPIO_CHIP)
    GPIOline = chip.get_line(GPIO_LINE)
    config = gpiod.line_request()
    config.consumer = f"Get value from gpiochip{GPIO_CHIP} line {GPIO_LINE}"
    config.request_type = gpiod.line_request.DIRECTION_INPUT

    GPIOline.request(config)

    print(GPIOline.consumer)

    val = -1
    while True:
        nval = GPIOline.get_value()
        if nval != val:
            onchange(GPIO_CMD, nval)
            val = nval
        time.sleep(0.05)
