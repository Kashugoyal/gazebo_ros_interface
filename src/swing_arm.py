#!/usr/bin/env python

import sys
from gazebo_msgs.srv import ApplyJointEffort
import rospy


def move():
	rospy.init_node('swing')
	value = ApplyJointEffort()
	count=0
	while not rospy.is_shutdown():
		
		value.joint_name = 'joint1'
		
		if count%2 == 0:
			value.effort = 10
			value.start_time = rospy.Time(0)
			value.duration = rospy.Time(1)
		else:
			value.effort = 0
			value.start_time = rospy.Time(0)
			value.duration = rospy.Time(1)
		rospy.wait_for_service('/gazebo/apply_joint_effort')
		JointEffort=rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
		resp1=JointEffort('joint1',value.effort,value.start_time,value.duration)
		rospy.sleep(2.5)
		#count +=1
	
	



if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass
    print "Moving the arm"
