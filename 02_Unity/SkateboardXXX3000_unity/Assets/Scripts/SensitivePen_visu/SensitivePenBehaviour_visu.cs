using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Movuino;
using Movuino.Data;
using Device;
using System.IO;


/// <summary>
/// Inherited class from ObjectMovuino_visu, it represent the sensitivPen developped during/for the PhD of Ana Phelipeau
/// </summary>
/// <remarks>It allows us tu see on Unity two relevant angle for the project : 
/// <list type="bullet">
/// <item>psi : that correspond to the orientation of the pen</item>
/// <item>theta : that correspond to the inclination of the pen</item>
/// </list>
/// </remarks>
public class SensitivePenBehaviour_visu : ObjectMovuino_visu
{
    /// <summary>
    /// File where would like to stock data during the online mode
    /// </summary>
    [SerializeField] private bool _exportIntoFile;


    [Tooltip("Path of the export data file.")]
    [SerializeField] private string _folderPath;
    [Tooltip("Filename.")]
    [SerializeField] private string _filename;

    [SerializeField] private GameObject vertAngle;
    [SerializeField] private GameObject horizAngle;

    [Tooltip("Sample rate for the offline mode.")]
    [SerializeField] private float offlineSampleRate;

    private DataMovuinoSensitivePen _movuinoExportData;

    private float startTime;
    private float prevTime;
    private int i { get { return movuinoDataSet.i; } }
    private bool end;

    //Angles we want with sensitiv pen
    private float theta;
    private float psi;

    float initPsi = 666;

    Vector3 initAngle;


    public void Start()
    {
        _movuinoExportData = new DataMovuinoSensitivePen();

        if (offlineMode)
        {
            print("Movuino offline mode");
        }
        else if (onlineMode)
        {
            print("Movuino online mode");
        }
        else if (movuinoBehaviour.enabled && movuinoDataSet.enabled)
        {
            print("Impossible to use both modes, please uncheck one");
        }

        initAngle = this.gameObject.transform.localEulerAngles;

    }
    public void FixedUpdate()
    {
        if (onlineMode)
        {
            if (initPsi == 666)
            {
                initPsi = GetPenOrientation(movuinoBehaviour.initmovuinoCoordinates.rotationMatrix);
            }

            theta = movuinoBehaviour.angleAccelOrientation.x-90;

            if (Mathf.Abs(theta) > 80)
            {
                psi = 0;
            }
            else
            {
                psi = GetPenOrientation(movuinoBehaviour.movuinoCoordinates.rotationMatrix) - initPsi;
            }

            //Angle continuity for the pen :
            MovuinoDataProcessing.AngleRange(ref psi);

            graphData.x = psi;
            graphData.y = movuinoBehaviour.magnetometerSmooth.magnitude;
            graphData.z = theta;


            this.gameObject.transform.eulerAngles = new Vector3(-theta, psi, 0);

            vertAngle.transform.eulerAngles = new Vector3(0, -theta+90,0);
            horizAngle.transform.eulerAngles = new Vector3(0, psi, 0);

            _movuinoExportData.StockData(Time.time, movuinoBehaviour.accelerationRaw, movuinoBehaviour.gyroscopeRaw, movuinoBehaviour.magnetometerRaw, theta, psi);
        } 
        else if (offlineMode)
        {

            if (Time.time - prevTime > offlineSampleRate)
            {
                theta = movuinoDataSet.GetValue("theta", i);
                psi = movuinoDataSet.GetValue("psi", i);
 
                graphData = new Vector3(psi, 0, theta); //TODO

                vertAngle.transform.eulerAngles = new Vector3(0, -theta + 90, 0);
                horizAngle.transform.eulerAngles = new Vector3(0, psi, 0);

                this.gameObject.transform.eulerAngles = new Vector3(-theta, psi, 0);


                prevTime = Time.time;
                print(prevTime);
                movuinoDataSet.i++;
            }
        }

    }

    private void OnDestroy()
    {
        if (onlineMode && _exportIntoFile) //We export the file t the end of the session if t
        {
            if (!Directory.Exists(_folderPath))
            {
                Debug.Log(_folderPath + " has been created");
                Directory.CreateDirectory(_folderPath);
            }
            DataManager.ToCSV(_movuinoExportData.DataTable, _folderPath + _filename);
        }
    }

    /// <summary>
    /// Calculate psi for the sensitive pen cf doc that explain the methods
    /// </summary>
    /// <param name="coord"></param>
    /// <returns>angle</returns>
    private float GetPenOrientation(Matrix4x4 coord)
    {
        /*
         * x' (xpen) is in the line of the matrix
         */
        float a00 = coord.m00;
        float a01 = coord.m01;
        print(coord);
        print(a01);

        float psi = Mathf.Atan2(a01, a00)*180/Mathf.PI;
        
        return psi;
    }


}