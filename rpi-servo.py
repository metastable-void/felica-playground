import RPi.GPIO as GPIO
import time
import signal

servopin = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50)
p.start(0)
time.sleep(2)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servopin, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servopin, False)
    p.ChangeDutyCycle(0)

while True:
    degree = input ('input a degree: ')
    
    if degree == 'stop':
        break
    else:
        degree = int(degree)
        SetAngle(degree)

GPIO.cleanup()

