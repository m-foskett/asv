#import RPi.GPIO as GPIO
import time
import math


# CONSTANTS
RADIUS = 100 # physical parameter of joystick
T1_DEADBAND_R = 1475 # microseconds
T1_DEADBAND_F = 1525 # microseconds
T1_MIN = 1100 # microseconds
T1_MAX = 1900 # microseconds
FREQUENCY = 50 # Hz
PWM_CHANNEL_1 = 38 # pin38 is GPIO, GND at pin ?
PWM_CHANNEL_2 = 18 # pin18 is GPIO, GND at pin 14

# SETUP
# GPIO.setmode(GPIO.BOARD) # sets the GPIO addressing as BOARD(Pin Numbers)
# GPIO.setup(PWM_CHANNEL_1, GPIO.OUT) # set pwm1 pin to output
# GPIO.setup(PWM_CHANNEL_2, GPIO.OUT) # set pwm2 pin to output
# thruster_pwm_1 = GPIO.PWM(PWM_CHANNEL_1, FREQUENCY) # 50 Hz Frequency outputting on pin13
# thruster_pwm_2 = GPIO.PWM(PWM_CHANNEL_2, FREQUENCY) # 50 Hz Frequency outputting on pin38
# thruster_pwm_1.start(0) # start the pwm1 with 0 dc
# thruster_pwm_2.start(0) # start the pwm2 with 0 dc
# thruster_pwm_1.ChangeDutyCycle(T1_DEADBAND*FREQUENCY/10000)
# time.sleep(2)
# thruster_pwm_2.ChangeDutyCycle(T1_DEADBAND*FREQUENCY/10000)
# time.sleep(2) # Initialisation - should hear two tones to indicate ESC is ready

# INSERT CODE TO EXTRACT DATA FROM XBEE PACKETS

# TESTING CODE: DATA STRAIGHT FROM JOYSTICK


# PARAMETERS RECEIVED VIA XBEE

# THRUST CALCULATION USING PYTHAGORAS
def getDutyCycle(direction_x, direction_y, heading):
    base_thrust = (math.sqrt(direction_x**2 + direction_y**2))/RADIUS * 100 # gives thrust as % of maximum thrust [0<=thrust<=100]
    if(direction_y < 0):
        base_thrust *= -1 # reverse
    #print("base_thrust = ", base_thrust, "%")
    #heading = ? number dependent on joystick mapping between [0%, 100%]
    left_thrust = base_thrust + heading    # + and - dependent on how coordinate system is defined
    if(left_thrust > 100):
        left_thrust = 100 # saturate to full speed (100%)
    elif(left_thrust < -100):
        left_thrust = -100 # saturate to full reverse speed (-100%)
    #print("left thrust = ", left_thrust, "%")
    right_thrust = base_thrust - heading   # + and - dependent on how coordinate system is defined
    if(right_thrust > 100):
        right_thrust = 100 # saturate to full speed (100%)
    elif(right_thrust < -100):
        right_thrust = -100 # saturate to full reverse speed(-100%)
    #print("right thrust = ", right_thrust, "%")

    # CONVERSION OF LEFT AND RIGHT THRUST PERCENTAGE TO DUTY CYCLE
    if(left_thrust > 0):
        high_left = (left_thrust * (T1_MAX - T1_DEADBAND_F))/100 + T1_DEADBAND_F
    elif(left_thrust < 0):
        high_left = (left_thrust * (T1_MAX - T1_DEADBAND_F)) / 100 + T1_DEADBAND_R
    duty_left = (high_left * FREQUENCY)/10000 # divided by 10^6 and * 100 gives /10000
    #print("duty_left = ", duty_left, "%")
    if(right_thrust > 0):
        high_right = (right_thrust * (T1_MAX - T1_DEADBAND_F))/100 + T1_DEADBAND_F
    elif(right_thrust < 0):
        high_right = (right_thrust * (T1_MAX - T1_DEADBAND_F)) / 100 + T1_DEADBAND_R
    duty_right = (high_right * FREQUENCY)/10000 # divided by 10^6 and * 100 gives /10000
    #print("duty_right = ", duty_right, "%")

    return duty_left, duty_right


# while True:
#     try:
#         thruster_pwm_1.ChangeDutyCycle(duty_left*FREQUENCY/10000)
#         thruster_pwm_2.ChangeDutyCycle(duty_right*FREQUENCY/10000)
#     except KeyboardInterrupt:
#         thruster_pwm_1.stop()
#         thruster_pwm_2.stop()
#         GPIO.cleanup()
#         break




