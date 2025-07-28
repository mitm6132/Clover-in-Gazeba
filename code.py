import rospy
from clover import srv
from std_srvs.srv import Trigger
import math

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
set_yaw_rate = rospy.ServiceProxy('set_yaw_rate', srv.SetYawRate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

navigate(x=0, y=0, z=1, frame_id='body', auto_arm=True)
rospy.sleep(3)
navigate_wait(x = 0, y = 1, z=1, frame_id = 'aruco_map')
rospy.sleep(3)
navigate_wait(x = 1, y = 1, z=1, frame_id = 'aruco_map')
rospy.sleep(3)
navigate_wait(x = 2, y = 1, z=1, frame_id = 'aruco_map')
rospy.sleep(3)
navigate_wait(x = 1, y = 1, z=1, frame_id = 'aruco_map')
rospy.sleep(3)
navigate_wait(x = 0, y = 0, z=1, frame_id = 'aruco_map')
rospy.sleep(3)

land()