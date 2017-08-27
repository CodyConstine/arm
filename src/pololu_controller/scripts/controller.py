#!/usr/bin/env python
import termios, fcntl, sys, os
import contextlib
import rospy
import math
import time
from pololu_controller.msg import MotorCommand
# from std_msgs.msg import Float64MultiArray
import struct
import roslib
import binascii
roslib.load_manifest("rosparam")
import rosparam
import serial
#key stroke interrupt

# * Front: 0
# * front_right: 6
# * front_left: 2
# * back_right: 3
# * back_left: 5
# * back: 4
# * left: 9
# * right: 8

class Controller():
    def __init__(self):


        f = rospy.get_param("/controller/arm_yaml/")
        paramlist=rosparam.load_file(f,default_namespace="motors")
        for params, ns in paramlist:
            rosparam.upload_params(ns,params)
        port = rospy.get_param("/controller/port_name/")
        baud = rospy.get_param("/controller/baud_rate/")
        self.port = serial.Serial(port, baud, timeout=0.5)
        self.port.flush()
        self.sub = rospy.Subscriber('pololu/command', MotorCommand, self.command_callback, queue_size=40)

    def command_callback(self,msg):
        pin = rospy.get_param('/motors/'+msg.joint_name+'/motor_id')
        min_pwn = rospy.get_param('/motors/'+msg.joint_name+'/min')
        max_pwn = rospy.get_param('/motors/'+msg.joint_name+'/max')
        if(msg.position < min_pwn):
            msg.position = min_pwn
        if(msg.position > max_pwn):
            msg.position = max_pwn
        pwn = msg.position * 4
        # print(pin)
        pwn = int(pwn)
        serialBytes = [
        0x84,
        pin,
        pwn & 0x7F,
        (pwn >> 7) & 0x7F
        ]
        #print serialBytes
        self.port.write(serialBytes)
        binary_string = binascii.unhexlify(b'A1')
        self.port.write(binary_string)
        self.port.flush()
        if(self.port.in_waiting > 0):
            s = self.port.read(2)
            out = struct.unpack('<H',s)
            # print(out)

m = Controller()
def signal_handler(singnal, frame):
    print("\nprogram exited gracefully")
    sys.exit(0)
def main():
    rospy.init_node('Controller')

    rospy.spin()


if __name__ == "__main__":
    main()
