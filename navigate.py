import time
import argparse
import pyfirmata
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


# Using parser argument
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='udp:10.42.0.1:14552')
args = parser.parse_args()
# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud=57600, wait_ready=True)

def status_info():
    print "---------------------------------------------------"
    print " GPS: %s" % vehicle.gps_0
    print " Battery: %s" % vehicle.battery
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Is Armable?: %s" % vehicle.is_armable
    print " System status: %s" % vehicle.system_status.state
    print " Mode: %s" % vehicle.mode.name    # settable
    print "---------------------------------------------------"
def check_n_arm():
    print "Basic pre-arm checks"
    if not vehicle.armed:
        # Don't let the user try to arm until autopilot is ready
        while not vehicle.is_armable:
            print " Waiting for vehicle to initialise..."
            time.sleep(1)
        print "Arming motors"
        # Copter should arm in GUIDED mode
        vehicle.mode    = VehicleMode("GUIDED")
        vehicle.armed   = True
        while not vehicle.armed:
            print " Waiting for arming..."
            time.sleep(1)
    else:
        print "Vehicle already armed"


def move_up(z=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        0, 0, -1*z,                          # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
def move_down(z=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        0, 0, z,                          # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
def move_left(y=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        0, -1*y, 0,                          # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
def move_right(y=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        0, y, 0,                          # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
def move_forward(x=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        x, 0, 0,                          # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
def move_backward(x=0.25):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,                                  # time_boot_ms (not used)
        0, 0,                               # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000111111000111,                 # type_mask
        0, 0, 0,                            # x, y, z positions (not used)
        -1*x, 0, 0,                       # m/s
        0, 0, 0,                            # x, y, z acceleration
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

status_info()
check_n_arm()
move_right(0.)

vehicle.close()
