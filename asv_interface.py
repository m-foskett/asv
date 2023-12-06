from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from prototype import CtlSlider, CtlKnob, CtlCheckbox
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from asv_openloop import getDutyCycle
#import RPi.GPIO as GPIO
import time
import math
import pygame

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

class ASVWidget(BoxLayout):
    Window.clearcolor = (0.25, 0.25, 0.25, 1)

    DeviceID_MotorA = 0x01
    DeviceID_MotorB = 0x02
    joystick = None

    def connectJoystick(self):
        pygame.display.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.joystick = pygame.joystick.Joystick(0)  # check device number
        self.joystick.init()
        print(self.joystick)
        print (self.joystick.get_init())
        print (self.joystick.get_id())
        print (self.joystick.get_name())
        print (self.joystick.get_numaxes())
        print (self.joystick.get_numballs())
        print (self.joystick.get_numbuttons())
        print (self.joystick.get_numhats())
        print (self.joystick.get_axis(0))

    def updateThruster(self, dt):
        pygame.event.pump()

        for event in pygame.event.get():

            print("X = ", float('%.3f'%(self.joystick.get_axis(0))))
            print("Y = ", float('%.3f'%(-1*self.joystick.get_axis(1))))
            print("Z = ", float('%.3f'%(self.joystick.get_axis(3))))
            x = self.joystick.get_axis(0) * 100 # increase from range of (-1,1) to (-100,100)
            y = self.joystick.get_axis(1) * -100 # increase from range of (-1,1) to (-100,100)
            #code from asv_send to transfer the data from the joystick to pi via xbee
            
            
            ########################################################################################
            heading = self.joystick.get_axis(3) * 100 # increase from range of (-1,1) to (-100,100)
            #heading = 0
            duty_left, duty_right = getDutyCycle(x, y, heading)
            print("Left_Duty = ", float('%.3f'%duty_left), "% Right Duty = ", float('%.3f'%duty_right), "%")
            #thruster_pwm_1.ChangeDutyCycle(duty_left*FREQUENCY/10000)
            #thruster_pwm_2.ChangeDutyCycle(duty_right*FREQUENCY/10000)

class ASVInterfaceApp(App):
    def build(self):
        ASV = ASVWidget()
        ASV.connectJoystick()
        Clock.schedule_interval(ASV.updateThruster, 0.04)

        return ASV

ASVInterfaceApp().run()
#thruster_pwm_1.stop()
#thruster_pwm_2.stop()
#GPIO.cleanup()