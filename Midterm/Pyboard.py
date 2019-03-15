import machine, network, ubinascii, ujson, urequests, utime
from pyb import DAC, Pin, UART
from array import array
import math
import gc,pyb,time
from machine import WDT

#digital in
p_a = Pin('X5', Pin.IN, Pin.PULL_UP)
p_b = Pin('X6', Pin.IN, Pin.PULL_UP)

## Wifi
WiFi = network.WLAN()

mac = ubinascii.hexlify(network.WLAN().config("mac"),":").decode()
print("MAC address: " + mac)

# Info
Tag = "Eric"
Type = "STRING"
Value = "0"
Key = "43yu2MDQCevken1DKXYEsyxgUaOoLQS12-nzB1bUSi"

urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"   
urlTag = urlBase + Tag
urlValue = urlBase + Tag + "/values/current"

headers = {"Accept":"application/json","x-ni-api-key":Key}
propName={"type":Type,"path":Tag}

# UART
uart = UART(3, 9600) #Use UART 3 in pybaord 
uart.init(9600, bits=8, parity=None, stop=1, timeout=50)


def put(num):
     propValue = {"value":{"type":Type,"value":str(num)}}
     urequests.put(urlValue,headers=headers,json=propValue).text


def connect():
     EN1 = machine.Pin("W23", machine.Pin.OUT, value=1)  # set power high for USB power (500mA now allowed)
     if not WiFi.isconnected():
          print ("Connecting ..")
          WiFi.active(True)
          WiFi.connect("Tufts_Wireless","")
          i=0
          while i < 25 and not WiFi.isconnected():
               utime.sleep_ms(200)
               i=i+1
          if WiFi.isconnected():
               print ("Connection succeeded")
          else:
               print ("Connection failed")     

def main():
     connect()
     print ("WiFi: ",WiFi.isconnected())

     counter = 0
     a_last = p_a.value()
     put_val = 1


     while True:
          val_a = p_a.value()
          val_b = p_b.value()
          if a_last != val_a:
               if val_a != val_b:
                    #print difference to check
                    counter += 1
               else:
                    counter -= 1
               uart.write(str(math.fabs(counter)))

          print(counter)
          a_last = val_a

          if math.fmod(put_val, 100) == 0:
               put(counter)

          put_val += 1
          gc.collect()
          time.sleep(.01)


if __name__ == '__main__':
     main()




