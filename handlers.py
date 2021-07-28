import traceback

from Phidget22.Phidget import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.LCD import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.RCServo import *
import datetime as date
import time

lcd0 = None
lcd1 = None
lcd2 = None
lcd3 = None
lcd4 = None
lcd5 = None
lcd6 = None

TopVoltage = None
TopCurrent = None

BotTemperature = None
BotHumidity = None
BotVoltage = None
BotCurrent = None

rcServo0 = None
rcServo1 = None
rcServo2 = None
rcServo3 = None
rcServo4 = None
rcServo5 = None

Lights = None

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
    global temperature_data
    global ax_three
    global canvas_three
    if "0" in str(self.getChannel()):
        temperature_data.pop(0)
        temperature_data.append(sensor_value)
        ax_three.clear()
        ax_three.set_ylim([0, 40])
        ax_three.plot(range(len(temperature_data)), temperature_data)
        canvas_three.draw()
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


#   Screen Setup


def connect():
    global lcd0
    global lcd1
    global lcd2
    global lcd3
    global lcd4
    global lcd5
    global lcd6

    global TopVoltage
    global TopCurrent

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

    lcd0.setOnAttachHandler(on_large_screen_attach)
    lcd0.setOnDetachHandler(on_screen_detach)
    lcd0.setOnErrorHandler(on_error)
    lcd2.setOnAttachHandler(on_large_screen_attach)
    lcd2.setOnDetachHandler(on_screen_detach)
    lcd2.setOnErrorHandler(on_error)
    lcd4.setOnAttachHandler(on_large_screen_attach)
    lcd4.setOnDetachHandler(on_screen_detach)
    lcd4.setOnErrorHandler(on_error)
    lcd6.setOnAttachHandler(on_mini_screen_attach)
    lcd6.setOnDetachHandler(on_screen_detach)
    lcd6.setOnErrorHandler(on_error)

    TopVoltage.setOnErrorHandler(on_error)
    TopCurrent.setOnErrorHandler(on_error)

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
    today = str(date.date.today())
    lcd6.writeText(LCDFont.FONT_5x8, 0, 0, "Timer not set")
    lcd6.writeText(LCDFont.FONT_5x8, 0, 1, "00:00")
    lcd6.writeText(LCDFont.FONT_5x8, 0, 3, today)
    lcd6.writeText(LCDFont.FONT_5x8, 15, 3, "OD-4D")
    lcd6.flush()

    TopVoltage.setOnVoltageChangeHandler(on_topside_voltage_change)
    TopCurrent.setOnVoltageRatioChangeHandler(on_topside_current_change)


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


def robot_sensors_connect():
    try:
        global BotTemperature
        global BotHumidity
        global BotVoltage
        global BotCurrent

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

        BotTemperature.setOnSensorChangeHandler(on_temperature_sensor_change)
        BotTemperature.setOnErrorHandler(on_error)
        BotHumidity.setOnSensorChangeHandler(on_temperature_sensor_change)
        BotHumidity.setOnErrorHandler(on_error)

        BotVoltage.setOnVoltageChangeHandler(on_robot_voltage_change)
        BotVoltage.setOnErrorHandler(on_error)
        BotCurrent.setOnVoltageRatioChangeHandler(on_robot_current_change)
        BotCurrent.setOnErrorHandler(on_error)

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


def topside_sensors_detach():
    TopVoltage.close()
    TopCurrent.close()


def robot_sensors_detach():
    BotTemperature.close()
    BotHumidity.close()
    BotVoltage.close()
    BotCurrent.close()


#   Lights
def lights_connect():
    global Lights

    Lights = RCServo()
    Lights.setDeviceSerialNumber(493392)
    Lights.setChannel(6)
    Lights.openWaitForAttachment(5000)
    Lights.setMinPulseWidth(1100)
    Lights.setMaxPulseWidth(1900)
    Lights.setMinPosition(1100)
    Lights.setMaxPosition(1900)


def lights_disconnect():
    Lights.setTargetPosition(1100)
    Lights.setEngaged(True)
    Lights.close()


#   Thruster
def thruster_connect():
    try:
        global rcServo0
        global rcServo1
        global rcServo2
        global rcServo3
        global rcServo4
        global rcServo5

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

        rcServo0.setOnAttachHandler(on_attach_thruster)
        rcServo0.setOnDetachHandler(on_detach_thruster)
        rcServo1.setOnAttachHandler(on_attach_thruster)
        rcServo1.setOnDetachHandler(on_detach_thruster)
        rcServo2.setOnAttachHandler(on_attach_thruster)
        rcServo2.setOnDetachHandler(on_detach_thruster)
        rcServo3.setOnAttachHandler(on_attach_thruster)
        rcServo3.setOnDetachHandler(on_detach_thruster)
        rcServo4.setOnAttachHandler(on_attach_thruster)
        rcServo4.setOnDetachHandler(on_detach_thruster)
        rcServo5.setOnAttachHandler(on_attach_thruster)
        rcServo5.setOnDetachHandler(on_detach_thruster)

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


def thruster_disconnect():
    rcServo0.close()
    rcServo1.close()
    rcServo2.close()
    rcServo3.close()
    rcServo4.close()
    rcServo5.close()

