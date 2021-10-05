using System;
using System.IO;
using System.Globalization;
using System.Collections;
using System.Data;
using System.Collections.Generic;
using UnityEngine;

namespace Movuino
{
    /// <summary>
    /// Class That represent a complete file of data of a movuino
    /// </summary>
    public class MovuinoDataSet: MonoBehaviour
    {
        /// <summary>
        /// Path of the file.
        /// </summary>
        [Tooltip("Path of the file.")]
        [SerializeField] private string folderPath;
        /// <summary>
        /// Name of the file.
        /// </summary>
        [Tooltip("Name of the file.")]
        [SerializeField] private string filename;

        List<object[]> rawData_ = new List<object[]>();
        DataTable _rawData;

        /// <summary>
        /// DataTable that contain ll the data set.
        /// </summary>
        public DataTable rawData
        {
            get { return _rawData; }
        }

        public DataRowCollection table
        {
            get { return _rawData.Rows; }
        }

        /// <summary>
        /// Current index in the dataTable
        /// </summary>
        public int i;

        #region Properties
        //Basic data that you should find in a movuino file
        /// <summary>
        /// Returns the time value at the index i.
        /// </summary>
        public float time { get { return GetValue("time",i); } }
        /// <summary>
        /// Returns the vector acceleration at the index i.
        /// </summary>
        public Vector3 acceleration { get { return GetAcceleration(i); } }
        /// <summary>
        /// Returns the vector gyro at the index i.
        /// </summary>
        public Vector3 gyroscope { get { return GetGyroscope(i); } }
        /// <summary>
        /// Returns the vector magnetometer at the index i.
        /// </summary>
        public Vector3 magnetometre { get { return GetMagnetometre(i); } }

        /// <summary>
        /// Returns the vector angleGyr at the index i.
        /// </summary>
        /// <remarks>It doesn't have to be obligatory in the file.</remarks>
        public Vector3 angleGyrOrientation 
        { 
            get 
            { 
                if (Convert.ToBoolean(_rawData.Rows[i]["ThetaGyrx"]))
                {
                    return GetVector("ThetaGyrx", "ThetaGyry", "ThetaGyrz", i);
                }
                else
                {
                    return new Vector3(0, 0, 0);
                }
            } 
        }

        /// <summary>
        /// Returns the vector angleAccelOrientation at the index i.
        /// </summary>
        /// <remarks>It doesn't have to be obligatory in the file.</remarks>
        public Vector3 angleAccelOrientationRaw
        {
            get
            {
                if (Convert.ToBoolean(_rawData.Rows[i]["ThetaAccx"]))
                {
                    return GetVector("ThetaAccx", "ThetaAccy", "ThetaAccz", i);
                }
                else
                {
                    return new Vector3(0, 0, 0);
                }
            }
        }
        #endregion
        #region Methods

        public void Awake()
        {
            Init(folderPath + filename);
        }

        public void Start()
        {
            
        }

        /// <summary>
        /// Read and stock a csv in the rawData dataTable.
        /// </summary>
        /// <param name="dataPath">path of the file.</param>
        public void Init(string dataPath)
        {
            Debug.Log("Reading... " + dataPath);
            //rawData_ = ReadCSV(dataPath);
            _rawData = ConvertCSVtoDataTable(dataPath);
            i = 1;
        }

        /// <summary>
        /// Get a vector from the raw data a the index i.
        /// </summary>
        /// <param name="columnX">column x</param>
        /// <param name="columnY">column y</param>
        /// <param name="columnZ">column z</param>
        /// <param name="i">index in raw data</param>
        /// <returns>Vector3(x,y,z)</returns>
        public Vector3 GetVector(string columnX, string columnY, string columnZ, int i)
        {
            float x = GetValue(columnX, i);
            float y = GetValue(columnY, i);
            float z = GetValue(columnZ, i);
            return new Vector3(x, y, z);
        }

        /// <summary>
        /// GetVector("ax", "ay", "az")
        /// </summary>
        /// <param name="i">index</param>
        /// <returns></returns>
        public Vector3 GetAcceleration(int i)
        {
            return GetVector("ax", "ay", "az", i);
        }

        /// <summary>
        /// GetVector("gx", "gy", "gz")
        /// </summary>
        /// <param name="i">index</param>
        /// <returns></returns>
        public Vector3 GetGyroscope(int i)
        {
            return GetVector("gx", "gy", "gz", i);
        }

        /// <summary>
        /// GetVector("mx", "my", "mz")
        /// </summary>
        /// <param name="i">index</param>
        /// <returns></returns>
        public Vector3 GetMagnetometre(int i)
        {
            return GetVector("mx", "my", "mz", i);
        }

        /// <summary>
        /// Get a complete column.
        /// </summary>
        /// <param name="columnName"></param>
        /// <returns>List of floats <=> dataTable[columnName].Value</returns>
        public List<float> GetColumn(string columnName)
        {
            List<float> column = new List<float>();

            for (int i = 0; i < _rawData.Columns.Count; i++)
            {
                column.Add(GetValue(columnName, i));
            }

            return column;
        }

        /// <summary>
        /// Get the value of (float)rawData.Rows[index][columnName].
        /// </summary>
        /// <param name="columnName">Column name.</param>
        /// <param name="index">Index of the line.</param>
        /// <returns>Result : (float)_rawData.Rows[index][columnName]</returns>
        public float GetValue(string columnName, int index)
        {
            return (float)_rawData.Rows[index][columnName];
        }

        /// <summary>
        /// Convert a csv file to a datatable.
        /// </summary>
        /// <param name="strFilePath">Path of the csv file.</param>
        /// <returns>Result</returns>
        /// <remarks>Column type is float/System.Single.</remarks>
        public static DataTable ConvertCSVtoDataTable(string strFilePath)
        {
            StreamReader sr = new StreamReader(strFilePath);
            string[] headers = sr.ReadLine().Split(',');
            DataTable dt = new DataTable();

            foreach (string header in headers)
            {
                dt.Columns.Add(header);
                dt.Columns[header].DataType = typeof(float);
            }
            CultureInfo culture = new CultureInfo("en-US");
            while (!sr.EndOfStream)
            {
                string[] rows = sr.ReadLine().Split(',');
                DataRow dr = dt.NewRow();
                for (int i = 0; i < headers.Length; i++)
                {
                    dr[i] = float.Parse(rows[i], culture);
                }
                dt.Rows.Add(dr);
            }
            return dt;
        }

        List<object[]> ReadCSV(string dataPath)
        {

            StreamReader sr = new StreamReader(dataPath);
            char sep = ',';

            string line = sr.ReadLine();

            //We'ra counting the number of column
            int nb_columne = 1;
            foreach (char a in line)
            {
                if (a == sep)
                    nb_columne++;
            }
            List<object[]> data = new List<object[]>(); //All the file
            object[] tData = new object[nb_columne]; //Data for a t time that has a 
            string value = "";
            int i = 0;

            //Header
            foreach (char a in line)
            {
                if (a == ',')
                {
                    tData[i] = value;

                    value = "";
                    i += 1;
                }
                else
                {
                    value += a;
                }

            }
            tData[i] = value;
            data.Add(tData);
            tData = new object[nb_columne];
            value = "";
            line = sr.ReadLine();

            //Data
            while (line != null)
            {
                i = 0;
                //We read all the line
                foreach (char a in line)
                {
                    if (a == ',')
                    {
                        tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                        value = "";
                        i += 1;
                    }
                    else
                    {
                        value += a;
                    }

                }
                tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                data.Add(tData);
                tData = new object[nb_columne];
                value = "";
                line = sr.ReadLine();
            }
            return data;
        }
        #endregion
    }


}