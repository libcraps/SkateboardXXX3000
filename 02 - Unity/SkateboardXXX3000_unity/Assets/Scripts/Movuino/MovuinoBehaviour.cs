using System.Collections.Generic;
using Device;
using UnityEngine;
using Movuino.Data;
using System.IO;

/// <summary>
/// Namespace relative to movuino's scripts
/// </summary>
namespace Movuino
{
    /// <summary>
    /// Class that manage the movuino object in the scene
    /// </summary>
    /// <remarks>Handle OSC conncetion too</remarks>
    public class MovuinoBehaviour : MonoBehaviour
	{
        #region Attributs
        /// <summary>
        /// OSC connection
        /// </summary>
        [Tooltip("OSC object that will make the connection with the movuino.")]
        public OSC oscManager;

        /// <summary>
        /// OSC adress that the movuino will read
        /// </summary>
        [Tooltip("OSC adress that the movuino will read.")]
        [SerializeField] private string _movuinoAdress;

        /// <summary>
        /// Level of filtering of the data.
        /// </summary>
        [Tooltip("Level of filtering of the data.")]
        [SerializeField] private int _nbPointFilter;

        // List usefull for the filtering of the data
        private List<Vector3> _listMeanAcc;
        private List<Vector3> _listMeanGyro;
        private List<Vector3> _listMeanMag;

        //norm
        private float _normAccel;
        private float _normGyro;
        private float _normMag;

        private string _addressSensorData;

        private OSCMovuinoSensorBasicData _OSCmovuinoSensorData; //9axes data
        public string movuinoAdress { get { return _movuinoAdress; } }


        #region Properties
        //OSC
        public OSCMovuinoSensorBasicData OSCmovuinoSensorData { get { return _OSCmovuinoSensorData; } }
        //Instant data
        /// <summary>
        /// Last value of the acceleration that came out from the movuino
        /// </summary>
        public Vector3 instantAcceleration { get { return _OSCmovuinoSensorData.accelerometer; } }
        /// <summary>
        /// Last value of the gyro that came out from the movuino
        /// </summary>
        public Vector3 instantGyroscope { get { return _OSCmovuinoSensorData.gyroscope; } }
        /// <summary>
        /// Last value of the magnetometer that came out from the movuino
        /// </summary>
        public Vector3 instantMagnetometer { get { return _OSCmovuinoSensorData.magnetometer; } }

        //Data for the duration of the frame
        /// <summary>
        /// Value of the acceleration during the current frame
        /// </summary>
        public Vector3 accelerationRaw { get { return _accel; } }
        /// <summary>
        /// Value of the gyro during the current frame
        /// </summary>
        public Vector3 gyroscopeRaw { get { return (_gyr)*(float)(360/(2*3.14)); } }
        /// <summary>
        /// Value of the magnetometer during the current frame
        /// </summary>
        public Vector3 magnetometerRaw { get { return _mag; } }

        //Data for the duration of the frame
        /// <summary>
        /// Value of the norm of acceleration during the current frame
        /// </summary>
        public float normAccel { get { return _normAccel; } }
        /// <summary>
        /// Value of the norm of gyro during the current frame
        /// </summary>
        public float normGyro { get { return (_normGyro) * (float)(360 / (2 * 3.14)); } }
        /// <summary>
        /// Value of the norm of magnetometer during the current frame
        /// </summary>
        public float normMag { get { return _normMag; } }


        //Filtered data
        /// <summary>
        /// Filtered value of the acceleration during the current frame 
        /// </summary>
        public Vector3 accelerationSmooth { get { return MovuinoDataProcessing.MovingMean(_accel, ref _listMeanAcc, _nbPointFilter); } }
        /// <summary>
        /// Filtered value of the gyro during the current frame 
        /// </summary>
        public Vector3 gyroscopeSmooth { get { return MovuinoDataProcessing.MovingMean(_gyr, ref _listMeanGyro, _nbPointFilter) * (float)(360 / (2 * 3.14)); } }
        /// <summary>
        /// Filtered value of the magnetometer during the current frame 
        /// </summary>
        public Vector3 magnetometerSmooth { get { return MovuinoDataProcessing.MovingMean(_mag, ref _listMeanMag, _nbPointFilter); } }

        //DeltaValues
        /// <summary>
        /// Delta value of the acceleration between the last frame and the current frame
        /// </summary>
        public Vector3 deltaAccel { get { return _accel - _prevAccel;  } }
        /// <summary>
        /// Delta value of the gyro between the last frame and the current frame
        /// </summary>
        public Vector3 deltaGyr { get { return _gyr - _prevGyr;  } }
        /// <summary>
        /// Delta value of the magnetometer between the last frame and the current frame
        /// </summary>
        public Vector3 deltaMag { get { return _mag - _prevMag;  } }


        //Angle obtained with != ways
        /// <summary>
        /// Angle obtained by integration of the gyroscope
        /// </summary>
        public Vector3 angleGyrOrientation {  get { return _angleGyrMethod; } }
        /// <summary>
        /// Angle obtained using the inclinaison of the axis and vertical axis (gravity)
        /// </summary>
        public Vector3 angleAccelOrientation {  get { return _angleAccelMethod; } }
        /// <summary>
        /// Euler angle (not Working)
        /// </summary>
        public Vector3 angleEuler { get { return (_euler) * 180 / Mathf.PI;  } }
        #endregion

        /// <summary>
        /// Structure that represent a coordinates system of the movuino for the currant frame
        /// </summary>
        /// <remarks>At the moment it is used esentially for the SensitivPen</remarks>
        public struct Coordinates
        {
            /// <summary>
            /// x axis
            /// </summary>
            public Vector3 xAxis;
            /// <summary>
            /// y axis
            /// </summary>
            public Vector3 yAxis;
            /// <summary>
            /// z axis
            /// </summary>
            public Vector3 zAxis;

            /// <summary>
            /// 4x4 matrix that contains the coordinate system
            /// </summary>
            public Matrix4x4 rotationMatrix { get { return new Matrix4x4(new Vector4(xAxis.x, xAxis.y, xAxis.z, 0), 
                                                                         new Vector4(yAxis.x, yAxis.y, yAxis.z, 0), 
                                                                         new Vector4(zAxis.x, zAxis.y, zAxis.z, 0), 
                                                                         new Vector4(0, 0, 0, 1));  } }

            public override string ToString() {
                return "  x  " + "  y  " + "  z  " + " \n " 
                    + xAxis.x + "   " + yAxis.x + "   " + zAxis.x + " \n " 
                    + xAxis.y + "   " + yAxis.y + "   " + zAxis.y + " \n " 
                    + xAxis.z + "   " + yAxis.z + "   " + zAxis.z;
            }

            /// <summary>
            /// Constructor
            /// </summary>
            /// <param name="i"></param>
            public Coordinates(int i)
            {
                xAxis = new Vector3(666, 666, 666);
                yAxis = new Vector3(666, 666, 666);
                zAxis = new Vector3(666, 666, 666);
            }
        }


        Vector3 _accel;
        Vector3 _gyr;
        Vector3 _mag;
        Vector3 _euler;

        Vector3 _prevAccel;
        Vector3 _prevGyr;
        Vector3 _prevMag;
        Vector3 _prevEuler;

        Vector3 _deltaAngleAccel;

        Vector3 _initObjectAngle;
        Vector3 _initGyr;
        Vector3 _initAccel;
        Vector3 _initMag;
        Vector3 _initEulerAngle;

        Vector3 _angleMagMethod;
        Vector3 _angleGyrMethod;
        Vector3 _angleAccelMethod;
        Vector3 _initMagAngle;

        /// <summary>
        /// Coordinates system of the movuino
        /// </summary>
        public Coordinates movuinoCoordinates;
        /// <summary>
        /// Initial coordinate system of the movuino
        /// </summary>
        public Coordinates initmovuinoCoordinates;
        #endregion

        #region Methods

        #region Unity implemented Methods
        private void Awake()
        {
            Init();
            _addressSensorData = movuinoAdress + _OSCmovuinoSensorData.OSCAddress;

        }
        void Start()
        {
            //Set the adress to listen and the associated function
            oscManager.SetAddressHandler(movuinoAdress, _OSCmovuinoSensorData.ToOSCDataHandler);
        }


        private void FixedUpdate()
        {
            UpdateMovuinoData();
            
        }

        private void OnDestroy()
        {

        }
        #endregion

        /// <summary>
        /// Initialise movuino's attributs
        /// </summary>
        public void Init()
		{
            _prevAccel = new Vector3(0, 0, 0);
            _prevGyr = new Vector3(0, 0, 0);
            _prevMag = new Vector3(0, 0, 0);
            _prevEuler = new Vector3(0, 0, 0);

            _accel = new Vector3(0, 0, 0);
            _gyr = new Vector3(0, 0, 0);
            _mag = new Vector3(0, 0, 0);
            _euler = new Vector3(0, 0, 0);

            _initObjectAngle = this.gameObject.transform.eulerAngles;
            _deltaAngleAccel = new Vector3(0, 0, 0);

            _initGyr = new Vector3(666, 666, 666);
            _initAccel = new Vector3(666, 666, 666);
            _initMag = new Vector3(666, 666, 666);
            _initEulerAngle = new Vector3(0, 0, 0);

            _angleGyrMethod = new Vector3(0, 0, 0);
            _angleAccelMethod = new Vector3(0, 0, 0);
            _angleMagMethod = new Vector3(0, 0, 0);

            _listMeanAcc = new List<Vector3>();
            _listMeanGyro = new List<Vector3>();
            _listMeanMag = new List<Vector3>();

            initmovuinoCoordinates = new Coordinates(0);

            _OSCmovuinoSensorData = OSCDataHandler.CreateOSCDataHandler<OSCMovuinoSensorBasicData>();
        }

        public void UpdateMovuinoData()
        {

            /*
             * Initialise value of _init variable (else it stays a null)
             */
            if (_initMag == new Vector3(666, 666, 666) && _initAccel == new Vector3(666, 666, 666) && initmovuinoCoordinates.xAxis == new Vector3(666, 666, 666) && _mag != new Vector3(0, 0, 0) && _accel != new Vector3(0, 0, 0))
            {
                _initMag = _mag;
                _initAccel = _accel;

                Vector3 d = _initAccel.normalized;
                Vector3 e = Vector3.Cross(d, _initMag.normalized).normalized;
                Vector3 n = Vector3.Cross(e, d).normalized;
                initmovuinoCoordinates.xAxis = n;
                initmovuinoCoordinates.yAxis = e;
                initmovuinoCoordinates.zAxis = d;
            }
            

            // --- Updtae values 
            _prevAccel = _accel;
            _prevGyr = _gyr;
            _prevMag = _mag;
            _prevEuler = _euler;

            _accel = instantAcceleration;
            _gyr = instantGyroscope;
            _mag = instantMagnetometer;

            _normAccel = _accel.magnitude;
            _normGyro = _gyr.magnitude;
            _normMag = _mag.magnitude;
            
            _angleGyrMethod = MovuinoDataProcessing.GetEulerIntegration(gyroscopeRaw, _angleGyrMethod, Time.fixedDeltaTime);
            _angleMagMethod = MovuinoDataProcessing.ComputeAngleMagnetometer(magnetometerSmooth.normalized);
            _angleAccelMethod = MovuinoDataProcessing.ComputeAngleAccel(accelerationSmooth.normalized);
            _deltaAngleAccel = _angleAccelMethod - _deltaAngleAccel;

            // --- Getting orientation matrix -----
            Vector3 D = accelerationSmooth.normalized;
            Vector3 E = Vector3.Cross(D, magnetometerSmooth.normalized).normalized;
            Vector3 N = Vector3.Cross(E, D).normalized;

            movuinoCoordinates.xAxis = N;
            movuinoCoordinates.yAxis = E;
            movuinoCoordinates.zAxis = D;
        }
        #endregion



    }

}