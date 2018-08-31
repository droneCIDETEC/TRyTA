#!/usr/bin/env python
# Execute as a python script
# Set linear and angular values of Bebop's speed and turning.
import rospy # Needed to create a ROS node
from geometry_msgs.msg import Twist # Message that moves base
from geometry_msgs.msg import Pose # Message that moves base
from std_msgs.msg import *
import time

estado = 0

class windowfollower():
  def __init__(self):
      # ControlBebop is the name of the node sent to the master
      #rospy.init_node('control_ventana', anonymous=False)
      self.pubComando = rospy.Publisher('bebop/cmd_vel', Twist, queue_size=10)
      self.pubAterriza = rospy.Publisher('/ventana/aterriza', Int8, queue_size=10)
      self.pubDespega = rospy.Publisher('/ventana/despega', Int8, queue_size=10)
      self.msg = Twist()
      self.pubComando.publish(self.msg)
      #self.posicion = Pose()

  def callback(self, posicion):
      f_iz= 415
      f_der = 445
      vel_d = 0.015
      global estado 
      ############################################
      pixel_x = posicion.position.x
      pixel_y = posicion.position.y  
      print (pixel_x) 
      # Called by the main program to set the current command
      # Linear speed in x in meters/second is + (forward) or - (backwards)
      # Linear speed in y in meters/second is + (left) or - (right)
      # Linear speed in z in meters/second is + (ascend) or - (descend)
      # Modify this value to change speed Turn at 0 radians/s is + (rotate counter clockwise) or - (rotate clockwise)
      #moviendose a la izquierda
      if (pixel_x >= 1 and pixel_x <= (f_iz -1) and ( estado == 0)) :
          print('izq')
          vel_adelante = 0.0     # La velocidad de vuelo es constante
          desplazamiento = vel_d     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido = 0
      #moviendose adelante
      elif (pixel_x > f_iz and pixel_x <= f_der) :
          print('centro')
          estado = 1
          vel_adelante = 0.1     # La velocidad de vuelo es constante
          desplazamiento = 0     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido =  0
      #moviendose a la derecha
      elif (pixel_x > (f_der + 1) and pixel_x <=840 and ( estado == 0)) :
          print('derecha')
          vel_adelante = 0     # La velocidad de vuelo es constante
          desplazamiento = -vel_d     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
          altura = 0             # La altura no se modificara, sera a la altura de despegue
          theta_corregido = 0
      else:
          print('nada')
          vel_adelante = 0.1     # La velocidad de vuelo es constante
          desplazamiento = 0     # Solo vamos a corregir el angulo de yaw, asi que no presentara desplazamientos en y
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

if __name__ == '__main__':
  
  rospy.init_node('control_ventana', anonymous=False)
  empty = Empty()
  takeoff = rospy.Publisher('bebop/takeoff', Empty, queue_size=10)
  land = rospy.Publisher('bebop/land', Empty, queue_size=10)
  rate = rospy.Rate(10)
  
  # takeoff and land
  takeoff.publish(empty)
  rospy.loginfo("Sleep 1")
  rate.sleep()
  rospy.sleep(1)

  takeoff.publish(empty)
  rospy.loginfo("Sleep 2")
  rate.sleep()
  rospy.sleep(5)
  
  
  #estado = 0
  
  while(1): 
    bebop = windowfollower()
    rospy.Subscriber("/publish_ventana", Pose, windowfollower().callback)
    rospy.spin()

