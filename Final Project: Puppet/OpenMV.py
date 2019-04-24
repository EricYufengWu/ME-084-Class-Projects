# Face Detection Example
#
# Modified from OpenMV example, 'face_detection'

import sensor, time, image, gc, utime, pyb
from pyb import UART

#Setup UART
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout = 100)

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# FPS clock
clock = time.clock()

# Servo
left_ear = pyb.Servo(2)
right_ear = pyb.Servo(1)
arm = pyb.Servo(3)


# Servo functions
def move_ears():
     left_ear.angle(30)
     right_ear.angle(90)
     utime.sleep_ms(100)
     left_ear.angle(90)
     right_ear.angle(30)
def move_arms():
    arm.angle(-50)
    utime.sleep_ms(300)
    arm.angle(50)
    utime.sleep_ms(300)


while (True):
    clock.tick()
    flag = True

    # Capture snapshot
    img = sensor.snapshot()

    # Find objects.
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    # Draw objects
    for r in objects:
        flag = False
        img.draw_rectangle(r)
        coord = str(r[1]) + '|' + str(r[0]) + '|' + str(r[2]) + '\n'
        print(coord)
        uart.write(coord)

        if r[2] > 90:     # If the size of the detected face exceeds a threshold, move servos in the ears
            move_ears()

        gc.collect()
        utime.sleep(0.05)

    if(flag):             # If the camera finds no faces, move servo arms
        print('move arms')
        move_arms()



