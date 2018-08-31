#!/usr/bin/env python

import rospy
from fases_tryta import *
from std_msgs.msg import Int32

def talker():
    pub = rospy.Publisher('fase', Int32, queue_size=10)
    rospy.init_node('racer', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    flight_altitude = 1 

    fase_actual = Fases.DISARMED.value

    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)

        if fase_actual == Fases.DISARMED.value:
            #armar
            fase_actual = Fases.ARMING.value
        if fase_actual == Fases.ARMING.value
            #camara abajo
            #despegar
            fase_actual = Fases.TAKING_OFF.value
                            
        if fase_actual = Fases.TAKING_OFF.value:
            # Si la altura es adecuada
            if( > flight_altitude)
                fase_actual = Fases.HOVERING.value

        if fase_actual = Fases.HOVERING.value:
            #aterrizar

        pub.publish(fase_actual)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
