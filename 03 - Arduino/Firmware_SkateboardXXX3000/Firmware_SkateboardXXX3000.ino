/*
 * Main program of the firmware of the movuino.
 * This firmware allows us to store data in the Spiffs and to get it after
 * Utilisation :
 * Double tap a first time the button to record a new session and double tap a second time to stop the record
 * 
 * https://arduino.esp8266.com/stable/package_esp8266com_index.json
 * 
 */

#include "Wire.h"
#include "I2Cdev.h"
#include "MPU9250.h"
#include "FS.h"
#include <Adafruit_NeoPixel.h>
#include <Yabl.h>

//Command for serial messages
#define  CMD_FORMAT_SPIFFS 'f' //Format the spiffs
#define  CMD_CREATE_FILE   'c' //Create a new file in the spiffs
#define  CMD_READ_FILE     'r' //Read the file
#define  CMD_ADD_LINE      'a' //Add a ne line in the spiffs (usefull for debugging)
#define  CMD_STOP_RECORD   's' //Stop the record
#define  CMD_LISTING_DIR   'l' //List files in the directory

#define MPU_I2C_ADDRESS 0x69

// SENSOR
MPU9250 IMU(Wire, MPU_I2C_ADDRESS);
int status;

float time, startTime;
float ax, ay, az; // store accelerometre values
float gx, gy, gz; // store gyroscope values
float mx, my, mz; // store magneto values
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

//NEO PIXEL
Adafruit_NeoPixel pixel(1, pinLedNeopix, NEO_GRB + NEO_KHZ800);
uint32_t Red = pixel.Color(255,0,0);
uint32_t Blue = pixel.Color(0,0,255);
uint32_t Green = pixel.Color(0,255,0);

//FILE
File file;
String dirPath = "/data";
String filePath = "/data/file2.txt";
String sep = ",";
String serialMessage;
bool isEditable = false;
bool isReadable = false;
bool formatted;


void setup() {
  // pin setup
  //pinMode(pinBtn, INPUT_PULLUP); // pin for the button
  pinMode(pinLedESP, OUTPUT);   // pin for the wifi led
  pinMode(pinLedBat, OUTPUT);    // pin for the battery led
  button.attach(pinBtn, INPUT_PULLUP); // pin configured to pull-up mode

  //NEOPIXEL setup
  pixel.begin();
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
  status = IMU.begin();
  
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
}

void loop() {
  
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
      case CMD_CREATE_FILE: //Create a new file and replace the previous one
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
      case 'b': //Light tests
        Serial.println("ligth");
        break;
      default:
        Serial.println("No command associated");
        break;
    }
  }

  //---------- Creating File -----------
  if (doubleTap)
  {
    Serial.print(isEditable);
    doubleTap = false;
    if(isEditable == false)
    {
      blink3Times();
      isEditable = true;
      startTime = millis();
      
      Serial.println("Writing in " + filePath);
      if (SPIFFS.exists(filePath))
      {
        file = SPIFFS.open(filePath, "a");     
        file.println("-----------------   NEW RECORD   ---------------------");
        initialiseFileMovuinoData(file, sep);
        file.close();
      } 
      else 
      {
        
        createFile(filePath);
      }

    } 
    else 
    {
      Serial.println();
      
      Serial.println("Stopping the continue edition of " + filePath);
      isEditable = false;
      blinkLongTimes();
      
    }
  }


    // GET MOVUINO DATA
  IMU.readSensor();
  //print9axesDataMPU(IMU);
  get9axesDataMPU(IMU, &ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
  time = millis() - startTime;
  
  //------- Writing in File ------------
  if (isEditable)
  {
    writeData(filePath);
  }
  
  if (isReadable)
  {
    Serial.println();
    Serial.println("reading " + filePath + "...");
    readFile(filePath);
    
    isReadable = false;
  }

  if (buttonFlash) 
  {
    if(millis()-startPush > 2500) //If the button is pressed more than 2.5sec
    {
      isReadable = true;
      digitalWrite(pinLedESP, HIGH);
      startPush = millis()+10000;
      delay(250);
    }
    else
    {
      digitalWrite(pinLedESP, millis() % 80 < 40); // Flash every 80ms
    }
  }

  delay(25);
}

void blink3Times()
{
  //USed when the record start
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
  delay(250);
  digitalWrite(pinLedESP, HIGH);
  delay(250);
  digitalWrite(pinLedESP, LOW);
}
void blinkLongTimes()
{
  //Used when the record stop
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
  delay(500);
  digitalWrite(pinLedESP, HIGH);
  delay(1000);
  digitalWrite(pinLedESP, LOW);
}


float splitFloatDecimal(float f_) {
  int i_ = f_ * 1000;
  return i_ / 1000.0f;
}
