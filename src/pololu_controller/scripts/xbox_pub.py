#!/usr/bin/env python

import rospy
import xbox
# from std_msgs.msg import Float32MultiArray
from pololu_controller.msg import MotorCommand


def talker():
    pub = rospy.Publisher('pololu/command', MotorCommand, queue_size=10)

    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(40) # 10hz
    a = MotorCommand()
    a.speed = 0
    a.acceleration = 0
    base_rot = 1500
    base_joint = 1500
    middle_joint = 1500
    wrist_joint = 1500
    wrist_rot = 1500
    gripper = 1500
    while not rospy.is_shutdown():
        if(joy.rightTrigger()):
            gripper-=50
        if(joy.leftTrigger()):
            gripper+=50
        a.position = gripper
        a.joint_name = 'gripper'
        pub.publish(a)

        if(joy.leftX() > .75):
            base_rot+=10
        if(joy.leftX() < -.75):
            base_rot-=10
        a.position = base_rot
        a.joint_name = 'base_rot'
        pub.publish(a)

        if(joy.leftY() > .75):
            base_joint+=10
        if(joy.leftY() < -.75):
            base_joint-=10
        # print(base_joint)
        a.position = base_joint
        a.joint_name = 'bottom_joint_1'
        pub.publish(a)
        a.joint_name = 'bottom_joint_2'
        pub.publish(a)

        if(joy.rightY() > .75):
            middle_joint+=10
        if(joy.rightY() < -.75):
            middle_joint-=10
        # print(base_joint)
        a.position = middle_joint
        a.joint_name = 'middle_joint'
        pub.publish(a)


        if(joy.dpadUp()):
            wrist_joint-=10
        if(joy.dpadDown()):
            wrist_joint+=10
        a.position = wrist_joint
        a.joint_name = 'wrist_joint'
        pub.publish(a)
        if(joy.dpadLeft()):
            wrist_rot-=10
        if(joy.dpadRight()):
            wrist_rot+=10
        a.position = wrist_rot
        a.joint_name = 'wrist_rot'
        pub.publish(a)

        rate.sleep()
    joy.close()


if __name__ == '__main__':
    try:
        joy = xbox.Joystick()
        talker()
    except rospy.ROSInterruptException:
        pass
