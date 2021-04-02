void print9axesDataMPU(MPU9250 IMU){
  // display the data
  Serial.print(IMU.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelZ_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroX_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroY_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroZ_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getMagX_uT(),6);
  Serial.print("\t");
  Serial.println(IMU.getMagY_uT(),6);
}

void printTempDataMPU(MPU9250 IMU){
    Serial.println(IMU.getTemperature_C(),6);
}

void get9axesDataMPU(MPU9250 IMU, float* ax, float* ay, float* az, float* gx, float* gy, float* gz, float* mx, float* my, float* mz){
    //Accel
    *ax = IMU.getAccelX_mss();
    *ay = IMU.getAccelY_mss();
    *az = IMU.getAccelZ_mss();
    //Gyro
    *gx = IMU.getGyroX_rads();
    *gy = IMU.getGyroY_rads();
    *gz = IMU.getGyroZ_rads();
    //Mag
    *mx = IMU.getMagX_uT();
    *my = IMU.getMagY_uT();
    *mz = IMU.getMagZ_uT();
}


void getTempDataMPU(MPU9250 IMU){
  
}
