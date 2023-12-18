#!/usr/bin/env python3

#Spencer Quizon

import rospy
from sensor_msgs.msg import Imu



def imu_callback(data):
    global Imu_msg
    Imu_msg = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]

rospy.init_node('IMU_listener', anonymous=True)
rospy.Subscriber("euclid_imu", Imu, imu_callback)

if __name__ == '__main__':
    while not rospy.is_shutdown():
        rate = rospy.Rate(10)
        data = Imu()
        imu_callback(data)
        print(Imu_msg)
    rospy.spin()