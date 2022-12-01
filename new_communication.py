"""
    - New communication script (Mx series 2.0)
    Author: Othman Turki
    Date: 2022/11/07
"""

# import os
import time
import threading
# import nep
# import nep_local_lan as nep_2
import numpy as np
from dynamixel_sdk import *  # Uses Dynamixel SDK library

import constants_definition_yokobo as constants


def initialization():
    """ Initialization of Yokobo: Works when Yokobo start """

    global portHandler
    global packetHandler
    global dx1, dx2, dx3, defaultSpeed

    EmergencyFlag = False

    initial_pos = [constants.MOTOR_1_CENTER,
                   constants.MOTOR_2_MIN_LIM,
                   constants.MOTOR_3_CENTER]

    portHandler = PortHandler(constants.DEVICENAME)
    packetHandler = PacketHandler(constants.PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        # getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(constants.BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        # getch()
        quit()

    # Disable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, constants.DXL1_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL2_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL3_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)

    # Enable position mode Dynamixel #1
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_PRO_OPERATING_MODE, 3)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel has been successfully putted in position control")

    # Enable position mode Dynamixel #2
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_PRO_OPERATING_MODE, 3)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel has been successfully putted in position control")

    # Enable position mode Dynamixel #3
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_PRO_OPERATING_MODE, 3)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel has been successfully putted in position control")

    # Enable Dynamixel Torque #1
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel#%d has been enabled" % constants.DXL1_ID)

    # Enable Dynamixel Torque #2
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel#%d has been enabled" % constants.DXL2_ID)

    # Enable Dynamixel Torque #3
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        # flag_error = True
    else:
        print("Dynamixel#%d has been enabled" % constants.DXL3_ID)

    # Set profile velocity and accereration (Bigger value for smoother motion)
    defaultSpeed = [1000, 1000, 1000]
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, 108, defaultSpeed[0])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, 108, defaultSpeed[1])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, 108, defaultSpeed[2])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, 112, defaultSpeed[0])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, 112, defaultSpeed[1])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, 112, defaultSpeed[2])

    dxl_present_position1, dxl_present_position2, dxl_present_position3 = read_motors()
    dxl3 = dxl_present_position3 % 4096
    over = dxl_present_position3 / 4096
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL1_ID, dxl_present_position1))
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL2_ID, dxl_present_position2))
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL3_ID, dxl_present_position3))

    if over >= 1:
        packetHandler.write1ByteTxRx(
            portHandler, constants.DXL3_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
        packetHandler.write1ByteTxRx(
            portHandler, constants.DXL3_ID, constants.ADDR_PRO_OPERATING_MODE, 1)
        packetHandler.write1ByteTxRx(
            portHandler, constants.DXL3_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
        time.sleep(0.3)
        while True:
            packetHandler.write4ByteTxRx(
                portHandler, constants.DXL3_ID, 104, np.sign(constants.MOTOR_3_CENTER-dxl3)*10)
            dxl_present_position1, dxl_present_position2, dxl_present_position3 = read_motors()
            nowpos = dxl_present_position3 % 4096 + 100
            if nowpos < constants.MOTOR_3_CENTER:
                break
        packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID, 104, 0)
    time.sleep(0.3)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL3_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_PRO_OPERATING_MODE, 3)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL3_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    time.sleep(0.3)

    # Write commands to motors (to initial positions)
    write_motors(initial_pos[0], initial_pos[1], initial_pos[2])
    time.sleep(3)

    # Read current positions
    dxl_present_position1, dxl_present_position2, dxl_present_position3 = read_motors()
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL1_ID, dxl_present_position1))
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL2_ID, dxl_present_position2))
    print("[ID:%03d] PresPos:%03d" %
          (constants.DXL3_ID, dxl_present_position3))
    dx1 = dxl_present_position1
    dx2 = dxl_present_position2
    dx3 = dxl_present_position3

    while True:
        if packetHandler != {}:
            break

    while True:
        while True:
            time.sleep(1.0)
            if EmergencyFlag == True:
                break
        break

    print("thread started")


def read_motors():
    """ Read Dynamixel motors present positions """

    global packetHandler
    global dx1, dx2, dx3

    dxl_present_position1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_PRESENT_POSITION)
    dxl_present_position2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_PRESENT_POSITION)
    dxl_present_position3, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_PRESENT_POSITION)
    if dxl_present_position1 == 0 or dxl_present_position2 == 0 or dxl_present_position3 == 0:
        while int(dxl_present_position1*dxl_present_position2*dxl_present_position3) == 0:
            dxl_present_position1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
                portHandler, constants.DXL1_ID, constants.ADDR_MX_PRESENT_POSITION)
            dxl_present_position2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
                portHandler, constants.DXL2_ID, constants.ADDR_MX_PRESENT_POSITION)
            dxl_present_position3, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
                portHandler, constants.DXL3_ID, constants.ADDR_MX_PRESENT_POSITION)
            print("can't read")
    return dxl_present_position1, dxl_present_position2, dxl_present_position3


def write_motors(control_motor_1, control_motor_2, control_motor_3,
                 duration_time=0):
    """ Write positions to Dynamixel motors  """

    global packetHandler

    if int(control_motor_1) > constants.MOTOR_1_MAX_LIM:
        control_motor_1 = constants.MOTOR_1_MAX_LIM
    elif int(control_motor_1) < constants.MOTOR_1_MIN_LIM:
        control_motor_1 = constants.MOTOR_1_MIN_LIM
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_GOAL_POSITION, int(control_motor_1))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error1 = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL1_ID, 18)
        print("18-1: ", dxl)
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL1_ID, 17)
        print("17-1: ", dxl)
        # flag_error1 = True
    # else:
        # flag_error1 = False

    if int(control_motor_2) > constants.MOTOR_2_MAX_LIM:
        control_motor_2 = constants.MOTOR_2_MAX_LIM
    elif int(control_motor_2) < constants.MOTOR_2_MIN_LIM:
        control_motor_2 = constants.MOTOR_2_MIN_LIM
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_GOAL_POSITION, int(control_motor_2))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error2 = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL2_ID, 18)
        print("18-2: ", dxl)
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL2_ID, 17)
        print("17-2: ", dxl)
        # flag_error2 = True
    # else:
        # flag_error2 = False
    # print("Dynamixel#%d" % constants.DXL2_ID, int(cmd2))

    if int(control_motor_3) > constants.MOTOR_3_MAX_LIM:
        control_motor_3 = constants.MOTOR_3_MAX_LIM
    elif int(control_motor_3) < constants.MOTOR_3_MIN_LIM:
        control_motor_3 = constants.MOTOR_3_MIN_LIM
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_GOAL_POSITION, int(control_motor_3))
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        # flag_error3 = True
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL3_ID, 18)
        print("18-3: ", dxl)
        dxl, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, constants.DXL3_ID, 17)
        print("17-3: ", dxl)
        # flag_error3 = True
    # else:
        # flag_error3 = False
        # print("Dynamixel#%d" % constants.DXL3_ID, int(control_motor_3))

        # if flag_error1 == False and flag_error2 == False and flag_error3 == False:
        #     pass
        #print(int(control_motor_1), int(control_motor_2), int(control_motor_3))
    time.sleep(duration_time)


# def initialize_pos(ini_pos):
#     global portHandler
#     global packetHandler

#     now_pos2 = dx2
#     diff = ini_pos[1] - now_pos2
#     step_num = int(abs(diff)/100)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID, 108, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID, 112, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID, 108, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID, 112, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID, 108, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID, 112, 1000)
#     for ii in range(step_num):
#         com = now_pos2+100*ii*np.sign(diff)
#         packetHandler.write4ByteTxRx(
#             portHandler, constants.DXL2_ID, constants.ADDR_MX_GOAL_POSITION, int(com))
#         time.sleep(0.1)
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL1_ID, constants.ADDR_MX_GOAL_POSITION, int(ini_pos[0]))
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL2_ID, constants.ADDR_MX_GOAL_POSITION, int(ini_pos[1]))
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL3_ID, constants.ADDR_MX_GOAL_POSITION, int(ini_pos[2]))
#     time.sleep(1.5)


# def Greeting():
#     ini_pos = [constants.MOTOR_1_CENTER,
#                constants.MOTOR_2_MIN_LIM, constants.MOTOR_3_CENTER]
#     initialize_pos(ini_pos)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID, 108, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID, 112, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID, 108, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID, 112, 1000)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_MIN_LIM+500))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_MIN_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_MAX_LIM))
#     time.sleep(1)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_MAX_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_MIN_LIM))
#     time.sleep(1)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_MIN_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_MAX_LIM))
#     time.sleep(1)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_MAX_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_MIN_LIM))
#     time.sleep(1)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_MIN_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_MAX_LIM))
#     time.sleep(1)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL3_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_3_CENTER))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER-200))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER+200))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER-200))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER+200))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER-200))
#     time.sleep(1.5)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_CENTER+200))
#     time.sleep(2)
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL2_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_2_MIN_LIM))
#     packetHandler.write4ByteTxRx(portHandler, constants.DXL1_ID,
#                                  constants.ADDR_MX_GOAL_POSITION, int(constants.MOTOR_1_CENTER))
#     time.sleep(2)
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL2_ID, 108, defaultSpeed[1])
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL2_ID, 112, defaultSpeed[1])
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL1_ID, 108, defaultSpeed[0])
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL1_ID, 112, defaultSpeed[0])
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL3_ID, 108, defaultSpeed[2])
#     packetHandler.write4ByteTxRx(
#         portHandler, constants.DXL3_ID, 112, defaultSpeed[2])


initialization()
print("end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
