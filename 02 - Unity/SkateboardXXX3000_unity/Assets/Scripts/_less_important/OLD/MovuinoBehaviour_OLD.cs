using System.Collections;
using System.Collections.Generic;
using Device;
using UnityEngine;

namespace Movuino
{
    /// <summary>
    /// Class that manage the movuino object in the scene
    /// </summary>
    /// <remarks>Handle OSC conncetion too</remarks>
    public class MovuinoBehaviour_OLD : MonoBehaviour
    {

        public OSC oscManager;
        private string addressSensorData;

        private MovuinoBehaviour movuino;
        [SerializeField]
        private string movuinoAdress;

        private void Awake()
        {
            //movuino = new MovuinoSensor(movuinoAdress);
            addressSensorData = movuino.movuinoAdress + movuino.OSCmovuinoSensorData.OSCAddress;
        }
        void Start()
        {
            oscManager.SetAddressHandler(movuino.movuinoAdress, movuino.OSCmovuinoSensorData.ToOSCDataHandler);
            //oscManager.SetAllMessageHandler(OSCDataHandler.DebugAllMessage);
        }


        private void FixedUpdate()
        {
            movuino.UpdateMovuinoData();
            //this.gameObject.transform.Rotate(movuino.InstantGyroscope * Time.fixedDeltaTime * (float)(360/(2*3.14)));
        }

        void GetGyroriantation(OSCMovuinoSensorBasicData movuino)
        {
            this.gameObject.transform.Rotate(movuino.gyroscope * Time.fixedDeltaTime * (float)(360.0 / (2 * 3.14)));
        }
        void MoveObj(OSCMovuinoSensorBasicData movuino)
        {
            this.gameObject.transform.Translate(movuino.accelerometer * Time.fixedDeltaTime);
        }

        void OrientObj(OSCMovuinoSensorBasicData movuino)
        {
            //this.gameObject.transform.localEulerAngles = Angle;
        }


    }

}