"""
    - Make motors in initial state (Mx series 2.0)
    Author: Othman Turki
    Date: 2022/11/01
"""

import os
from dynamixel_sdk import *  # Uses Dynamixel SDK library

import constants_definition_yokobo as constants

if os.name == 'nt':  # Windows
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
# else:  # Linux
#     import sys
#     import tty
#     import termios
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)

#     def getch():
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch


def init_state():
    portHandler = PortHandler(constants.DEVICENAME)
    packetHandler = PacketHandler(constants.PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(constants.BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    # Disable Dynamixel Torque
    packetHandler.write1ByteTxRx(portHandler, constants.DXL1_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL2_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL3_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)

    # Enable position mode Dynamixel
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_PRO_OPERATING_MODE, 3)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #1 has been successfully putted in position control")

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_PRO_OPERATING_MODE, 3)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #2 has been successfully putted in position control")

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_PRO_OPERATING_MODE, 3)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #3 has been successfully putted in position control")

    # Set profile velocity and accereration (Bigger value for smoother motion)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, 108, 1000)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, 108, 1000)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, 108, 1000)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, 112, 1000)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, 112, 1000)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, 112, 1000)

    # Enable Dynamixel #1 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #1 has been successfully connected")

    # Enable Dynamixel #2 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #2 has been successfully connected")

    # Enable Dynamixel #3 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel #3 has been successfully connected")

    # Read present position
    dxl_present_position1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_present_position2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_PRESENT_POSITION)
    dxl_present_position2 = dxl_present_position2 % 4096
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_present_position3, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    print(dxl_present_position1)
    print(dxl_present_position2)
    print(dxl_present_position3)

    initial_pos = [
        constants.MOTOR_1_CENTER,
        constants.MOTOR_2_CENTER,
        constants.MOTOR_3_CENTER,
    ]

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL1_ID, constants.ADDR_MX_GOAL_POSITION, initial_pos[0])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL2_ID, constants.ADDR_MX_GOAL_POSITION, initial_pos[1])
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, constants.DXL3_ID, constants.ADDR_MX_GOAL_POSITION, initial_pos[2])

    time.sleep(3)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL1_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL2_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)
    packetHandler.write1ByteTxRx(portHandler, constants.DXL3_ID,
                                 constants.ADDR_MX_TORQUE_ENABLE, constants.TORQUE_DISABLE)

    print('end')


init_state()
