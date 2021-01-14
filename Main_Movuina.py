import sys
import time
from threading import Thread
import Movuino as mvn

#####################################################################
#####################		MOVUINO			#########################
#####################################################################

# COMPUTER
computerIP = "127.0.0.1" # set local ip adress

# MOVUINO MASTER
movuinoIP = "127.0.0.1"  # set local ip adress
movuino = mvn.Movuino(computerIP, movuinoIP, 3000, 3001) # port in // port out

#####################################################################
####################		 MAIN				#####################
#####################################################################
def main(args = None):
	movuino.start() # start thread and OSC communication
	
	#-----------------------#
	#-----------------------#
	#-----------------------#

	movuino.vibroNow(True) # activate continuous vibrations on Movuino
	time.sleep(0.5)
	movuino.vibroNow(False) # turn off vibration on Movuino

	timer0 = time.time()
	while (time.time()-timer0 < 2):
		movuino.dataPrint()	# print incoming data and device id
		#print movuino.ax # or print individual data from Movuina
		time.sleep(.01)									# let quick sleep to avoid overload
	
	movuino.vibroPulse(150, 100, 3)						# make pulsation on Movuino master (vibration time, vibration off, number of pulsation)

	#-----------------------#
	#-----------------------#
	#-----------------------#

	movuino.stop() # stop thread and OSC communication

if __name__ == '__main__':
	sys.exit(main())