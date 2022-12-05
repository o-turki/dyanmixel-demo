"""
Yokobo Animations
"""

import time
from dynamixel_sdk import *

import constants_definition_yokobo as cst
from animation_logger import animation_logger

timing = []
rotations = []


def intrusion(cycles_number, duration):
    """ Movements of the Yokobo in case of intrusion """

    global timing
    global rotations
    timing = []
    rotations = []

    portHandler = PortHandler(cst.DEVICENAME)
    packetHandler = PacketHandler(cst.PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        quit()
    # Set port baudrate
    if portHandler.setBaudRate(cst.BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        quit()

    # Enable Dynamixel Torque
    toggle_torque(portHandler, packetHandler, cst.DXL1_ID, cst.TORQUE_ENABLE)
    # toggle_torque(portHandler, packetHandler, cst.DXL2_ID, cst.TORQUE_ENABLE)

    # Set profile accereration and velocity (Bigger value for smoother motion)
    set_acceleration_and_velocity(
        portHandler, packetHandler, cst.DXL1_ID, 1000)
    # set_acceleration_and_velocity(
    #     portHandler, packetHandler, cst.DXL2_ID, 1000)

    # ================================================================================
    # ANIMATION <START>
    # ================================================================================
    start = time.time()

    end = time.time()
    timing.append(round(end - start, 1))
    read_motor(portHandler, packetHandler, cst.DXL1_ID, cst.MOTOR_1_CENTER)

    write_motor(portHandler, packetHandler,
                cst.DXL1_ID, cst.MOTOR_1_CENTER, duration)

    end = time.time()
    timing.append(round(end - start, 1))
    read_motor(portHandler, packetHandler, cst.DXL1_ID, cst.MOTOR_1_CENTER)

    # write_motor(portHandler, packetHandler,
    #             cst.DXL2_ID, cst.MOTOR_2_CENTER, duration)
    # for _ in range(math.ceil(cycles_number / 2)):
    #     write_motor(portHandler, packetHandler,
    #                 cst.DXL2_ID, cst.MOTOR_2_MIN_LIM, duration)
    #     write_motor(portHandler, packetHandler,
    #                 cst.DXL2_ID, cst.MOTOR_2_MAX_LIM, duration)

    for _ in range(cycles_number):
        write_motor(portHandler, packetHandler,
                    cst.DXL1_ID, cst.MOTOR_1_MIN_LIM, duration)

        end = time.time()
        timing.append(round(end - start, 1))
        read_motor(portHandler, packetHandler, cst.DXL1_ID, cst.MOTOR_1_CENTER)

        write_motor(portHandler, packetHandler,
                    cst.DXL1_ID, cst.MOTOR_1_MAX_LIM, duration)

        end = time.time()
        timing.append(round(end - start, 1))
        read_motor(portHandler, packetHandler, cst.DXL1_ID, cst.MOTOR_1_CENTER)

    # BACK TO CENTER
    write_motor(portHandler, packetHandler,
                cst.DXL1_ID, cst.MOTOR_1_CENTER, duration)
    # write_motor(portHandler, packetHandler,
    #             cst.DXL2_ID, cst.MOTOR_2_CENTER, duration)

    end = time.time()
    timing.append(round(end - start, 1))
    read_motor(portHandler, packetHandler, cst.DXL1_ID, cst.MOTOR_1_CENTER)
    # ================================================================================
    # ANIMATION <END>
    # ================================================================================

    # Disable Dynamixel Torque
    toggle_torque(portHandler, packetHandler, cst.DXL1_ID, cst.TORQUE_DISABLE)
    # toggle_torque(portHandler, packetHandler, cst.DXL2_ID, cst.TORQUE_DISABLE)

    portHandler.closePort()


def toggle_torque(port_handler, packet_handler, dxl_id, state):
    """ Toggle Dynamixel Torque ON and OFF """

    dxl_comm_result, dxl_error = packet_handler.write1ByteTxRx(
        port_handler, dxl_id, cst.ADDR_TORQUE, state)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))
    else:
        if state == cst.TORQUE_ENABLE:
            print(f"Dynamixel {dxl_id} has been successfully connected")
        if state == cst.TORQUE_DISABLE:
            print(f"Dynamixel {dxl_id} has been successfully disconnected")


def set_acceleration_and_velocity(port_handler, packet_handler, dxl_id, speed):
    """ Set profile accereration and velocity """

    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
        port_handler, dxl_id, cst.ADDR_PROFILE_ACCELERATION, speed)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
        port_handler, dxl_id, cst.ADDR_PROFILE_VELOCITY, speed)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))


def write_motor(port_handler, packet_handler, dxl_id, goal_position, duration):
    """ Write to Dynamixel """

    limits = {
        cst.DXL1_ID: {
            "MIN_LIMIT": cst.MOTOR_1_MIN_LIM,
            "MAX_LIMIT": cst.MOTOR_1_MAX_LIM,
        },
        cst.DXL2_ID: {
            "MIN_LIMIT": cst.MOTOR_2_MIN_LIM,
            "MAX_LIMIT": cst.MOTOR_2_MAX_LIM,
        },
        cst.DXL3_ID: {
            "MIN_LIMIT": cst.MOTOR_3_MIN_LIM,
            "MAX_LIMIT": cst.MOTOR_3_MAX_LIM,
        },
    }
    if int(goal_position) < limits[dxl_id]["MIN_LIMIT"]:
        goal_position = limits[dxl_id]["MIN_LIMIT"]
    if int(goal_position) > limits[dxl_id]["MAX_LIMIT"]:
        goal_position = limits[dxl_id]["MAX_LIMIT"]

    dxl_comm_result, dxl_error = packet_handler.write4ByteTxRx(
        port_handler, dxl_id, cst.ADDR_GOAL_POSITION, goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))
    time.sleep(duration)


def read_motor(port_handler, packet_handler, dxl_id, center):
    """ Read from Dynamixel """

    dxl_present_position, dxl_comm_result, dxl_error = packet_handler.read4ByteTxRx(
        port_handler, dxl_id, cst.ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packet_handler.getRxPacketError(dxl_error))

    # print(round(dxl_present_position - center, -1))
    # print(round((dxl_present_position - center) / 4096 * 360))
    rotations.append(round((dxl_present_position - center) / 4096 * 360))


# intrusion(3, cst.SECONDS_DELAY)
# print(timing)
# print(rotations)

# timing = [0.0, 1.0, 2.1, 3.1, 4.2, 5.2, 6.2, 7.3, 8.3]
# rotations = [0, 0, -52, 52, -52, 52, -52, 52, 0]
# animation_logger("Intrusion", "M1", timing, rotations, 0, 0)

def animate_intrusion():
    """ Animation and Log to Excel File """

    intrusion(3, cst.SECONDS_DELAY)
    animation_logger("Intrusion", "M1", timing, rotations, 0, 0)


animate_intrusion()
