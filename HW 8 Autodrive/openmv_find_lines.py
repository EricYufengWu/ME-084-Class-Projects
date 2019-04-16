

enable_lens_corr = False # turn on for straighter lines...

import sensor, image, time, utime, gc
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# All line objects have a `theta()` method to get their rotation angle in degrees.
# You can filter lines based on their rotation angle.
value =90
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout = 50)

# filter out interfering lines
min_degree = 50
max_degree = 130

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    temp = 90  # stores the current value. to be used in the next loop.

    flag = True  # If the camera sees no lines, sends command to pyboard to drive straight

    for l in img.find_lines(threshold = 2000, theta_margin = 25, rho_margin = 25):
        flag = False
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (255, 0, 0))
            current = l[6]
            avg = (current + temp)/2   # Take the average of the current and previous angle
            print(avg)
            uart.write(str(avg))   # uart to pyboard
            temp = l[6]
            utime.sleep_ms(100)


    if(flag):
         uart.write('90')
         print('90')
         utime.sleep_ms(100)

    gc.collect()

