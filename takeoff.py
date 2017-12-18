import time
import argparse
import pyfirmata
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


# Using parser argument
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='udp:10.42.0.1:14551')
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


def take_off(aTargetAltitude=2):
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            status_info()
            break
        time.sleep(1)


check_n_arm()
status_info() 
take_off()



#vehicle.mode = VehicleMode("LAND")
vehicle.close()

