# Russell Corbett 2020
# OD - 4D
# Any questions, email me at russellcorbett11@gmail.com


from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.LCD import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.RCServo import *

import cv2
import numpy as np

import time
from datetime import date
import traceback

import threading
import asyncio

import evdev
from evdev import InputDevice, categorize, ecodes

global timer
global runtime
global end
global lcd6


class Handlers:
    #   Create Attach, Detach, Change, and Error handlers

    # Screen Handlers
    def on_large_screen_attach(self):
        self.setScreenSize(LCDScreenSize.SCREEN_SIZE_4x40)
        self.setBacklight(1)

    def on_mini_screen_attach(self):
        self.setScreenSize(LCDScreenSize.SCREEN_SIZE_4x20)
        self.setBacklight(1)

    def on_screen_detach(self):
        print("A screen has detached, check it out")

    def on_error(self, code, description):
        print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
        print("Description [" + str(self.getChannel()) + "]: " + str(description))
        print("----------")

    #   Sensor Handlers
    def on_topside_voltage_change(self, voltage):
        global lcd2
        lcd2.writeText(LCDFont.FONT_5x8, 28, 0, (str(voltage)))
        lcd2.flush()

    def on_robot_voltage_change(self, voltage):
        global lcd2
        lcd2.writeText(LCDFont.FONT_5x8, 9, 0, (str(voltage)))
        lcd2.flush()

    def on_topside_current_change(self, voltageRatio):
        global lcd2
        lcd2.writeText(LCDFont.FONT_5x8, 28, 1, (str(voltageRatio)))
        lcd2.flush()

    def on_robot_current_change(self, voltageRatio):
        global lcd2
        lcd2.writeText(LCDFont.FONT_5x8, 9, 1, (str(voltageRatio)))
        lcd2.flush()

    def on_temperature_sensor_change(self, sensor_value, sensor_unit):
        global lcd2
        if "0" in str(self.getChannel()):
            lcd2.writeText(LCDFont.FONT_5x8, 13, 2, (str(round(sensor_value, 1))) + str(sensor_unit.symbol))
            lcd2.flush()
        elif "1" in str(self.getChannel()):
            lcd2.writeText(LCDFont.FONT_5x8, 10, 3, (str(round(sensor_value, 1))) + str(sensor_unit.symbol))
            lcd2.flush()

    # Motor Handlers
    def on_attach_thruster(self):
        print("Attach Thruster # [" + str(self.getChannel()) + "]!")

    def on_detach_thruster(self):
        print("Detach Thruster # [" + str(self.getChannel()) + "]!")

    def __init__(self):
        pass


class TopsideComputer:
    #   Topside Controls
    def __init__(self):
        pass

    #   Screen Setup
    @staticmethod
    def connect():
        global lcd0
        global lcd2
        global lcd4
        global lcd6
        # Create your Phidget LCD channels
        lcd0 = LCD()
        lcd1 = LCD()
        lcd2 = LCD()
        lcd3 = LCD()
        lcd4 = LCD()
        lcd5 = LCD()
        lcd6 = LCD()
        TopVoltage = VoltageInput()
        TopCurrent = VoltageRatioInput()

        lcd0.setDeviceSerialNumber(329759)
        lcd0.setChannel(0)
        lcd1.setDeviceSerialNumber(329759)
        lcd1.setChannel(1)

        lcd2.setDeviceSerialNumber(329683)
        lcd2.setChannel(0)
        lcd3.setDeviceSerialNumber(329683)
        lcd3.setChannel(1)

        lcd4.setDeviceSerialNumber(329778)
        lcd4.setChannel(0)
        lcd5.setDeviceSerialNumber(329778)
        lcd5.setChannel(1)

        lcd6.setDeviceSerialNumber(330051)
        lcd6.setChannel(0)

        TopVoltage.setDeviceSerialNumber(433284)
        TopVoltage.setChannel(6)
        TopCurrent.setDeviceSerialNumber(433284)
        TopCurrent.setChannel(7)

        lcd0.setOnAttachHandler(Handlers.on_large_screen_attach)
        lcd0.setOnDetachHandler(Handlers.on_screen_detach)
        lcd0.setOnErrorHandler(Handlers.on_error)
        lcd2.setOnAttachHandler(Handlers.on_large_screen_attach)
        lcd2.setOnDetachHandler(Handlers.on_screen_detach)
        lcd2.setOnErrorHandler(Handlers.on_error)
        lcd4.setOnAttachHandler(Handlers.on_large_screen_attach)
        lcd4.setOnDetachHandler(Handlers.on_screen_detach)
        lcd4.setOnErrorHandler(Handlers.on_error)
        lcd6.setOnAttachHandler(Handlers.on_mini_screen_attach)
        lcd6.setOnDetachHandler(Handlers.on_screen_detach)
        lcd6.setOnErrorHandler(Handlers.on_error)

        TopVoltage.setOnErrorHandler(Handlers.on_error)
        TopCurrent.setOnErrorHandler(Handlers.on_error)

        lcd0.openWaitForAttachment(5000)
        lcd1.openWaitForAttachment(5000)
        lcd2.openWaitForAttachment(5000)
        lcd3.openWaitForAttachment(5000)
        lcd4.openWaitForAttachment(5000)
        lcd5.openWaitForAttachment(5000)
        lcd6.openWaitForAttachment(5000)

        TopVoltage.openWaitForAttachment(5000)
        TopCurrent.openWaitForAttachment(5000)

        # Connections Screen / Top Screen
        lcd0.writeText(LCDFont.FONT_5x8, 0, 0, "Joystick: ")
        lcd0.writeText(LCDFont.FONT_5x8, 0, 2, "Main ROV: ")
        lcd0.flush()

        # Sensors Screen / Middle Screen

        # Robot
        lcd2.writeText(LCDFont.FONT_5x8, 0, 0, "Voltage: N/A")
        lcd2.writeText(LCDFont.FONT_5x8, 0, 1, "Current: N/A")
        lcd2.writeText(LCDFont.FONT_5x8, 0, 2, "Temperature: N/A")
        lcd2.writeText(LCDFont.FONT_5x8, 0, 3, "Humidity: N/A")
        lcd2.writeText(LCDFont.FONT_5x8, 19, 3, "Depth: N/A")

        # Topside Controller
        lcd2.writeText(LCDFont.FONT_5x8, 19, 0, "Voltage: 0")
        lcd2.writeText(LCDFont.FONT_5x8, 19, 1, "Current: 0")
        lcd2.flush()

        # Action Screen / Bottom Screen
        lcd4.writeText(LCDFont.FONT_5x8, 0, 0, "Mode: Not Set")
        lcd4.writeText(LCDFont.FONT_5x8, 0, 1, "Angle: Not Set")
        lcd4.writeText(LCDFont.FONT_5x8, 20, 0, "Surge:  0")
        lcd4.writeText(LCDFont.FONT_5x8, 20, 1, "Sway:   0")
        lcd4.writeText(LCDFont.FONT_5x8, 20, 2, "Heave:  0")
        lcd4.writeText(LCDFont.FONT_5x8, 20, 3, "Yaw:    0")
        lcd4.flush()

        # Basic Information + Timer / Mini Screen
        today = str(date.today())
        lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Timer not set")
        lcd6.writeText(LCDFont.FONT_5x8, 0, 1, "00:00")
        lcd6.writeText(LCDFont.FONT_5x8, 0, 3, today)
        lcd6.writeText(LCDFont.FONT_5x8, 15, 3, "OD-4D")
        lcd6.flush()

        TopVoltage.setOnVoltageChangeHandler(Handlers.on_topside_voltage_change)
        TopCurrent.setOnVoltageRatioChangeHandler(Handlers.on_topside_current_change)

    @staticmethod
    def screen_detach():
        lcd0.close()
        lcd1.close()
        time.sleep(0.5)
        lcd2.close()
        lcd3.close()
        time.sleep(0.5)
        lcd4.close()
        lcd5.close()
        time.sleep(0.5)
        lcd6.close()
        time.sleep(0.5)

    @staticmethod
    def robot_sensors_connect():
        try:
            BotTemperature = VoltageRatioInput()
            BotHumidity = VoltageRatioInput()
            BotVoltage = VoltageInput()
            BotCurrent = VoltageRatioInput()

            BotTemperature.setDeviceSerialNumber(394113)
            BotTemperature.setChannel(0)
            BotHumidity.setDeviceSerialNumber(394113)
            BotHumidity.setChannel(1)
            BotVoltage.setDeviceSerialNumber(394113)
            BotVoltage.setChannel(2)
            BotCurrent.setDeviceSerialNumber(394113)
            BotCurrent.setChannel(3)

            BotTemperature.setOnSensorChangeHandler(Handlers.on_temperature_sensor_change)
            BotTemperature.setOnErrorHandler(Handlers.on_error)
            BotHumidity.setOnSensorChangeHandler(Handlers.on_temperature_sensor_change)
            BotHumidity.setOnErrorHandler(Handlers.on_error)

            BotVoltage.setOnVoltageChangeHandler(Handlers.on_robot_voltage_change)
            BotVoltage.setOnErrorHandler(Handlers.on_error)
            BotCurrent.setOnVoltageRatioChangeHandler(Handlers.on_robot_current_change)
            BotCurrent.setOnErrorHandler(Handlers.on_error)

            BotTemperature.openWaitForAttachment(5000)
            BotHumidity.openWaitForAttachment(5000)
            BotVoltage.openWaitForAttachment(5000)
            BotCurrent.openWaitForAttachment(5000)

            BotTemperature.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_TEMPERATURE)
            BotHumidity.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1125_HUMIDITY)

        except PhidgetException as ex:
            traceback.print_exc()
            print("")
            print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

    @staticmethod
    def topside_sensors_detach():
        TopVoltage.close()
        TopCurrent.close()

    @staticmethod
    def robot_sensors_detach():
        BotTemperature.close()
        BotHumidity.close()
        BotVoltage.close()
        BotCurrent.close()

    #   Lights
    @staticmethod
    def lights_connect():
        Lights = RCServo()
        Lights.setDeviceSerialNumber(493392)
        Lights.setChannel(6)
        Lights.openWaitForAttachment(5000)
        Lights.setMinPulseWidth(1100)
        Lights.setMaxPulseWidth(1900)
        Lights.setMinPosition(1100)
        Lights.setMaxPosition(1900)

    @staticmethod
    def lights_disconnect():
        Lights.setTargetPosition(1100)
        Lights.setEngaged(True)
        Lights.close()

    #   Thruster
    @staticmethod
    def thruster_connect():
        try:
            rcServo0 = RCServo()
            rcServo1 = RCServo()
            rcServo2 = RCServo()
            rcServo3 = RCServo()
            rcServo4 = RCServo()
            rcServo5 = RCServo()

            rcServo0.setDeviceSerialNumber(493392)
            rcServo0.setChannel(0)
            rcServo1.setDeviceSerialNumber(493392)
            rcServo1.setChannel(1)
            rcServo2.setDeviceSerialNumber(493392)
            rcServo2.setChannel(2)
            rcServo3.setDeviceSerialNumber(493392)
            rcServo3.setChannel(3)
            rcServo4.setDeviceSerialNumber(493392)
            rcServo4.setChannel(4)
            rcServo5.setDeviceSerialNumber(493392)
            rcServo5.setChannel(5)

            rcServo0.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo0.setOnDetachHandler(Handlers.on_detach_thruster)
            rcServo1.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo1.setOnDetachHandler(Handlers.on_detach_thruster)
            rcServo2.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo2.setOnDetachHandler(Handlers.on_detach_thruster)
            rcServo3.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo3.setOnDetachHandler(Handlers.on_detach_thruster)
            rcServo4.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo4.setOnDetachHandler(Handlers.on_detach_thruster)
            rcServo5.setOnAttachHandler(Handlers.on_attach_thruster)
            rcServo5.setOnDetachHandler(Handlers.on_detach_thruster)

            rcServo0.openWaitForAttachment(5000)
            rcServo1.openWaitForAttachment(5000)
            rcServo2.openWaitForAttachment(5000)
            rcServo3.openWaitForAttachment(5000)
            rcServo4.openWaitForAttachment(5000)
            rcServo5.openWaitForAttachment(5000)

            rcServo0.setMinPulseWidth(1100)
            rcServo1.setMinPulseWidth(1100)
            rcServo2.setMinPulseWidth(1100)
            rcServo3.setMinPulseWidth(1100)
            rcServo4.setMinPulseWidth(1100)
            rcServo5.setMinPulseWidth(1100)

            rcServo0.setMaxPulseWidth(1900)
            rcServo1.setMaxPulseWidth(1900)
            rcServo2.setMaxPulseWidth(1900)
            rcServo3.setMaxPulseWidth(1900)
            rcServo4.setMaxPulseWidth(1900)
            rcServo5.setMaxPulseWidth(1900)

            rcServo0.setMinPosition(1100)
            rcServo1.setMinPosition(1100)
            rcServo2.setMinPosition(1100)
            rcServo3.setMinPosition(1100)
            rcServo4.setMinPosition(1100)
            rcServo5.setMinPosition(1100)

            rcServo0.setMaxPosition(1900)
            rcServo1.setMaxPosition(1900)
            rcServo2.setMaxPosition(1900)
            rcServo3.setMaxPosition(1900)
            rcServo4.setMaxPosition(1900)
            rcServo5.setMaxPosition(1900)

            lcd0.writeText(LCDFont.FONT_5x8, 0, 3, "Connected")
            lcd0.writeText(LCDFont.FONT_5x8, 10, 3, "6 Thrusters")
            lcd0.flush()

            rcServo0.setTargetPosition(1500)
            rcServo1.setTargetPosition(1500)
            rcServo2.setTargetPosition(1500)
            rcServo3.setTargetPosition(1500)
            rcServo4.setTargetPosition(1500)
            rcServo5.setTargetPosition(1500)
            rcServo0.setEngaged(True)
            rcServo1.setEngaged(True)
            rcServo2.setEngaged(True)
            rcServo3.setEngaged(True)
            rcServo4.setEngaged(True)
            rcServo5.setEngaged(True)

            time.sleep(1)
            rcServo0.setTargetPosition(1600)
            rcServo0.setEngaged(True)
            time.sleep(0.5)
            rcServo0.setTargetPosition(1500)
            rcServo0.setEngaged(True)
            time.sleep(0.25)

            rcServo1.setTargetPosition(1600)
            rcServo1.setEngaged(True)
            time.sleep(0.5)
            rcServo1.setTargetPosition(1500)
            rcServo1.setEngaged(True)
            time.sleep(0.25)

            rcServo2.setTargetPosition(1600)
            rcServo2.setEngaged(True)
            time.sleep(0.5)
            rcServo2.setTargetPosition(1500)
            rcServo2.setEngaged(True)
            time.sleep(0.25)

            rcServo3.setTargetPosition(1600)
            rcServo3.setEngaged(True)
            time.sleep(0.5)
            rcServo3.setTargetPosition(1500)
            rcServo3.setEngaged(True)
            time.sleep(0.25)

            rcServo4.setTargetPosition(1600)
            rcServo4.setEngaged(True)
            time.sleep(0.5)
            rcServo4.setTargetPosition(1500)
            rcServo4.setEngaged(True)
            time.sleep(0.25)

            rcServo5.setTargetPosition(1600)
            rcServo5.setEngaged(True)
            time.sleep(0.5)
            rcServo5.setTargetPosition(1500)
            rcServo5.setEngaged(True)
            time.sleep(0.25)

        except Exception:
            lcd0.writeText(LCDFont.FONT_5x8, 0, 3, "Not Connected         ")
            lcd0.flush()

    @staticmethod
    def thruster_disconnect():
        rcServo0.close()
        rcServo1.close()
        rcServo2.close()
        rcServo3.close()
        rcServo4.close()
        rcServo5.close()


def controller():
    #   Find what or if a Joystick is connected
    print("Started looking for controller...\n")
    while not end:
        acceptable_controllers = ["Playstation", "Dual Action"]
        arcade = InputDevice('/dev/input/event0')

        input_list = []
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            str_device_path = str(device.path)
            k = str_device_path[16]
            k = int(k)
            input_list.append(k)
        str_arcade = str(arcade)
        for i in input_list:
            if any(cont in str_arcade for cont in acceptable_controllers):
                break
            else:
                arcade = InputDevice('/dev/input/event%i' % i)
                str_arcade = str(arcade)

        if "Playstation" in str_arcade:
            lcd0.writeText(LCDFont.FONT_5x8, 10, 0, "Connected    ")
            lcd0.writeText(LCDFont.FONT_5x8, 0, 1, "Playstation Joystick")
            lcd0.flush()
            print("AV8R Controller Found!")
            Controllers.playstation_joystick_controller()

        elif "Dual Action" in str_arcade:
            lcd0.writeText(LCDFont.FONT_5x8, 10, 0, "Connected    ")
            lcd0.writeText(LCDFont.FONT_5x8, 0, 1, "Logitech Controller")
            lcd0.flush()
            print("Console Controller Found!")
            Controllers.logitech_controller()

        else:
            lcd0.writeText(LCDFont.FONT_5x8, 10, 0, "Not Connected")
            lcd0.writeText(LCDFont.FONT_5x8, 0, 1, "                      ")
            lcd0.flush()
            print("No controller found")
            print("")
            print("Looking for controller...")
            time.sleep(5)


class Controllers:

    def __init__(self):
        pass

    @staticmethod
    def playstation_joystick_controller():
        #   Playstation Joystick Controller
        x = 0
        y = 0
        z = 0
        twist = 0
        direction_mode = 2
        speed_mode = 2
        light_level = 4
        global timer
        global runtime

        STICK_MAX = 255
        CENTER_TOLERANCE = 1
        CENTER_HAT = 0
        HAT_MAX = 0

        axis = {
            ecodes.ABS_X: 'JoystickX',
            ecodes.ABS_Y: 'JoystickY',
            ecodes.ABS_Z: 'Vertical',
            ecodes.ABS_RZ: 'JoystickSpin',

            ecodes.ABS_HAT0X: 'CameraX',
            ecodes.ABS_HAT0Y: 'CameraY'
        }

        center = {
            'JoystickX': STICK_MAX / 2,
            'JoystickY': STICK_MAX / 2,
            'Vertical': STICK_MAX / 2,
            'JoystickSpin': STICK_MAX / 2,
            'CameraX': HAT_MAX / 2,
            'CameraY': HAT_MAX / 2
        }

        last = {
            'JoystickX': STICK_MAX / 2,
            'JoystickY': STICK_MAX / 2,
            'Vertical': STICK_MAX / 2,
            'JoystickSpin': STICK_MAX / 2,
            'CameraX': HAT_MAX / 2,
            'CameraY': HAT_MAX / 2
        }

        # Assign buttons to code
        L3 = 296
        R3 = 297
        Select = 298
        Start = 299

        Triangle = 289
        Cross = 290
        Square = 291
        Trigger = 288

        try:
            for event in arcade.read_loop():
                if event.type == ecodes.EV_KEY:
                    if event.value == 1:
                        if event.code == R3:
                            if direction_mode == 1:
                                lcd4.writeText(LCDFont.FONT_5x8, 7, 1, "On        ")
                                lcd4.flush()
                                direction_mode = 2
                            elif direction_mode == 2:
                                lcd4.writeText(LCDFont.FONT_5x8, 7, 1, "Off        ")
                                lcd4.flush()
                                direction_mode = 1
                        elif event.code == L3:
                            if speed_mode == 1:
                                lcd4.writeText(LCDFont.FONT_5x8, 6, 0, "Speed     ")
                                lcd4.flush()
                                speed_mode = 2
                            elif speed_mode == 2:
                                lcd4.writeText(LCDFont.FONT_5x8, 6, 0, "Precision")
                                lcd4.flush()
                                speed_mode = 1

                        elif event.code == Select:
                            global runtime
                            if not timer:
                                lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Timer set to")
                                lcd6.writeText(LCDFont.FONT_5x8, 0, 1, "15:00")
                                runtime = 900
                                lcd6.flush()

                        elif event.code == Start:
                            if not timer:
                                timer = True
                            elif timer:
                                timer = False

                        elif event.code == Triangle:
                            print("Triangle")
                        elif event.code == Cross:
                            print("Cross")
                        elif event.code == Square:
                            print("Square")
                        elif event.code == Trigger:
                            if light_level == 0:
                                Lights.setTargetPosition(1100)
                                Lights.setEngaged(True)
                                light_level = 1
                            elif light_level == 1:
                                Lights.setTargetPosition(1300)
                                Lights.setEngaged(True)
                                light_level = 2
                            elif light_level == 2:
                                Lights.setTargetPosition(1500)
                                Lights.setEngaged(True)
                                light_level = 3
                            elif light_level == 3:
                                Lights.setTargetPosition(1700)
                                Lights.setEngaged(True)
                                light_level = 4
                            elif light_level == 4:
                                Lights.setTargetPosition(1900)
                                Lights.setEngaged(True)
                                light_level = 0

                #   Read stick axis movement
                elif event.type == ecodes.EV_ABS:
                    if axis[event.code] in ['JoystickX', 'JoystickY', 'Vertical', 'JoystickSpin']:
                        last[axis[event.code]] = event.value

                        value = event.value - center[axis[event.code]]

                        value_y = ((value * -1) + 0.5)
                        value_x = (value - 0.5)

                        if abs(value) <= CENTER_TOLERANCE:
                            value = 0

                        if axis[event.code] == 'JoystickX':
                            x = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 0, ((str(value_x)) + "      "))
                            lcd4.flush()

                        elif axis[event.code] == 'JoystickY':
                            y = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 1, ((str(value_y)) + "      "))
                            lcd4.flush()

                        elif axis[event.code] == 'Vertical':
                            z = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 2, ((str(value_y)) + "      "))
                            lcd4.flush()

                        elif axis[event.code] == 'JoystickSpin':
                            twist = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 3, ((str(value)) + "      "))
                            lcd4.flush()

                    elif axis[event.code] in ['CameraX', 'CameraY']:
                        last[axis[event.code]] = event.value

                        value = event.value - center[axis[event.code]]

                        if abs(value) <= CENTER_HAT:
                            value = 0
                        if axis[event.code] == 'CameraX':
                            if value == 0:
                                print('center_cam')
                            elif value < 0:
                                print('left_cam')
                            else:
                                print('right_cam')
                            print(value)

                        elif axis[event.code] == 'CameraY':
                            if value == 0:
                                print('center_cam')
                            elif value < 0:
                                print('up_cam')
                            else:
                                print('down_cam')
                            print(value)
                rov_movement(direction_mode, speed_mode, x, y, z, twist)
        except Exception:
            print("Controller Disconnected")

    @staticmethod
    def logitech_controller():
        #   Logitech Controller
        x = 0
        y = 0
        z = 0
        twist = 0
        direction_mode = 2
        speed_mode = 2
        global timer
        global runtime

        STICK_MAX = 255
        CENTER_TOLERANCE = 1
        CENTER_HAT = 0
        HAT_MAX = 0

        axis = {
            ecodes.ABS_X: 'LeftJoystickX',
            ecodes.ABS_Y: 'LeftJoystickY',
            ecodes.ABS_Z: 'RightJoystickX',
            ecodes.ABS_RZ: 'RightJoystickY',

            ecodes.ABS_HAT0X: 'CameraX',
            ecodes.ABS_HAT0Y: 'CameraY'
        }

        center = {
            'LeftJoystickX': STICK_MAX / 2,
            'LeftJoystickY': STICK_MAX / 2,
            'RightJoystickX': STICK_MAX / 2,
            'RightJoystickY': STICK_MAX / 2,
            'CameraX': HAT_MAX / 2,
            'CameraY': HAT_MAX / 2
        }

        last = {
            'LeftJoystickX': STICK_MAX / 2,
            'LeftJoystickY': STICK_MAX / 2,
            'RightJoystickX': STICK_MAX / 2,
            'RightJoystickY': STICK_MAX / 2,
            'CameraX': HAT_MAX / 2,
            'CameraY': HAT_MAX / 2
        }

        One = 288
        Two = 289
        Three = 290
        Four = 291

        LeftTrigger = 294
        LeftButton = 292
        RightTrigger = 295
        RightButton = 293

        Nine = 296
        Ten = 297

        LeftStickPress = 298
        RightStickPress = 299

        try:
            for event in arcade.read_loop():
                if not operation:
                    break
                if event.type == ecodes.EV_KEY:
                    if event.value == 1:
                        if event.code == One:
                            print("One")
                        if event.code == Two:
                            print("Two")
                        if event.code == Three:
                            print("Three")
                        if event.code == Four:
                            print("Four")
                        if event.code == LeftTrigger:
                            print("LeftTrigger")
                        if event.code == LeftButton:
                            print("LeftButton")
                        if event.code == RightTrigger:
                            print("RightTrigger")
                        if event.code == RightButton:
                            print("RightButton")
                        if event.code == Nine:
                            if timer:
                                lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Timer set to")
                                lcd6.writeText(LCDFont.FONT_5x8, 0, 1, "15:00")
                                lcd6.flush()
                                runtime = 900
                        if event.code == Ten:
                            if timer:
                                timer = False
                            elif not timer:
                                timer = True
                        if event.code == LeftStickPress:
                            if speed_mode == 1:
                                lcd4.writeText(LCDFont.FONT_5x8, 6, 0, "Speed     ")
                                lcd4.flush()
                                speed_mode = 2
                            elif speed_mode == 2:
                                lcd4.writeText(LCDFont.FONT_5x8, 6, 0, "Precision")
                                lcd4.flush()
                                speed_mode = 1
                        if event.code == RightStickPress:
                            if direction_mode == 1:
                                lcd4.writeText(LCDFont.FONT_5x8, 7, 1, "On       ")
                                lcd4.flush()
                                direction_mode = 2
                            elif direction_mode == 2:
                                lcd4.writeText(LCDFont.FONT_5x8, 7, 1, "Off      ")
                                lcd4.flush()
                                direction_mode = 1

                elif event.type == ecodes.EV_ABS:
                    if axis[event.code] in ['LeftJoystickX', 'LeftJoystickY', 'RightJoystickX', 'RightJoystickY']:
                        last[axis[event.code]] = event.value

                        value = event.value - center[axis[event.code]]

                        value_y = ((value * -1) + 0.5)
                        value_x = (value - 0.5)

                        if abs(value) <= CENTER_TOLERANCE:
                            value = 0
                        if axis[event.code] == 'LeftJoystickX':
                            x = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 0, ((str(value_x)) + "      "))
                            lcd4.flush()
                        if axis[event.code] == 'LeftJoystickY':
                            y = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 1, ((str(value_y)) + "      "))
                            lcd4.flush()
                        if axis[event.code] == 'RightJoystickX':
                            twist = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 3, ((str(value_x)) + "      "))
                            lcd4.flush()
                        if axis[event.code] == 'RightJoystickY':
                            z = value
                            lcd4.writeText(LCDFont.FONT_5x8, 28, 2, ((str(value_y)) + "      "))
                            lcd4.flush()

                    elif axis[event.code] in ['CameraX', 'CameraY']:
                        last[axis[event.code]] = event.value

                        value = event.value - center[axis[event.code]]
                        if abs(value) <= CENTER_HAT:
                            value = 0
                        if axis[event.code] == 'CameraX':
                            if value == 0:
                                print('center camera')
                            elif value < 0:
                                print('left camera')
                            else:
                                print('right camera')
                            print(value)

                        elif axis[event.code] == 'CameraY':
                            if value == 0:
                                print('center camera')
                            elif value < 0:
                                print('up camera')
                            else:
                                print('down camera')
                            print(value)
                rov_movement(direction_mode, speed_mode, x, y, z, twist)
        except Exception:
            print("Controller Disconnected")


def rov_movement(direction_mode, speed_mode, x, y, z, twist):
    #   ROV Movement
    if direction_mode == 1:
        if z != 0:
            heave_move = 1500 + (3.125 * z)
            rcServo4.setTargetPosition(heave_move)
            rcServo5.setTargetPosition(heave_move)
            rcServo4.setEngaged(True)
            rcServo5.setEngaged(True)
        else:
            rcServo4.setTargetPosition(1500)
            rcServo5.setTargetPosition(1500)

        if x != 0:
            if speed_mode == 2:
                positive_surge = 1500 + (3.125 * x)
                negative_surge = 1500 - (3.125 * x)
                rcServo0.setTargetPosition(positive_surge)
                rcServo1.setTargetPosition(negative_surge)
                rcServo2.setTargetPosition(positive_surge)
                rcServo3.setTargetPosition(positive_surge)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)
            elif speed_mode == 1:
                positive_surge = 1500 + x
                negative_surge = 1500 - x
                rcServo0.setTargetPosition(positive_surge)
                rcServo1.setTargetPosition(negative_surge)
                rcServo2.setTargetPosition(positive_surge)
                rcServo3.setTargetPosition(positive_surge)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)

        elif y != 0:
            if speed_mode == 2:
                positive_sway = 1500 + (3.125 * y)
                negative_sway = 1500 - (3.125 * y)
                rcServo0.setTargetPosition(negative_sway)
                rcServo1.setTargetPosition(negative_sway)
                rcServo2.setTargetPosition(positive_sway)
                rcServo3.setTargetPosition(negative_sway)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)
            elif speed_mode == 1:
                positive_sway = 1500 + y
                negative_sway = 1500 - y
                rcServo0.setTargetPosition(negative_sway)
                rcServo1.setTargetPosition(negative_sway)
                rcServo2.setTargetPosition(positive_sway)
                rcServo3.setTargetPosition(negative_sway)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)

        elif twist != 0:
            if speed_mode == 2:
                positive_yaw = 1500 + (3.125 * twist)
                negative_yaw = 1500 - (3.125 * twist)
                rcServo0.setTargetPosition(negative_yaw)
                rcServo1.setTargetPosition(positive_yaw)
                rcServo2.setTargetPosition(positive_yaw)
                rcServo3.setTargetPosition(positive_yaw)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)
            elif speed_mode == 1:
                positive_yaw = 1500 + twist
                negative_yaw = 1500 - twist
                rcServo0.setTargetPosition(negative_yaw)
                rcServo1.setTargetPosition(positive_yaw)
                rcServo2.setTargetPosition(positive_yaw)
                rcServo3.setTargetPosition(positive_yaw)
                rcServo0.setEngaged(True)
                rcServo1.setEngaged(True)
                rcServo2.setEngaged(True)
                rcServo3.setEngaged(True)

        else:
            rcServo0.setTargetPosition(1500)
            rcServo1.setTargetPosition(1500)
            rcServo2.setTargetPosition(1500)
            rcServo3.setTargetPosition(1500)

    elif direction_mode == 2:
        if speed_mode == 2:
            H0 = 1500 + (3.125 * surge / 2 - 3.125 * sway / 2)
            H1 = 1500 + (-3.125 * surge / 2 - 3.125 * sway / 2)
            H2 = 1500 + (3.125 * surge / 2 + 3.125 * sway / 2)
            H3 = 1500 + (3.125 * surge / 2 - 3.125 * sway / 2)

        elif speed_mode == 1:
            H0 = 1500 + (surge / 2 - sway / 2)
            H1 = 1500 + (surge / -2 - sway / 2)
            H2 = 1500 + (surge / 2 + sway / 2)
            H3 = 1500 + (surge / 2 - sway / 2)
        else:
            H0 = 1500
            H1 = 1500
            H2 = 1500
            H3 = 1500

        rcServo0.setTargetPosition(H0)
        rcServo1.setTargetPosition(H1)
        rcServo2.setTargetPosition(H2)
        rcServo3.setTargetPosition(H3)
        rcServo0.setEngaged(True)
        rcServo1.setEngaged(True)
        rcServo2.setEngaged(True)
        rcServo3.setEngaged(True)

    else:
        print("Direction mode not set")


def clock():
    #   Timer
    global timer
    global end
    global runtime
    global lcd6
    runtime = 900
    while not end:
        while runtime > 0:
            global lcd6
            if end:
                break
            if timer:
                minutes, secs = divmod(runtime, 60)
                time_format = '{:02d}:{:02d}'.format(minutes, secs)
                lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Time Left Is...")
                lcd6.writeText(LCDFont.FONT_5x8, 0, 1, time_format)
                lcd6.flush()
                time.sleep(1)
                runtime -= 1
            elif not timer:
                lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Timer is Paused!   ")
                lcd6.flush()

        lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Time is up!                ")
        lcd6.writeText(LCDFont.FONT_5x8, 0, 1, "00:00")
        lcd6.flush()
        time.sleep(1)


def cameras():
    #   Dual Camera Feed
    top_view = cv2.VideoCapture(0)
    bottom_view = cv2.VideoCapture(1)
    while not end:
        cv2.imshow('Top_View', top_view)
        cv2.imshow('Bottom_View', bottom_view)


def main():
    global end
    global timer
    global runtime
    global lcd6
    end = False
    timer = False
    runtime = 900

    TopsideComputer.connect()

    try:
        TopsideComputer.thruster_connect()
        TopsideComputer.robot_sensors_connect()
        #    threading.Thread(name='Cameras', target=cameras).start()
    except Exception:
        print("Robot not Found")

    threading.Thread(name='Timer', target=clock()).start()

    controller()

    try:
        input("Press enter to end code\n")
    except KeyboardInterrupt:
        end = True
        pass

    print("\n\n\nEnding...\n\n\n")

    TopsideComputer.topside_sensors_detach()
    TopsideComputer.thruster_disconnect()
    TopsideComputer.robot_sensors_detach()

    TopsideComputer.screendetach()
    print("\n\nProgram Over")
    exit()


main()


