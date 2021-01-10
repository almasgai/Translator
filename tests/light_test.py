from time import sleep

from gpiozero import PWMLED
from signal import pause


led = PWMLED(14)
led.value = 0

while True:
    for i in range(0, 90, 1):
        led.value += 0.1
        print(led.value)
        sleep(0.01)

    sleep(2)

    for i in range(90, 0, -1):
        led.value -= 0.1
        print(led.value)
        sleep(0.01)

    sleep(2)
