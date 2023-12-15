#!/usr/bin/env python3

#MAde by SPENCER FUCKING QUIZON (REMOVE THIS LATER)
#find body name and other shiiiiiii

#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3

#defining name space and bodys that will be moved
ns = "euclid"
body_name = 'thruster2' 

#--------------------------------keyboard control-------------------------------


if __name__ == '__main__':
    try:
        rospy.init_node('force_publisher', anonymous=True)
    except rospy.ROSInterruptException:
        pass
    try:
        rospy.wait_for_service('/gazebo/apply_body_wrench', timeout=10)
    except rospy.ROSException:
        pass
    try:
        apply_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', ApplyBodyWrench)
    except rospy.ServiceException:
        pass
    force = [0, 200, 0]
    torque = [0, 0, 0]
    rospy.sleep(1)  # Wait for the publisher to initialize

    force_msg = Wrench()
    force_balls = ApplyBodyWrench()
    force_balls.body_name = 'thruster4'
    
    #force_balls.reference_frame = 'euclidworld::chassie'
    
    force_msg.force = Vector3(*force)  # Apply force along x-axis

    rate = rospy.Rate(10)  # 10 Hz

    duration = 1.0
    if rospy.has_param('~duration'):
        duration = rospy.get_param('~duration')

    while not rospy.is_shutdown():
        success = apply_wrench(
            body_name,
            'world',
            Point(0, 0, 0),
            force_msg,
            rospy.Time().now(),
            rospy.Duration(1))
        break
        
    rospy.spin()

    
