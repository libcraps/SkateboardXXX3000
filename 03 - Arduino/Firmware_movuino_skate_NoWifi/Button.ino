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
  buttonHold = false;
  buttonPressed = false;
  startPush = 0;
}

void onButtonHold() {
  buttonHold = true;
}

void onButtondoubleTap(){
  doubleTap = true;
}
