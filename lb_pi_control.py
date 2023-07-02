#   pip install gpiozero
# from gpiozero import AngularServo

from time import sleep

# TESTER

# alter frequencies to servo manufacturers specs
minpw = 0.0006
maxpw = 0.0023

def pi_open_locker(locker):
    _lockerNum = locker.split()
    lockerNum = _lockerNum[1]
    # can alter lockerNum to match used GPIO pin
    print(lockerNum)

            # call      # GPIO      # start freq          # stop freq
    servo = AngularServo(lockerNum, min_pulse_width=minpw, max_pulse_width=maxpw)

    while (True):
        servo.angle = 90
        sleep(2)
        servo.angle = 0
        sleep(2)
        servo.angle = -90
        sleep(2)


pi_open_locker("locker 12")






# just PI can control 2 9gm servo
# Adafruit HAT for Raspberry Pi required to control 16 servos
# The Code is importing from a library called "gpiozero"


"""
# 9gram servo motor - viable for prototype of 2 servos 

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

while (True):
    servo.angle = 90
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = -90
    sleep(2)


# 15kg servo motor REQUIRES external PSU

servo = AngularServo(18, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

while (True):
    servo.angle = 0
    sleep(2)
    servo.angle = 135
    sleep(2)
    servo.angle = 260
    sleep(2)
"""