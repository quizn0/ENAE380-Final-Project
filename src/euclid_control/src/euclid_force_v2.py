#!/usr/bin/env python3

#Spencer Quizon

import rospy
from gazebo_msgs.srv import ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def shutdown():
    crtl_c = True


#necessary varibles
ns = "euclid"
body_name = 'thruster4' 
body_names = ['thruster1','thruster2','thruster3','thruster4','thruster5','thruster6']
ctrl_c = False
rospy.on_shutdown(shutdown)

if __name__ == '__main__':

    #--------------------------------General Setup-------------------------------------------
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

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

    #defining force parameters
    force = [0, 0, 100]
    force_neg = [0, 0, -100]
    torque = [0, 0, 0]
    rospy.sleep(1)  # Wait for the publisher to initialize

    force_msg = Wrench()
    force_balls = ApplyBodyWrench()
    force_balls.body_name = 'thruster4'
    
    #force_balls.reference_frame = 'euclidworld::chassie'
    
    force_msg.force = Vector3(*force)  # Apply force along x-axis

    rate = rospy.Rate(10)  # 10 Hz

    #time varibles
    duration = 1.0

    #dont need this idk manzz
    if rospy.has_param('~duration'):
        duration = rospy.get_param('~duration')

    print("TESTTTTTTTTTTT")

    while not rospy.is_shutdown():
        key_press = getKey()
        if key_press == "w":
            force_balls.body_name = "thruster5"
            print("this is key press:", key_press)
            success = apply_wrench(
                body_names[4],
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))
            
        if key_press == "s":
            force_balls.body_name = "thruster3"
            print("this is key press:", key_press)
            success = apply_wrench(
                body_names[2],
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))
            
        if key_press == "d":
            force_balls.body_name = "thruster2" #idk
            print("this is key press:", key_press)
            success = apply_wrench(
                body_names[1],
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))

        if key_press == "a":
            force_balls.body_name = "thruster1" #idk
            print("this is key press:", key_press)
            force_msg.force = Vector3(*force) 
            success = apply_wrench(
                body_names[0],
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))
            
        #MOMENTS ARENT BEING GENARATED
        if key_press == "e":
            force_balls.body_name = "thruster5"
            print("this is key press:", key_press)
            force_msg.force = Vector3(*force) 
            success = apply_wrench(
                body_name,
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))
            force_balls.body_name = "thruster3"
            force_msg.force = Vector3(*force) 
            success = apply_wrench(
                body_name,
                'world',
                Point(0, 0, 0),
                force_msg,
                rospy.Time().now(),
                rospy.Duration(1))
                
        if key_press == "q":  
             ctrl_c = True
    
    rospy.spin()

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)