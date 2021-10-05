# Firmware for movuino esp8266 

This firmware works 'offline', which means that you have no wifi and no bluetooth (not available on movuino esp8266)

## Utilisation

- Press the button to turn on the movuino

- Press 2 times to launch a record, it should blink 3 times
- Press again 2 times to stop it, it should also blink 3 times but slower
(It is possible to do it again it won't delete previouses records and it'll show it the export file the separation)

- When the movuino is connected to your computer on a serial port, press the button a long time to export the file
(you can use the python file associated)

## Export file :

When you extract the file in the serial the movuino sens 'XXX_begin' to say that the extraction starts and it sends 'XXX_end' to say that its over.
The file you'll recieve whill be like so :

time,ax,ay,az,gx,gy,gz,mx,my,mz
dat,dat,dat,dat,dat,dat,...
dat,dat,dat,dat,dat,dat,...
dat,dat,dat,dat,dat,dat,...
...
---------------- NEW RECORD -------------------------
time,ax,ay,az,gx,gy,gz,mx,my,mz
newDat,newDat,newDat,newDat,...
newDat,newDat,newDat,newDat,...
newDat,newDat,newDat,newDat,...
...

## Librairies

- Wire
- I2Cdev
- MPU9250
- FS
- Adafruit_NeoPixel 
- Yabl