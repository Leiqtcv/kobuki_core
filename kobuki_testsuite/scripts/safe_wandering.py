#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Yujin Robot
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Yujin Robot nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author: Younghun Ju <yhju@yujinrobot.com> <yhju83@gmail.com>

import roslib; roslib.load_manifest('kobuki_testsuite')
import rospy

from tf.transformations import euler_from_quaternion
from math import degrees, radians

import sys
import random

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from kobuki_comms.msg import BumperEvent, CliffEvent


def wrapToPi(x):
  import numpy as np
  return np.mod(x+np.pi,2*np.pi)-np.pi

def sig(x):
  if x > 0: return +1
  if x < 0: return -1
  return 0

class SafeWandering(object):
  def __init__(self):
    rospy.init_node('safe_wandering')
    rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.BumperEventCallback)
    rospy.Subscriber("/mobile_base/events/cliff", CliffEvent, self.CliffEventCallback)
    rospy.Subscriber("/odom", Odometry, self.OdometryCallback)
    self.pub = rospy.Publisher("/cmd_vel", Twist)
    self.rate = rospy.Rate(50)

    self.ok = True
    self.theta = 0.0
    self.theta_goal = 0.0

  def command(self, twist):
    self.pub.publish(twist)
    self.rate.sleep()
    if rospy.is_shutdown():
      sys.exit()

  def go(self):
    twist = Twist()
    twist.linear.x = 0.18
    while self.ok:
      self.command(twist)

  def stepback(self):
    twist = Twist()
    twist.linear.x = -0.1
    for i in range(0,35): 
      self.command(twist)
 
  def turn(self):
    twist = Twist()
    twist.angular.z = 1.8*sig(wrapToPi(self.theta_goal - self.theta))
    while not self.reached():
      self.command(twist)
    self.ok = True

  def reached(self):
    if abs(wrapToPi(self.theta_goal - self.theta)) < radians(5.0):
      return True
    else:
      return False

  def spin(self):
    while not rospy.is_shutdown():
      self.go()
      self.stepback()
      self.turn()

  def OdometryCallback(self, data):
    quat = data.pose.pose.orientation
    q = [quat.x, quat.y, quat.z, quat.w]
    roll, pitch, yaw = euler_from_quaternion(q)
    self.theta = yaw
  
  def BumperEventCallback(self, data):
    if data.state == BumperEvent.PRESSED:
      self.ok = False
      if   data.bumper == BumperEvent.LEFT:
        self.theta_goal = self.theta - 3.141592*random.uniform(0.2, 1.0)
      elif data.bumper == BumperEvent.RIGHT:
        self.theta_goal = self.theta + 3.141592*random.uniform(0.2, 1.0)
      else:
        self.theta_goal = wrapToPi(self.theta + 3.141592*random.uniform(-1.0, 1.0))

  def CliffEventCallback(self, data):
    if data.state == CliffEvent.CLIFF:
      self.ok = False
      if   data.sensor == CliffEvent.LEFT:
        self.theta_goal = self.theta - 3.141592*random.uniform(0.2, 1.0)
      elif data.sensor == CliffEvent.RIGHT:
        self.theta_goal = self.theta + 3.141592*random.uniform(0.2, 1.0)
      else:
        self.theta_goal = wrapToPi(self.theta + 3.141592*random.uniform(-1.0, 1.0))


if __name__ == '__main__':
  try:
    instance = SafeWandering()
    instance.spin()
  except rospy.ROSInterruptException: pass
 