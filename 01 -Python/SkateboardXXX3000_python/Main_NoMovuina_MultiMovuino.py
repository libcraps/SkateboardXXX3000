import sys
import time
from threading import Thread
import Movuino as mvn

#####################################################################
####################		MOVUINOS			#####################
#####################################################################

# COMPUTER
computerIP = "150.10.147.70" # set here your computer IP

# MOVUINO MASTER
movuino1IP = "150.10.147.14"  # set here your Movuino master IP once its connected to the same wifi network as your computer
movuino1   = mvn.Movuino(computerIP, movuino1IP, 7400, 7401) # 7400 port out // 7401 port in

# MOVUINO SLAVE
movuino2IP = "150.10.147.15"  # set here your Movuino slave IP once its connected to the same wifi network as your computer
movuino2   = mvn.Movuino(computerIP, movuino2IP, 7500, 7501)

#-----------------------#

def setMovuinosNeopix(mvn1_, mvn2_, red_, green_, blue_):
	mvn1_.setNeoPix(red_, green_, blue_)
	mvn2_.setNeoPix(red_, green_, blue_)

def printMovuinoData(mvn_):
	print("Movuino ID:", mvn_.id)
	print("Accelerometer data:", mvn_.ax, mvn_.ay, mvn_.az)
	print("Gyroscope data:", mvn_.gx, mvn_.gy, mvn_.gz)
	print("Magnetometer data:", mvn_.mx, mvn_.my, mvn_.mz)
	print("---")

#####################################################################
####################		 MAIN				#####################
#####################################################################
def main(args = None):
	movuino1.start() # start thread and OSC communication
	movuino2.start()

	#-----------------------#

	movuino1.vibroNow(True)       # activate vibration on Movuino master
	movuino1.setNeoPix(255,0,0)   # set pixel color on Movuino master
	movuino2.setNeoPix(0,0,255)   # set pixel color on Movuino slave
	time.sleep(0.5)
	movuino1.vibroNow(False)      # turn off vibration on Movuino master

	timer0 = time.time()
	while (time.time()-timer0 < 5):
		printMovuinoData(movuino1)
		printMovuinoData(movuino2)

		red_ = (int)(255.0*(0.07+movuino1.ax)/0.14)     # set red light component
		green_ = (int)(255.0*(0.07+movuino1.ay)/0.14)   # set green
		blue_ = 0                                         # set blue

		setMovuinosNeopix(movuino1, movuino2, red_, green_, blue_)  # set pixel color on both Movuino

		time.sleep(.01) # let quick sleep to avoid overload
	
	movuino1.vibroPulse(150,100,3)                        # make pulsation on Movuino master (vibration time, vibration off, number of pulsation)
	setMovuinosNeopix(movuino1, movuino2, 0,255,0)

	movuino1.lightNow(False) # turn off light on Movuino Master
	time.sleep(0.5)
	movuino1.lightNow(True)  # turn on on last color
	time.sleep(0.5)
	movuino1.lightNow(False)
	movuino2.lightNow(False)

	#-----------------------#

	movuino1.stop() # stop thread and OSC communication
	movuino2.stop()

if __name__ == '__main__':
	sys.exit(main())