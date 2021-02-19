#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"
#include "FS.h"
#include <Yabl.h>

MPU6050 mpu6050;

int16_t ax, ay, az; // store accelerometre values
int16_t gx, gy, gz; // store gyroscope values
int16_t mx, my, mz; // store magneto values
int magRange[] = {666, -666, 666, -666, 666, -666}; // magneto range values for callibration

// Button variables
const int pinBtn = 13;     // the number of the pushbutton pin
Button button;
bool buttonFlash = false;
bool buttonPressed = false;
float startPush;

// LEDs
const int pinLedESP = 2; // wifi led indicator
const int pinLedBat = 0;  // battery led indicator
const int pinLedNeopix = 15;

bool test = false;
float testMillis;

void setup() {
  // pin setup
  //pinMode(pinBtn, INPUT_PULLUP); // pin for the button
  pinMode(pinLedESP, OUTPUT);   // pin for the wifi led
  pinMode(pinLedBat, OUTPUT);    // pin for the battery led
  button.attach(pinBtn, INPUT_PULLUP); // pin configured to pull-up mode
  
  button.callback(onButtonPress, PRESS);
  button.callback(onButtonRelease, RELEASE);
  button.callback(onButtonHold, HOLD | DOUBLE_TAP); // called on either event

  Wire.begin();
  Serial.begin(115200);
  delay(2000);

  // initialize device
  Serial.println("Initializing I2C devices...");
  mpu6050.initialize();
  testMillis = millis();
  createFile("/data/file.txt");
}

void loop() {
  // GET MOVUINO DATA
  mpu6050.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz); // Get all 9 axis data (acc + gyro + magneto)
  //---- OR -----//
  //mpu6050.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // Get only axis from acc & gyr

  magnetometerAutoCallibration();
  button.update();
  if (buttonFlash) {
    Serial.println(startPush);
    
    if (millis()-startPush > 1500){
      digitalWrite(pinLedESP, LOW); // Flash every 80ms
    } else {
      digitalWrite(pinLedESP, millis() % 80 < 40); // Flash every 80ms
    }
  }
  delay(1);
}

float splitFloatDecimal(float f_) {
  int i_ = f_ * 1000;
  return i_ / 1000.0f;
}
