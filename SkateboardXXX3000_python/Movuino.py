import OSC
import sys
import threading
from threading import Thread
import time
import socket, traceback


#####################################################################
######################       OSC CLIENT       #######################
#####################################################################
class OSCclient():
    def __init__(self, ip, port):
        # Initialize OSC communication (to send message)
        self.isSendingOSC = False
        self.c = OSC.OSCClient()
        self.c.connect((ip, port))
        print("OSC Client defined on ip", ip, "through port", port)

    def sendOSCMessage(self, address, *message):
        try:
            # Send message to client through OSC
            oscmsg = OSC.OSCMessage()
            oscmsg.setAddress("/" + address)
            for m_ in message:
                oscmsg.append(message)
            self.c.send(oscmsg)
        # print "Sent message : ", message, " at ", address
        finally:
            print("No receiver")

    def closeClient(self):
        self.c.close()


#####################################################################
######################       OSC SERVER       #######################
#####################################################################
class OSCserver():
    def __init__(self, ip, port):
        self.receive_address = (ip, port)
        self.s = OSC.ThreadingOSCServer(self.receive_address)
        self.s.addDefaultHandlers()  # this registers a 'default' handler (for unmatched messages)
        self.st = threading.Thread(target=self.s.serve_forever)
        self.st.start()

        # Initialize variables
        self.curAddr = "No OSC address"  # It can take the value of "movuino", "streamo", "gesture", "repetions"
        self.curMess = "No OSC message"

        print("Starting OSCServer")

    # define a message-handler function for the server to call.
    def printing_handler(self, addr, tags, stuff, source):
        # Store address and message
        self.curAddr = addr.split("/")[1]  # remove part we don't care
        self.curMess = stuff

    # define address to listen via OSC
    def addListener(self, addr):
        self.s.addMsgHandler("/" + addr, self.printing_handler)
        print("Start listening address:", addr, self.receive_address)

    # Return receive values
    def get_CurrentMessage(self):
        return self.curAddr, self.curMess

    def closeServer(self):
        self.s.close()
        self.st.join()
        print ("OSC server close")


#####################################################################
#######################       MOVUINO       #########################
#####################################################################
class Movuino(Thread):
    def __init__(self, computerIP_, movuinoIP_, portIn_, portOut_):
        self.listenOSCAdr1 = 'movuino'
        self.listenOSCAdr2 = 'streamo'
        self.device = 'unknown'
        self.id = 'unknown'

        # Motion sensors data
        self.ax = 0.0  # acceleration X
        self.ay = 0.0  # Y
        self.az = 0.0  # Z
        self.gx = 0.0  # gyroscope X
        self.gy = 0.0
        self.gz = 0.0
        self.mx = 0.0  # magnetometer X
        self.my = 0.0
        self.mz = 0.0

        self.repAcc = False
        self.repGyr = False
        self.repMag = False
        self.xmmGestId = 0
        self.xmmGestProg = 0.0

        # Light
        self.red = 0
        self.green = 0
        self.blue = 0

        #############   SERVER   #############
        # Start OSCServer
        self.osc_server = OSCserver(computerIP_, portIn_)  # Init server communication on specific Ip and port
        self.osc_server.addListener(self.listenOSCAdr1)  # add listener
        self.osc_server.addListener(self.listenOSCAdr2)  # add listener
        self.osc_server.addListener('gesture')
        self.osc_server.addListener('repetitions')

        #############   CLIENT   #############
        self.osc_client = OSCclient(movuinoIP_, portOut_)  # Init client communication on specific Ip and port
        ######################################
        self.isMovuinoRunning = True
        self.thrd = Thread.__init__(self)

    def run(self):
        while self.isMovuinoRunning:
            curAddr, curVal = self.osc_server.get_CurrentMessage()  # extract address and values of current message
            if curAddr == self.listenOSCAdr1 or curAddr == self.listenOSCAdr2:
                if curAddr == self.listenOSCAdr1:
                    self.device = "Movuino"
                else:
                    self.device = "Streamo"
                self.id = curVal[0]
                self.ax = curVal[1]
                self.ay = curVal[2]
                self.az = curVal[3]
                self.gx = curVal[4]
                self.gy = curVal[5]
                self.gz = curVal[6]
                self.mx = curVal[7]
                self.my = curVal[8]
                self.mz = curVal[9]

            if curAddr == "gesture":
                self.xmmGestId = int(curVal[0])
                self.xmmGestProg = float(curVal[1])


            time.sleep(0.01)

    def stop(self):
        self.isMovuinoRunning = False
        time.sleep(.5)
        self.osc_server.closeServer()  # ERROR MESSAGE but close the OSC server without killing the app
        self.osc_client.closeClient()

    # self.thrd.join()

    def dataPrint(self):
        print ("")
        print (self.device, "ID:", self.id)
        print ("Accelerometer data:", self.ax, self.ay, self.az)
        print ("Gyroscope data:", self.gx, self.gy, self.gz)
        print ("Magnetometer data:", self.mx, self.my, self.mz)
        # print("Repetitions:", self.repAcc, self.repGyr, self.repMag)
        print("Gesture recognition:", self.xmmGestId, self.xmmGestProg)
        print ("--------------------------------------")

    def vibroNow(self, isVib):
        if isVib:
            self.osc_client.sendOSCMessage('vibro/now',1)  # send value True to address "/vibroNow" on IP 127.0.0.1 port 3011
        else:
            self.osc_client.sendOSCMessage('vibro/now',0)  # send value False to address "/vibroNow" on IP 127.0.0.1 port 3011

    def vibroPulse(self, on_, off_, rep_):
        self.osc_client.sendOSCMessage('vibro/pulse', on_, off_, rep_)

    def setNeoPix(self, red_, green_, blue_):
        self.osc_client.sendOSCMessage('neopix', red_, green_, blue_)

        if (red_ != 0 or green_ != 0 or blue_ != 0):
            self.red = red_
            self.green = green_
            self.blue = blue_

    def lightNow(self, isLit_):
        if (isLit_):
            self.setNeoPix(self.red, self.green, self.blue)
        else:
            self.setNeoPix(0, 0, 0)
