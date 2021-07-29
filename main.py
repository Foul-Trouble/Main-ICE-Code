# Russell Corbett 2020
# OD - 4D
# Any questions, email me at russellcorbett11@gmail.com

from handlers import *
from bot_gui import *
from visuals import *

from Phidget22.Devices.LCD import *

import time
from datetime import datetime

import threading

import platform
if platform.system() == "Linux":
    import evdev
    from evdev import InputDevice, categorize, ecodes

global timer
global runtime
global end
global lcd6

global end
global connected
global ICE

log = open("log.txt", "a")
now = datetime.now()
log.write(f"Program Start at {now}\n")


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


def robot():
    global ICE
    while not end:
        if not ICE:
            try:
                thruster_connect()
                robot_sensors_connect()
                try:
                    threading.Thread(name='Cameras', target=cameras).start()
                except:
                    print("Cameras not functioning or connected")
                ICE = True
            except Exception:
                print("Robot not Found")
                ICE = False


class Controllers:

    def __init__(self):
        pass

    @staticmethod
    def playstation_joystick_controller():
        log.write("Connected Playstation Controller\n")
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
            log.write("Disconnected Playstation Controller\n")
            print("Controller Disconnected")

    @staticmethod
    def logitech_controller():
        log.write("Connected Logitech Controller\n")
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
                if not end:
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
            log.write("Disconnected Logitech Controller\n")
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
        sway = x
        surge = y

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

    thruster_power_data = [H0, H1, H2, H3, heave_move]
    thruster_ax.clear()
    thruster_ax.patch.set_facecolor("black")
    thruster_ax.set_xlim([-0.5, len(thruster_power_data) - 0.5])
    thruster_ax.bar(range(len(thruster_power_data)), thruster_power_data)
    thruster_canvas.draw()


def clock():
    #   Timer
    global timer
    global end
    global runtime
    timer = False
    runtime = 900
    while not end:
        while runtime > 0:
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


def main():
    global end
    global connected
    global ICE
    end = False
    connected = False
    ICE = False
    if platform.system() == "Linux":
        log.write("Connected through Linux\n")
        try:
            connect()
            connected = True

            threading.Thread(name='Timer', target=clock()).start()

            threading.Thread(name='Controllers', target=controller()).start()

            threading.Thread(name='Robot', target=robot()).start()

        except:
            connected = False
            ICE = False
            print("Something is seriously wrong...")
    elif platform.system() == "Darwin":
        print("Russell is probably testing the GUI")
        log.write("Connected through Mac\n")
    else:
        print("I see you Windows")
        log.write("Connected through Windows\n")

    gui(ICE, connected)

    print("\n\n\nEnding...\n\n\n")

    end = True
    if ICE:
        thruster_disconnect()
        robot_sensors_detach()
    if connected:
        topside_sensors_detach()
        screen_detach()
    print("Program Over")
    now = datetime.now()
    log.write(f"Program End at {now}\n\n")
    log.close()
    exit()


main()


