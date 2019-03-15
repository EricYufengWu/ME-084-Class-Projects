import board, busio, digitalio, time
import adafruit_dotstar as dotstar
 
uart = busio.UART(board.TX, board.RX, baudrate=9600, bits=8, parity=None, stop=1, timeout=50, receiver_buffer_size=64)
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))
i = 0

while True:
    data = uart.read(4)  # read line
    print(data)  # this is a bytearray type
    if data is not None:
    	led.value = True
    	time.sleep(0.05)
    	led.value = False
    	time.sleep(0.05)
    	dot[0] = wheel(i & 255)
    i = (i+10) % 256
