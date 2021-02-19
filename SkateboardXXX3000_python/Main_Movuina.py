import sys
import time
from threading import Thread
import Movuino as mvn
import matplotlib.pyplot as plt
import pandas
# ok ok
#####################################################################
#####################		MOVUINO			#########################
#####################################################################

# COMPUTER
computerIP = "127.0.0.1"  # set local ip adress

# MOVUINO MASTER
movuinoIP = "127.0.0.1"  # set local ip adress
movuino = mvn.Movuino(computerIP, movuinoIP, 7400, 7401)  # port in // port out

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

	tricks = []

	timer0 = time.time()
	plt.figure()
	plt.show()
	while (time.time() - timer0 < 30):

		movuino.dataPrint()	# print incoming data and device id
		if (movuino.xmmGestId == 1 and movuino.xmmGestProg >= 0.9) :
			tricks.append("ollie")
			time.sleep(2)

			#plt.close()
		elif (movuino.xmmGestId == 2 and movuino.xmmGestProg >= 0.9) :
			tricks.append("kickflip")
			time.sleep(2)

		time.sleep(.01)									# let quick sleep to avoid overload
	
	#movuino.vibroPulse(150, 100, 3)						# make pulsation on Movuino master (vibration time, vibration off, number of pulsation)

	#-----------------------#
	#-----------------------#
	#-----------------------#

	movuino.stop() # stop thread and OSC communication

	print(tricks)

if __name__ == '__main__':
	sys.exit(main())