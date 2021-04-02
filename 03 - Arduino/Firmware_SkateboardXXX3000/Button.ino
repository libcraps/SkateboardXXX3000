/*
 * Function that allows us to handle button
 */

void onButtonPress() {
  digitalWrite(pinLedESP, HIGH);
  buttonPressed = true;
  startPush = millis();
}

void onButtonRelease() {
  digitalWrite(pinLedESP, LOW);
  buttonFlash = false;
  buttonPressed = false;
  startPush = 0;
}

void onButtonHold() {
  buttonFlash = true;
}

void onButtondoubleTap(){
  doubleTap = true;
}
