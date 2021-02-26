void createFile(String filepath)
{
  File file = SPIFFS.open(filepath, "w");
 
  if (!file) {
    Serial.println("Error opening file for writing");
    return;
  }
  
  file.println("TEST SPIFFS REDING and wrintng");
  
  initialiseFileMovuinoData(file);
  file.close();
}

void readFile(String filepath)
{
  
  File file = SPIFFS.open(filepath, "r");
  
  if (!file) {
    Serial.println("Error opening file for reading");
    return;
  }

  while(file.available()){
    Serial.write(file.read());
  }
  file.close();
}

void writeData(String filePath)
{
  
  file = SPIFFS.open(filePath, "a");
  if (!file) 
  {
    Serial.println("Error opening file for writing");
    return;
  }
  writeInFileMovuinoData(file);
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
