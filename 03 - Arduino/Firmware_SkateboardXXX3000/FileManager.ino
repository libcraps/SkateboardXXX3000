/*
 * Functions that allows us to manage files in the firmware
 */

void createFile(String filepath)
{
  File file = SPIFFS.open(filepath, "w");
 
  if (!file) {
    Serial.println("Error opening file for writing");
    return;
  }
  initialiseFileMovuinoData(file, sep);
  file.close();
}

void readFile(String filepath)
{
  
  File file = SPIFFS.open(filepath, "r");
  
  if (!file) {
    Serial.println("Error opening file for reading");
    return;
  }
  Serial.println("XXX_beginning");
  while(file.available()){
    Serial.write(file.read());
  }
  file.close();
  Serial.println("XXX_end");
}

void writeData(String filePath)
{
  
  file = SPIFFS.open(filePath, "a");
  
  if (!file) 
  {
    Serial.println();
    Serial.println("Error opening file for writing");
    return;
  }
  
  digitalWrite(pinLedBat, HIGH);
  writeInFileMovuinoData(file, sep);
  file.close();
}

void listingDir(String dirPath)
{
  Serial.println("Listing dir :");
  Dir dir = SPIFFS.openDir(dirPath);
  while (dir.next()) 
  {
    Serial.print(dir.fileName());
    File f = dir.openFile("r");
    Serial.print(" ");
    Serial.println(f.size());
    f.close();
  }
  Serial.println("End of listing");
}

void formatingSPIFFS(){
  bool formatted = SPIFFS.format();
  if(formatted)
  {
    Serial.println("\n\nSuccess formatting");
  }
  else
  {
    Serial.println("\n\nError formatting");
  }
}
