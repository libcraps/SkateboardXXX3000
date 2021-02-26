void createFile(String filepath) {
    
  bool success = SPIFFS.begin();
 
  if (success) {
    Serial.println("File system mounted with success");
  } else {
    Serial.println("Error mounting the file system");
  }
 
  File file = SPIFFS.open(filepath, "w");
 
  if (!file) {
    Serial.println("Error opening file for writing");
    return;
  }
  
  file.println("TEST SPIFFS REDING and wrintng");
  
  initialiseFileMovuinoData(file);
}

void readFile(String filepath){
  
  File file = SPIFFS.open(filepath, "r");
  
  if (!file) {
    Serial.println("Error opening file for reading");
    return;
  }

  while(file.available()){
    Serial.write(file.read());
  }
}

void writeData(String filePath){
  
  file = SPIFFS.open(filePath, "a");
  if (!file) 
  {
    Serial.println("Error opening file for writing");
    return;
  }
  writeInFileMovuinoData(file);
  file.close();
}
