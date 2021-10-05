using System.Collections;
using System.Collections.Generic;
using Device;
using UnityEngine;

namespace Movuino
{
    [System.Serializable]
	public class MovuinoSensor 
	{
        private string movuinoAdress;

        public OSCMovuinoSensorBasicData OSCmovuinoSensorData; //9axes data

        public string MovuinoAdress { get { return movuinoAdress; } }
        public Vector3 InstantAcceleration { get { return OSCmovuinoSensorData.accelerometer; } }
        public Vector3 InstantGyroscope { get { return OSCmovuinoSensorData.gyroscope; } }
        public Vector3 InstantMagnetometer { get { return OSCmovuinoSensorData.magnetometer; } }

        public Vector3 DeltaAccel { get { return Accel - prevAccel;  } }
        public Vector3 DeltaGyr { get { return Gyr - prevGyr;  } }
        public Vector3 DeltaMag { get { return Mag - prevMag;  } }

        public Vector3 AngleOrientation {  get { return GetAngle(); } }


        Vector3 Accel;
        Vector3 Gyr;
        Vector3 Mag;

        Vector3 prevAccel;
        Vector3 prevGyr;
        Vector3 prevMag;

        Vector3 initAngle;
        Vector3 angleOrientation;

        public MovuinoSensor(string adress)
		{
            prevAccel = new Vector3(0, 0, 0);
            prevGyr = new Vector3(0, 0, 0);
            prevMag = new Vector3(0, 0, 0);

            Accel = new Vector3(0, 0, 0);
            Gyr = new Vector3(0, 0, 0);
            Mag = new Vector3(0, 0, 0);

            initAngle = new Vector3(0, 0, 0);
            movuinoAdress = adress;
            OSCmovuinoSensorData = OSCDataHandler.CreateOSCDataHandler<OSCMovuinoSensorBasicData>();
        }


        Vector3 GetAngle()
        {
            angleOrientation = OSCmovuinoSensorData.magnetometer - initAngle;
            return angleOrientation;
        }

        public void InitMovTransform()
        {

            if (Input.GetKeyDown(KeyCode.I))
            {
                initAngle = OSCmovuinoSensorData.magnetometer;
            }
        }

        public void UpdateMovuinoData()
        {
            prevAccel = Accel;
            prevGyr = Gyr;
            prevMag = Mag;

            Accel = InstantAcceleration;
            Gyr = InstantGyroscope;
            Mag = InstantMagnetometer;
        }

    }

}