from pyb import Pin, Timer
import utime
import gc
from pyb import UART

# init UART
uart = UART(3, 9600) 
uart.init(9600, bits=8, parity=None, stop=1, timeout=50)

# init motors
A_PWM = Pin('W29') # W29 has TIM2, CH2
AIn2 = Pin('Y7',Pin.OUT)
AIn1 = Pin('Y8',Pin.OUT)
Stdby = Pin('W24',Pin.OUT)

BIn1 = Pin('X3', Pin.OUT)
BIn2 = Pin('X2',Pin.OUT)
B_PWM = Pin('X1') #  TIM8, CH2

timA = Timer(2, freq=1000)
timB = Timer(5, freq=1000)
chA = timA.channel(2, Timer.PWM, pin= A_PWM)
chB = timB.channel(1, Timer.PWM, pin= B_PWM)

BASE_SPEED = 20

FACTOR = 1  # proportional control scaling factor

SpeedA = BASE_SPEED + 1
SpeedB = BASE_SPEED

Stdby.value(255)  # stdy on to power on motors

# uses proportional control to adjust motor speed
def adjustMotors(angle_avg):
     diff = angle_avg - 90
     if diff < 0:
          SpeedB = BASE_SPEED + abs(diff) * FACTOR
          SpeedA = BASE_SPEED + 1
     else:
          SpeedB = BASE_SPEED
          SpeedA = BASE_SPEED + abs(diff) * FACTOR*1.5 + 1
     # Setting pulse widths
     print(SpeedA, SpeedB, sep=' ')
     chA.pulse_width_percent(SpeedA)
     chB.pulse_width_percent(SpeedB)
     # Sending out the voltages
     AIn1.value(0)
     AIn2.value(255)
     BIn1.value(0)
     BIn2.value(255)

while True:
     val = uart.read()
     if val != None:
          val = val.decode('utf-8')   # convert bytes from uart to strings 
          val = float(val)
          #print(val)
          adjustMotors(val)

     gc.collect()
     utime.sleep_ms(50)

     