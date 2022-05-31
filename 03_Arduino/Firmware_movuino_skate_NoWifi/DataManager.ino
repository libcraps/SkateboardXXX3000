void printMovuinoData() 
{
  /*
   * Print 9 axes data from the movuino
   */
  Serial.print(time/1000);
  Serial.print("\t ");
  Serial.print(-ax);
  Serial.print("\t ");
  Serial.print(ay);
  Serial.print("\t ");
  Serial.print(az);
  Serial.print("\t ");
  Serial.print(gx);
  Serial.print("\t ");
  Serial.print(-gy);
  Serial.print("\t ");
  Serial.print(-gz);
  Serial.println();
}
void writeInFileMovuinoData(File file, String sep) {
  file.print(time/1000);
  file.print(sep);
  file.print(-ax);
  file.print(sep);
  file.print(ay);
  file.print(sep);
  file.print(az);
  file.print(sep);
  file.print(gx);
  file.print(sep);
  file.print(-gy);
  file.print(sep);
  file.print(-gz);
  file.println();
}
void initialiseFileMovuinoData(File file, String sep) {
  file.print("time");
  file.print(sep);
  file.print("ax");
  file.print(sep);
  file.print("ay");
  file.print(sep);
  file.print("az");
  file.print(sep);
  file.print("gx");
  file.print(sep);
  file.print("gy");
  file.print(sep);
  file.print("gz");
  file.println();
}
