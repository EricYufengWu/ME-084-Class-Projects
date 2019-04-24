from pyb import UART, LED
import utime, gc
# init UART
uart = UART(3, 9600) #Use UART 3 in pybaord 
uart.init(9600, bits=8, parity=None, stop=1, timeout=100)
#init servo
servo_x = pyb.Servo(4)
servo_y = pyb.Servo(3)
#variables
temp_x = [40] * 3
temp_y = [70] * 3
ear_val = 60
speed = 100


while(True):
     val = uart.readline()
     if val != None:
          val = val.decode('utf-8')    # reads in and decode uart data from bytes to floats.
          val = val[:-1]
          val = val.split('|')
          print(val)
          if len(val) != 3 or val[0] == '' or val[1]=='' or val[2]=='':
               continue
          temp_x.append(80 - int(val[0]))   # x mounts in the head - up-and-down movement
          servo_x.angle(sum(temp_x)/len(temp_x))
          temp_x.pop(0)
      
          temp_y.append(110 - int(val[1]))   # y is horizontal sweeping
          servo_y.angle(sum(temp_y)/len(temp_y))
          temp_y.pop(0)

          speed = int(val[2])


     gc.collect()
     utime.sleep(0.05)