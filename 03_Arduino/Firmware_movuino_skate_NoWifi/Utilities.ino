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

void blinkNtimes(int N, int delayVar)
{
  static int i = 0;
  static uint32_t prev_ms = millis();

  //USed when the record start
  if (i<=N)
  {
      if (millis() > prev_ms && millis() < prev_ms + delayVar)
      {
          digitalWrite(pinLedESP, LOW);
          Serial.println("LOW");
          
      }
      else 
      {
          digitalWrite(pinLedESP, HIGH);
          Serial.println("HIGH");
          
          if (millis() > prev_ms + 2*delayVar)
          {
            prev_ms = millis(); 
            i++;
          }          
          
      }
  }
}
