from gpiozero import PWMLED

led = PWMLED(14)
print(dir(led))

step = 0.1
while led.value <= 1 - step:
    print(led.value)
    led.value = round(led.value + step, 3)

while led.value - step >= 0:
    print(led.value)
    led.value = round(led.value - step, 3)
