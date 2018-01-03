import time, logging
from dronekit import VehicleMode, LocationGlobalRelative, connect
from pymavlink import mavutil

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

def main():
    vehicle = Vehicle('udp:127.0.0.1:14553')
    vehicle.status_info()

class Vehicle():
    def __init__(self, port, baud=57600, wait_ready=True):
        self.vehicle = connect(port, baud, wait_ready)
        self.status_info()

    def status_info(self):
        logging.debug("---------------------------------------------------")
        logging.debug(" GPS:            " + str(self.vehicle.gps_0))
        logging.debug(" Battery:        " + str(self.vehicle.battery))
        logging.debug(" Last Heartbeat: " + str(self.vehicle.last_heartbeat))
        logging.debug(" Is Armable?:    " + str(self.vehicle.is_armable))
        logging.debug(" System status:  " + str(self.vehicle.system_status.state))
        logging.debug(" Mode:           " + str(self.vehicle.mode.name))
        logging.debug("---------------------------------------------------")


    def check_n_arm(self):
        logging.debug("Basic pre-arm checks")
        if not self.vehicle.armed:
            # Don't let the user try to arm until autopilot is ready
            while not self.vehicle.is_armable:
                logging.debug("Waiting for vehicle to initialise...")
                time.sleep(1)
            logging.debug("Arming motors")
            # Copter should arm in GUIDED mode
            self.vehicle.mode    = VehicleMode("GUIDED")
            self.vehicle.armed   = True
            while not self.vehicle.armed:
                logging.debug("Waiting for arming...")
                time.sleep(1)
        else:
            logging.debug("Vehicle already armed")


    def take_off(self, z=1):
        logging.debug("Taking off...")
        self.vehicle.simple_takeoff(z)
        while True:
            logging.debug("Altitude: " + str(self.vehicle.location.global_relative_frame.alt))
            if self.vehicle.location.global_relative_frame.alt>=z*0.95:
                break
            time.sleep(1)


    def move_up(self, z=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,
            0, 0, 0,                            # x, y, z positions
            0, 0, -1*z,                         # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def move_down(self, z=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,
            0, 0, 0,                            # x, y, z positions
            0, 0, z,                            # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def move_left(self, y=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,
            0, 0, 0,                            # x, y, z positions
            0, -1*y, 0,                         # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def move_right(self, y=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,                 # type_mask
            0, 0, 0,                            # x, y, z positions
            0, y, 0,                            # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def move_forward(self, x=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,
            0, 0, 0,                            # x, y, z positions
            x, 0, 0,                            # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def move_backward(self, x=0.25, cycles=1):
        self.vehicle.flush()
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
            0b0000111111000111,
            0, 0, 0,                            # x, y, z positions
            -1*x, 0, 0,                         # x, y, z movement in m/s
            0, 0, 0,                            # x, y, z acceleration
            0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def yaw_angle(self, heading=0, relative=True, cycles=1):
        self.vehicle.flush()
        msg = vehicle.message_factory.command_long_encode(
            0, 0, mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0, heading,                    # heading yaw in degrees
            0, 1, 1 if relative else 0,    # yaw relative to body
            0, 0, 0)
        for times in range(cycles):
            self.vehicle.send_mavlink(msg)
            time.sleep(1)
        self.vehicle.flush()


    def simple_goto(self, waypoints, sleep=1):
        for point in waypoints:
            logging.debug("going to point: " + str(waypoints.index(point)+1))
            self.vehicle.simple_goto(LocationGlobalRelative(point[0], point[1], point[2]))
            #time.sleep(point[1])
            difference_lat = (point[0] - self.vehicle.location.global_relative_frame.lat) *100000
            difference_lon = (point[1] - self.vehicle.location.global_relative_frame.lon) *100000
            while abs(difference_lat) > 0.5 and abs(difference_lon) > 0.5:
                difference_lat = (point[0] - self.vehicle.location.global_relative_frame.lat) *100000
                difference_lon = (point[1] - self.vehicle.location.global_relative_frame.lon) *100000
                logging.debug(str(int(difference_lat))+" "+str(int(difference_lon)))
                time.sleep(sleep)

if __name__ == "__main__":
    main()