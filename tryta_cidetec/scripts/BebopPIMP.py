#!/usr/bin/env python
# Execute as a python script
# Set linear and angular values of Bebop's speed and turning.
import rospy # Needed to create a ROS node
from geometry_msgs.msg import Twist # Message that moves base
from std_msgs.msg import *

class ControlBebop():
  def __init__(self):
     # ControlBebop is the name of the node sent to the master
     rospy.init_node('ControlBebop', anonymous=False)
     # Message to screen
     rospy.loginfo(" Press CTRL+c to stop ControlBebop")
     # Keys CNTL + c will stop script
     rospy.on_shutdown(self.shutdown)
     # Publisher will send Twist message on topic bebop/takeoff ----------------------(Despega el drone)
     self.cmd_takeoff = rospy.Publisher('bebop/takeoff',Empty, queue_size=1000)
     # Publisher will send Twist message on topic bebop/land    ----------------------(Aterriza el drone)
     self.cmd_land = rospy.Publisher('bebop/land',Empty, queue_size=1000)
     # Publisher will send Twist message on topic bebop/reset   ----------------------(Resetea el drone)
     self.cmd_reset = rospy.Publisher('bebop/reset',Empty, queue_size=1000)
     # Publisher will send Twist message on topic bebop/cmd_vel ----------------------(Hace mover el drone)
     self.cmd_vel = rospy.Publisher('bebop/cmd_vel',Twist, queue_size=1000)
     # Bebop will receive the message 10 times per second.
     self.rate = rospy.Rate(10);
     # 10 Hz is fine as long as the processing does not exceed
     # 1/10 second.
     # Twist is geometry_msgs for linear and angular velocity
     self.move_cmd = Twist()
     # Modify this value to cause rotation rad/s  # Loop and TurtleBot will move until you type CNTL+c
     rospy.loginfo("Lista la configuracion inicial de Bebop")

  def SendDespega(self):
     # Send a takeoff message to the bebop driver Note we only send a takeoff message if the drone is landed - an unexpected takeoff is not good!
     # if(self.status == DroneStatus.Landed):
     self.cmd_takeoff.publish(Empty())

  def SendAterriza(self):
     # Send a landing message to the bebop driver Note we send this in all states, landing can do no harm
     self.cmd_land.publish(Empty())

  def SendEmergencia(self):
     # Send an emergency (or reset) message to the bebop driver
     self.cmd_reset.publish(Empty())

  def shutdown(self):
     # You can stop bebop by publishing an empty Twist message
     rospy.loginfo("Stopping bebop")
     self.cmd_vel.publish(Twist())
     # Give Bebop time to stop
     rospy.sleep(3)
     rospy.loginfo("Mandamos a aterrizar")
     # You can land bebop by publishing an empty Twist message
     self.cmd_land.publish(Empty())
     # Give Bebop time to land
     rospy.sleep(5)

  def SetCommandPilot(self,xspeed,yspeed,zspeed,yaw):
     # Called by the main program to set the current command
     # Linear speed in x in meters/second is + (forward) or - (backwards)
     # Linear speed in y in meters/second is + (left) or - (right)
     # Linear speed in z in meters/second is + (ascend) or - (descend)
     # Modify this value to change speed Turn at 0 radians/s is + (rotate counter clockwise) or - (rotate clockwise)
     self.move_cmd.linear.x  = xspeed
     self.move_cmd.linear.y  = yspeed
     self.move_cmd.linear.z  = zspeed
     self.move_cmd.angular.z = yaw
     self.cmd_vel.publish(self.command)

  def callback(self, cmd):
     rospy.loginfo("Received a /cmd_vel message!")
     rospy.loginfo(cmd)
     drone.SetCommandPilot(cmd.linear.x, cmd.linear.y, cmd.linear.z,cmd.angular.z)

  def Despega(self, toff):
     # rospy.Subscriber("/siguelineas/despega", Int8, despega)
     # rospy.loginfo(toff.data)
     # if toff.data== True:
     if toff.data == 1:
         drone.SendDespega()
         rospy.loginfo("Se manda a volar al Bebop")

  def Aterriza(self, ld):
     # rospy.Subscriber("/siguelineas/aterriza", Int8, paro)
     # rospy.loginfo(ld.data)
     # if ld.data== True:
     if ld.data == 1:
         drone.SendAterriza()
         rospy.loginfo("Aterrizando al Bebop")
 
if __name__ == '__main__':
  #try:
    drone = ControlBebop()
    rospy.Subscriber("/ventana/vel_bebop_ventana", Twist, drone.callback)
    rospy.spin()
 # except:
 #    rospy.loginfo("End of the trip for Bebop")
