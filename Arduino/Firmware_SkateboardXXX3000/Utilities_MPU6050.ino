void printMovuinoData() {
  Serial.print(ax / float(32768));
  Serial.print("\t ");
  Serial.print(ay / float(32768));
  Serial.print("\t ");
  Serial.print(az / float(32768));
  Serial.print("\t ");
  Serial.print(gx / float(32768));
  Serial.print("\t ");
  Serial.print(gy / float(32768));
  Serial.print("\t ");
  Serial.print(gz / float(32768));
  Serial.print("\t ");
  Serial.print(mx);
  Serial.print("\t ");
  Serial.print(my);
  Serial.print("\t ");
  Serial.print(mz);
  Serial.println();
}
void writeInFileMovuinoData(File file) {
  file.print(ax / float(32768));
  file.print("\t ");
  file.print(ay / float(32768));
  file.print("\t ");
  file.print(az / float(32768));
  file.print("\t ");
  file.print(gx / float(32768));
  file.print("\t ");
  file.print(gy / float(32768));
  file.print("\t ");
  file.print(gz / float(32768));
  file.print("\t ");
  file.print(mx);
  file.print("\t ");
  file.print(my);
  file.print("\t ");
  file.print(mz);
  file.println();
}
void initialiseFileMovuinoData(File file) {
  file.print("ax");
  file.print("\t ");
  file.print("ay");
  file.print("\t ");
  file.print("az");
  file.print("\t ");
  file.print("gx");
  file.print("\t ");
  file.print("gy");
  file.print("\t ");
  file.print("gz");
  file.print("\t ");
  file.print("mx");
  file.print("\t ");
  file.print("my");
  file.print("\t ");
  file.print("mz");
  file.println();
}

void magnetometerAutoCallibration() {
  int magVal[] = {mx, my, mz};
  for (int i = 0; i < 3; i++) {
    // Compute magnetometer range
    if (magVal[i] < magRange[2 * i]) {
      magRange[2 * i] = magVal[i]; // update minimum values on each axis
    }
    if (magVal[i] > magRange[2 * i + 1]) {
      magRange[2 * i + 1] = magVal[i]; // update maximum values on each axis
    }

    // Scale magnetometer values
    if (magRange[2 * i] != magRange[2 * i + 1]) {
      magVal[i] = map(magVal[i], magRange[2 * i], magRange[2 * i + 1], -100, 100);
    }
  }

  // Update magnetometer values
  mx = magVal[0];
  my = magVal[1];
  mz = magVal[2];
}
