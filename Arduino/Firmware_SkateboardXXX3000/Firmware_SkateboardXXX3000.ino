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

// LEDs
const int pinLedESP = 2; // wifi led indicator
const int pinLedBat = 0;  // battery led indicator
const int pinLedNeopix = 15;

bool test = false;

void setup() {
  // pin setup
  pinMode(pinBtn, INPUT_PULLUP); // pin for the button
  pinMode(pinLedESP, OUTPUT);   // pin for the wifi led
  pinMode(pinLedBat, OUTPUT);    // pin for the battery led

  Wire.begin();
  Serial.begin(115200);
  delay(2000);

  // initialize device
  Serial.println("Initializing I2C devices...");
  mpu6050.initialize();

  createFile("/data/file.txt");

}

void loop() {
  // GET MOVUINO DATA
  mpu6050.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz); // Get all 9 axis data (acc + gyro + magneto)
  //---- OR -----//
  //mpu6050.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); // Get only axis from acc & gyr

  magnetometerAutoCallibration();

  if (!test && millis() > 5000) {
    Serial.println("ok");
    test =true;
  }
  
  delay(1);
}

float splitFloatDecimal(float f_) {
  int i_ = f_ * 1000;
  return i_ / 1000.0f;
}
