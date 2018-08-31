#!/usr/bin/env python
# Execute as a python script
# Set linear and angular values of Bebop's speed and turning.
import rospy # Needed to create a ROS node
from geometry_msgs.msg import Twist # Message that moves base
from geometry_msgs.msg import Pose # Message that moves base
from std_msgs.msg import *

class windowfollower():
  def __init__(self):
      # ControlBebop is the name of the node sent to the master
      rospy.init_node('control_ventana', anonymous=False)
      self.pubComando = rospy.Publisher('/ventana/vel_bebop_ventana', Twist, queue_size=10)
      #self.pubAterriza = rospy.Publisher('/siguelineas/aterriza', Int8, queue_size=10)
      #self.pubDespega = rospy.Publisher('/siguelineas/despega', Int8, queue_size=10)
      self.msg = Twist()
      self.pubComando.publish(self.msg)
      #self.posicion = Pose()

  def callback(self, posicion):
      #print(posicion)
      ############################################
      pixel_x = posicion.position.x
      pixel_y = posicion.position.y   
      # Called by the main program to set the current command
      # Linear speed in x in meters/second is + (forward) or - (backwards)
      # Linear speed in y in meters/second is + (left) or - (right)
      # Linear speed in z in meters/second is + (ascend) or - (descend)
      # Modify this value to change speed Turn at 0 radians/s is + (rotate counter clockwise) or - (rotate clockwise)
      print(pixel_x)
      print(pixel_y)
      #moviendose a la derecha
      if (pixel_x >= 1 and pixel_x <= 220) :
          vel_adelante = 0.0     # La velocidad de vuelo es constante
          desplazamiento = -0.1     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido = 0
      #moviendose adelante
      elif (pixel_x > 220 and pixel_x <= 420) :
          vel_adelante = 0.1     # La velocidad de vuelo es constante
          desplazamiento = 0     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido =  0
      #moviendose a la izquierda
      elif (pixel_x > 421 and pixel_x <=640) :
          vel_adelante = 0     # La velocidad de vuelo es constante
          desplazamiento = 0.1     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido = 0
      else:
          vel_adelante = 0     # La velocidad de vuelo es constante
          desplazamiento = 0.5     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido = 0

      self.msg.linear.x = vel_adelante
      self.msg.linear.y = desplazamiento
      self.msg.linear.z = altura
      self.msg.angular.z = theta_corregido
      self.pubComando.publish(self.msg)
      rospy.loginfo("Mandando los valores del control")

  def stop(self,paro):
      # rospy.Subscriber("/ProgramaMike/stop", Int8, paro)
      rospy.loginfo(paro.data)
      self.pubAterriza.publish(1)
      rospy.loginfo("Aterrizando")

  def inicia(self,vuelo):
      # rospy.Subscriber("/ProgramaMike/vuelo", Int8, vuelo)
      rospy.loginfo(vuelo.data)
      self.pubDespega.publish(1)
      rospy.loginfo("Mandando a volar")


def listener(bebop):
    #rospy.init_node('listener_line')
    rospy.Subscriber("/publish_ventana", Pose, bebop.callback)
    #rospy.Subscriber("/ProgramaMike/vuelo", Int8, bebop.inicia)
    #rospy.Subscriber("/ProgramaMike/paro", Int8, bebop.stop)
    # Allow the controller to publish to the /cmd_vel topic and thus control the drone Setup regular publishing of control packets
    rospy.spin()


if __name__ == '__main__':
  print('inicia codigo')
  #try:
  print('dentro del try')
  #windowfollower()
  bebop = windowfollower()
  #rospy.init_node('listener_line')
  rospy.Subscriber("/publish_ventana", Pose, windowfollower().callback)
  #listener(bebop)
  rospy.spin()

  #except:
  #   rospy.loginfo("End of the trip for Bebop")
