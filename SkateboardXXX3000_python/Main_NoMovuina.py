import sys
import time
from threading import Thread
import Movuino as mvn

#####################################################################
#####################		MOVUINO			#########################
#####################################################################

# COMPUTER
computerIP = "192.168.43.116" # set here your computer IP

# MOVUINO MASTER
movuinoIP = "192.168.43.236"  # set here your Movuino IP once its connected to the same wifi network as your computer
movuino = mvn.Movuino(computerIP, movuinoIP, 7400, 7401) # port in // port out

#####################################################################
####################		 MAIN				#####################
#####################################################################
def main(args = None):
	movuino.start() # start thread and OSC communication
	
	#-----------------------#
	#-----------------------#
	#-----------------------#

	movuino.vibroNow(True)							# activate continuous vibrations on Movuino
	movuino.setNeoPix(255,0,0)						# set pixel color on Movuino to red
	time.sleep(0.5)
	movuino.vibroNow(False)							# turn off vibration on Movuino

	timer0 = time.time()
	while (time.time()-timer0 < 10):
		movuino.dataPrint()								# print incoming data and device id

		red_ = (int)(255.0*(0.07+movuino.ax)/0.14)		# use data to set the red light component
		green_ = (int)(255.0*(0.07+movuino.ay)/0.14)	# set green
		blue_ = 0										# set blue

		movuino.setNeoPix(red_, green_, blue_)			# set pixel color matching with Movuino 3D orientation

		time.sleep(.01)									# let quick sleep to avoid overload
	
	movuino.vibroPulse(150,100,3)						# make pulsation on Movuino master (vibration time, vibration off, number of pulsation)

	movuino.lightNow(False)							# turn OFF light on Movuino
	time.sleep(0.2)
	movuino.lightNow(True)							# turn ON on last color
	time.sleep(0.2)
	movuino.lightNow(False)

	#-----------------------#
	#-----------------------#
	#-----------------------#

	movuino.stop() # stop thread and OSC communication

if __name__ == '__main__':
	sys.exit(main())