#!/usr/bin/env python
import rospy
from rrbot_control_me495.msg import RRBotConfig
import numpy as np
from math import atan2,pow,sqrt
from std_msgs.msg import Header
import tf

def move():
    rospy.init_node('circle_swing')
    joint_publisher = rospy.Publisher('/rrbot_joint_position_control/rrbot_ref_joint_config', RRBotConfig, queue_size=10)
    State = RRBotConfig()
    t1 = rospy.Time.now().to_sec()
    T= rospy.get_param('~time', default=5)
    r= rospy.get_param('~pub_rate', default=50)
    rate=rospy.Rate(r)

    while not rospy.is_shutdown():
        t2=rospy.Time.now().to_sec()
        t=t2-t1
        x = 0.5*np.cos(2*np.pi*t/T) +1.25
        y = 0.5*np.sin(2*np.pi*t/T)
        alpha = np.arccos(sqrt(x**2 + y**2)/2)
        beta = np.arccos((2-x**2 - y**2)/2)
        ang1 = atan2(y,x) - alpha
        ang2 = np.pi - beta
        State.j1= ang1
        State.j2= ang2
        joint_publisher.publish(State)
        rate.sleep()

    
if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass