/*
 * Main program of the firmware of the movuino.
 * This firmware allows us to store data in the Spiffs and to get it after
 * 
 */

#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"
#include "FS.h"
#include <Yabl.h>

//Command for serial messages
#define  CMD_FORMAT_SPIFFS 'f' //Format the spiffs
#define  CMD_CREATE_FILE   'c' //Create a new file in the spiffs
#define  CMD_READ_FILE     'r' //Read the file
#define  CMD_ADD_LINE      'a' //Add a ne line in the spiffs (usefull for debugging)
#define  CMD_STOP_RECORD   's' //Stop the record
#define  CMD_LISTING_DIR   'l' //List files in the directory

// SENSOR
MPU6050 mpu6050;

int16_t ax, ay, az; // store accelerometre values
int16_t gx, gy, gz; // store gyroscope values
int16_t mx, my, mz; // store magneto values
int magRange[] = {666, -666, 666, -666, 666, -666}; // magneto range values for callibration

// BUTTON
Button button;
const int pinBtn = 13;     // the number of the pushbutton pin
bool buttonFlash = false;
bool buttonPressed = false;
bool doubleTap = false;
float startPush;

// LEDs
const int pinLedESP = 2; // wifi led indicator
const int pinLedBat = 0;  // battery led indicator
const int pinLedNeopix = 15;

//FILE
File file;
String dirPath = "/data";
String filePath = "/data/file2.txt";
String serialMessage;
bool isEditable = false;
bool formatted;


void setup() {
  // pin setup
  //pinMode(pinBtn, INPUT_PULLUP); // pin for the button
  pinMode(pinLedESP, OUTPUT);   // pin for the wifi led
  pinMode(pinLedBat, OUTPUT);    // pin for the battery led
  button.attach(pinBtn, INPUT_PULLUP); // pin configured to pull-up mode

  //Button - function that we will use
  button.callback(onButtonPress, PRESS);
  button.callback(onButtonRelease, RELEASE);
  button.callback(onButtonHold, HOLD); // called on either event
  button.callback(onButtondoubleTap, DOUBLE_TAP);
  
  Wire.begin();
  Serial.begin(115200);
  delay(2000);
  
  SPIFFS.begin();
  
  // initialize device
  Serial.println("Initializing I2C devices...");
  mpu6050.initialize();
}

void loop() {
  // GET MOVUINO DATA
  mpu6050.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz); // Get all 9 axis data (acc + gyro + magneto)
  //---- OR -----//
  //mpu6050.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // Get only axis from acc & gyr
  magnetometerAutoCallibration();

  button.update();

  //------ Read serial Monitor -----------
  if (Serial.available()>0)
  {
    char serialMessage = Serial.read();
    Serial.print("\n");
    Serial.print("Message received : ");
    Serial.println(serialMessage);  

    //----- Serial command ----
    switch (serialMessage)
    {
      case CMD_FORMAT_SPIFFS:
        Serial.println("Formating the SPIFFS (data files)...");
        formatingSPIFFS();
        break;
      case CMD_CREATE_FILE:
        Serial.println("Creation of  " + filePath);
        createFile(filePath);
        break;
      case CMD_READ_FILE: //Reading File
        Serial.println("reading " + filePath + "...");
        readFile(filePath);
        break;
      case CMD_STOP_RECORD : //Stop the record
        Serial.println("Stopping the edition of " + filePath);
        isEditable = false;
        break;
      case CMD_ADD_LINE:
        Serial.println("Adding a new line to " + filePath);
        writeData(filePath);
        break;
      case CMD_LISTING_DIR:
        listingDir(dirPath);
        break;
      default:
        Serial.println("No command associated");
        break;
    }
  }

  //---------- Creating File -----------
  if (doubleTap)
  {
    if(isEditable == false)
    {
      isEditable = true;
      if (SPIFFS.exists(filePath))
      {
        file = SPIFFS.open(filePath, "a");     
        file.println("-----------------   NEW RECORD   ---------------------");
        initialiseFileMovuinoData(file);
        file.close();
      } 
      else 
      {
        createFile(filePath);
      }

    } 
    else 
    {
      Serial.println("Stopping the continue edition of " + filePath);
      isEditable = false;
    }
  }

  //------- Writing in File ------------
  if (isEditable == true)
  {
    writeData(filePath);
  }

  // DEBUG
  if (buttonFlash) 
  {
    digitalWrite(pinLedESP, millis() % 80 < 40); // Flash every 80ms
  }

  doubleTap = false;
  delay(1);
}

float splitFloatDecimal(float f_) {
  int i_ = f_ * 1000;
  return i_ / 1000.0f;
}
