import time
import pickle
import os.path
import struct
import math

from dronekit import connect , VehicleMode
import time
from pymavlink import mavutil
import argparse

def connectMyCopter():
	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()
	
	connection_string = args.connect
	baud_rate = 57600
	vehicle = connect(connection_string,baud=baud_rate,wait_ready=True)
	return vehicle

def arm_and_takeoff(aTargetAltitude):
    """A
    Arms vehicle and fly to aTargetAltitude.
    """
    
    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)

def goto_position_target_relative_ned(velocity_x, velocity_y, velocity_z, vehicle):

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    vehicle.send_mavlink(msg)


def LAND():
    vehicle.mode = VehicleMode("LAND")
    print(" Mode: %s" % vehicle.mode.name)  # settable

    while vehicle.mode.name != "LAND":
        time.sleep(1)
        print("Vehicle mode is: %s" % str(vehicle.mode.name))
        vehicle.mode = VehicleMode("LAND")

    print("Vehicle Mode is : LAND")
    
def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

def saveData(data, name):
    pickle_file = name + '.pkl'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_directory, pickle_file)

    if os.path.isfile(pickle_file_path) and os.path.getsize(pickle_file_path) > 0:
        with open(pickle_file_path, 'rb') as f:
            location_data = pickle.load(f)
    else:
        location_data = []

    location_data.extend([data])

    with open(pickle_file_path, 'wb') as f:
        pickle.dump(location_data, f, protocol=2)
        f.close()

def readData(database):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_directory, database)

    if os.path.isfile(pickle_file_path) and os.path.getsize(pickle_file_path) > 0:
        with open(pickle_file_path, 'rb') as f:
            try:
                location_data = pickle.load(f)
            except (EOFError, struct.error):
                location_data = []

        if len(location_data) > 0:
            return location_data[-1]
    else:
        return None
    
if __name__=="__main__":
    # Connect to drone
    '''vehicle = connectMyCopter()
    time.sleep(1)
    
    # Take off
    arm_and_takeoff(3)
    time.sleep(3)
    
    while True:
        try:
            face = readData("face.pkl")
            break
        except:
            continue'''
    
    while True:
        targets = []
        humans = readData("human.pkl")
        colors = readData("color.pkl")
        
        try:
            error_check = len(humans)
            error_check = len(colors)
        except:
            print("what...")
            continue
        
        for human in humans:
            for color in colors:
                x1 = max(color[0], human[0])
                y1 = max(color[1], human[1])
                x2 = min(color[0]+color[2], human[0]+human[2])
                y2 = min(color[1]+color[3], human[1]+human[3])

                if x2 > x1 and y2 > y1:
                    intersection_area = (x2 - x1) * (y2 - y1)
                else:
                    intersection_area = 0

                rect1_area = color[2] * color[3]
                rect2_area = human[2] * human[3]

                percentage_intersection = (float(intersection_area) / (rect1_area + rect2_area - intersection_area)) * 100
                print(percentage_intersection)
                
                if percentage_intersection >= 5:
                    targets.append(color)
                    
        final_distance = 1000
        if len(targets) != 0:
            final_target = targets[0]
        else:
            continue
        '''for target in targets:
            target_pos = [target[0] + target[2]/2, target[1] + target[3]/2]
            face_pos = [face[0] + face[2]/2, face[1] + face[3]/2]
            distance = math.sqrt((face_pos[0] - target_pos[0])**2 + (face_pos[1] - target_pos[1])**2)
            if distance < final_distance:
                final_distance = distance
                final_target = target
                target_check = 1'''
            
        if len(final_target) > 0:    
            final_target_x = final_target[0] + final_target[2]/2
            final_target_y = final_target[1] + final_target[3]/2
    
            if final_target_x > 175:
                #condition_yaw(vehicle.heading + 5)
                print("Sağa Dön")
                time.sleep(1)
            elif final_target_x < 145:
                #condition_yaw(vehicle.heading - 5)
                print("Sola Dön")
                time.sleep(1)
            if final_target[2]*final_target[3] < 400:
                #goto_position_target_relative_ned(0.3, 0, 0, vehicle)
                print("İleri Git")
                time.sleep(1)
            elif final_target[2]*final_target[3] > 800:
                #goto_position_target_relative_ned(-0.3, 0, 0, vehicle)
                print("Geri Git")
                time.sleep(1)
        
        #if time.time() - start_time >= 60:
            #saveData("RTL", "log")
            #break

'''if __name__=="__main__":
    
    vehicle.airspeed=5
    vehicle.groundspeed=5
    
    # Connect to drone
    vehicle = connectMyCopter()
    time.sleep(1)
    
    # Take off
    arm_and_takeoff(3)
    time.sleep(3)
    saveData("TAKE_OFF", "log")
    
    start_time = time.time()
    
    while True:
    
        color = readData("color.pkl")
        color_x = color[0] + color[2]/2
        color_y = color[1] + color[3]/2
    
        if color_x > 340:
            condition_yaw(vehicle.heading + 5)
            time.sleep(1)
        elif color_x < 300:
            condition_yaw(vehicle.heading - 5)
            time.sleep(1)
        if color[2]*color[3] < :
            goto_position_target_relative_ned(0.3, 0, 0, vehicle)
            time.sleep(3)
        
        if time.time() - start_time >= 60:
            saveData("RTL", "log")
            break
    
    LAND()
    vehicle.close()'''
