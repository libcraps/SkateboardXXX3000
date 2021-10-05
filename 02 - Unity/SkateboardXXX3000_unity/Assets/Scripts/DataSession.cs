using System.Collections;
using Device;
using System.Collections.Generic;
using System.Data;
using UnityEngine;

namespace Movuino.Data
{
    /*
     * Classes that allows us to deal with result of a session
     * Mother class : DataSession
     * 
     * With this class we can create data type and stock data in order to transfert everything to the dataController
     * Notice that the file will be created with a list of datatables
     * 
     * Data type :
     *      DataSessionPlayer : general data of a player (it has others data)
     *      DataSessionScenario : data of the scenario like target positions..etc
     *      DataSessionMovuino : data of movuino
     *      DataSessionPolar : data of the polar
     *      DataSessionMovuinoXMM : data of xmm
     *      DataSessonHit : data of hit
     *      
     */

    /// <summary>
    /// Abstract class that represent data types.
    /// </summary>
    /// <para>Inherit this class to create a new data tyes that is usefull to export</para>
    /// <remarks>With this class we can create data type and stock data in order to transfert everything to the dataController, Notice that the file will be created with a list of datatables</remarks>
    public abstract class DataSession
    {
        /// <summary>
        /// Create an object derived from DataSession class
        /// </summary>
        /// <typeparam name="T">Must be inherited from DataSession</typeparam>
        /// <returns>The DataSession object of type <typeparamref name="T"/> that has has been created</returns>
        public static T CreateDataObject<T>() where T : DataSession, new()
        {
            T dataObject = new T();
            return dataObject;
        }

        /// <summary>
        /// Create a DataTable
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>The dataTable that has been created</returns>
        public virtual DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            return table;
        }

        /// <summary>
        /// Merge vertically DataTables
        /// </summary>
        /// <param name="data">DataTables to merge</param>
        /// <returns>Result</returns>
        public static DataTable MergeDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            foreach (DataTable tab in data)
            {
                table.Merge(tab);
            }
            return table;
        }

        /// <summary>
        /// Merge horizontally (Join) different datatables that are in dataToJoin
        /// </summary>
        /// <param name="dataToJoin">DataTables to join</param>
        /// <returns>Result</returns>
        public static DataTable JoinDataTable(params DataTable[] dataToJoin)
        {
            /*
             * Join horizontally different datatables that are in dataToJoin
             */
            DataTable result = new DataTable();

            foreach (DataTable table in dataToJoin)
            {
                foreach (DataColumn column in table.Columns)
                {
                    result.Columns.Add(column.ColumnName);
                }
            }

            for (int i=0; i<dataToJoin[0].Rows.Count; i++)
            {
                DataRow dr = result.NewRow();
                foreach (DataTable dt in dataToJoin)
                {
                    foreach (DataColumn dc in dt.Columns)
                        dr[dc.ColumnName] = dt.Rows[i][dc.ColumnName];
                }
                result.Rows.Add(dr);

            }
            return result;
        }
        public virtual void StockData(params object[] list)
        {

        }
    }

    /// <summary>
    /// Class that represent all the data of a player during the session
    /// </summary>
    public class DataSessionPlayer : DataSession
    {
        /*
         * Class that represent all the data of a player during the session
         */
        public DataSessionScenario DataSessionScenario;
        public DataSessionMovuino[] DataSessionMovuino; //Because a player can have more than one movuino
        public DataSessionMovuinoXMM[] DataSessionMovuinoXMM;
        public DataSessionPolar DataSessionPolar;
        public DataSessionHit DataSessionHit;
        public DataSessionViveTracker DataSessionViveTracker;

        /// <summary>
        /// Get the DataTable of the DataSession object
        /// </summary>
        public DataTable DataTable { get { return CreateDataTable(); } }
        public override void StockData(params object[] list)
        {

        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <remarks>It joins dataTables from the other DataSessionType</remarks>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable joined</returns>
        public override DataTable CreateDataTable(params DataTable[] data) //TODO
        {
            DataTable result = new DataTable();
            result = JoinDataTable(DataSessionScenario.DataTable, DataSessionViveTracker.DataTable, DataSessionHit.DataTable, DataSessionPolar.DataTable);

            for(int i=0; i<DataSessionMovuino.Length;  i++) //Loop because it can have multiple movuinos
            {
                result = JoinDataTable(result, DataSessionMovuino[i].DataTable, DataSessionMovuinoXMM[i].DataTable);
            }

            return result;
        }

        /// <summary>
        /// Constructor of this DataSession object
        /// </summary>
        /// <param name="nbMov">Number of movuinos</param>
        public DataSessionPlayer(int nbMov)
        {
            DataSessionScenario = new DataSessionScenario();
            DataSessionMovuino = new DataSessionMovuino[nbMov];
            DataSessionMovuinoXMM = new DataSessionMovuinoXMM[nbMov];
            DataSessionHit = new DataSessionHit();
            DataSessionPolar = new DataSessionPolar();
            DataSessionViveTracker = new DataSessionViveTracker();

            for (int i = 0; i < nbMov; i++)
            {
                DataSessionMovuino[i] = new DataSessionMovuino();
                DataSessionMovuinoXMM[i] = new DataSessionMovuinoXMM();
            }
        }

    }

    /// <summary>
    /// Class that represent all the data of a Scenario during the session
    /// </summary>
    /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
    public class DataSessionScenario : DataSession
    {
        /// <summary>
        /// Consigne fo the scenario
        /// </summary>
        public List<object> consigne = new List<object>();
        public List<object> time = new List<object>();

        /// <value>Sum up of the scenario, used in the data controller</value>
        public Dictionary<string, string> scenarioSumUp = new Dictionary<string, string>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }

        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            time.Add(list[0]);
            consigne.Add(list[1]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("time", typeof(object));
            table.Columns.Add("Consigne", typeof(object));

            for (int i = 0; i < consigne.Count; i++)
            {
                table.Rows.Add(time[i], consigne[i]);
            }
            return table;
        }
    }

    /// <summary>
    /// Class that represent all the data of a Movuino during the session
    /// </summary>
    /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
    public class DataSessionMovuino : DataSession
    {
        /// <value>Id of the movuino</value>
        public string id;
        public List<object> listTime = new List<object>();
        public List<Vector3> listAcceleration = new List<Vector3>();
        public List<Vector3> listGyroscope = new List<Vector3>();
        public List<Vector3> listMagneto = new List<Vector3>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }


        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            listTime.Add(list[0]);
            listAcceleration.Add((Vector3)list[1]);
            listGyroscope.Add((Vector3)list[2]);
            listMagneto.Add((Vector3)list[3]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("Ax " + id, typeof(float));
            table.Columns.Add("Ay " + id, typeof(float));
            table.Columns.Add("Az " + id, typeof(float));
            table.Columns.Add("Gx " + id, typeof(float));
            table.Columns.Add("Gy " + id, typeof(float));
            table.Columns.Add("Gz " + id, typeof(float));
            table.Columns.Add("Mx " + id, typeof(float));
            table.Columns.Add("My " + id, typeof(float));
            table.Columns.Add("Mz " + id, typeof(float));

            for (int i = 0; i < listAcceleration.Count; i++)
            {
                table.Rows.Add(
                    listAcceleration[i].x, listAcceleration[i].y, listAcceleration[i].z,
                    listGyroscope[i].x, listGyroscope[i].y, listGyroscope[i].z, 
                    listMagneto[i].x, listMagneto[i].y, listMagneto[i].z);
            }

            return table;
        }
    }

    /// <summary>
    /// Class that represent all the usefull data of the sensitivPen
    /// </summary>
    /// <remarks>TODO : Add norm of the magnetometer</remarks>
    public class DataMovuinoSensitivePen : DataSession
    {
        /// <value>Id of the movuino</value>
        public string id = "";
        public List<object> listTime = new List<object>();
        public List<Vector3> listAcceleration = new List<Vector3>();
        public List<Vector3> listGyroscope = new List<Vector3>();
        public List<Vector3> listMagneto = new List<Vector3>();
        public List<float> listTheta = new List<float>();
        public List<float> listPsi = new List<float>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }


        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            listTime.Add((float)list[0]);
            listAcceleration.Add((Vector3)list[1]);
            listGyroscope.Add((Vector3)list[2]);
            listMagneto.Add((Vector3)list[3]);
            listTheta.Add((float)list[4]);
            listPsi.Add((float)list[5]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable that contain all the data</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("time" + id, typeof(float));
            table.Columns.Add("ax" + id, typeof(float));
            table.Columns.Add("ay" + id, typeof(float));
            table.Columns.Add("az" + id, typeof(float));
            table.Columns.Add("gx" + id, typeof(float));
            table.Columns.Add("gy" + id, typeof(float));
            table.Columns.Add("gz" + id, typeof(float));
            table.Columns.Add("mx" + id, typeof(float));
            table.Columns.Add("my" + id, typeof(float));
            table.Columns.Add("mz" + id, typeof(float));
            table.Columns.Add("theta" + id, typeof(float));
            table.Columns.Add("psi" + id, typeof(float));


            for (int i = 0; i < listAcceleration.Count; i++)
            {
                table.Rows.Add(listTime[i],
                    listAcceleration[i].x, listAcceleration[i].y, listAcceleration[i].z,
                    listGyroscope[i].x, listGyroscope[i].y, listGyroscope[i].z,
                    listMagneto[i].x, listMagneto[i].y, listMagneto[i].z,
                    listTheta[i],
                    listPsi[i]);
            }

            return table;
        }
    }

        /// <summary>
        /// Class that represent all the data of a Polar (heartbite sensor) during the session
        /// </summary>
        /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
        public class DataSessionPolar : DataSession
    {
        public List<object> listTime = new List<object>();
        public List<object> listBpm = new List<object>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }


        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            listTime.Add(list[0]);
            listBpm.Add(list[1]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("BPM", typeof(object));

            for (int i = 0; i < listTime.Count; i++)
            {
                table.Rows.Add(listBpm[i]);
            }

            return table;
        }
    }

    /// <summary>
    /// Class that represent all the data of a XMM analyse (gesture/mouvemement recognition) during the session
    /// </summary>
    /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
    public class DataSessionMovuinoXMM : DataSession
    {
        public string id;

        public List<object> listTime = new List<object>();
        public List<object> listGestureID= new List<object>();
        public List<object> listGestureProb= new List<object>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }

        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>

        public override void StockData(params object[] list)
        {
            listTime.Add(list[0]);
            listGestureID.Add(list[1]);
            listGestureProb.Add(list[2]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("Gesture " + id, typeof(object));
            table.Columns.Add("probability" + id, typeof(object));

            for (int i = 0; i < listTime.Count; i++)
            {
                table.Rows.Add(listGestureID[i], listGestureProb[i]);
            }


            return table;
        }
    }

    /// <summary>
    /// Class that represent all the data of hit during the session
    /// </summary>
    /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
    public class DataSessionHit : DataSession
    {
        public List<object> listTime = new List<object>();
        public List<object> listHit = new List<object>();
        public List<object> listReacTime = new List<object>();

        public float nbHit;

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }

        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            listTime.Add(list[0]);
            listHit.Add(list[1]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();
            table.Columns.Add("Hit", typeof(object));

            for (int i = 0; i < listHit.Count; i++)
            {
                table.Rows.Add(listHit[i]);
            }

            return table;
        }
    }

    /// <summary>
    /// Class that represent all the data of a ViveTracker during the session
    /// </summary>
    /// <remarks>First we stock datas into lists and we convert them into DataTables</remarks>
    public class DataSessionViveTracker : DataSession
    {
        public List<object> listTime = new List<object>();
        public List<object> listAngle = new List<object>();

        /// <value>Get the DataTable of this DataSession object</value>
        public DataTable DataTable { get { return this.CreateDataTable(); } }

        /// <summary>
        /// Stock data from list in DataSession's lists
        /// </summary>
        /// <param name="list">Data to stock</param>
        public override void StockData(params object[] list)
        {
            listTime.Add(list[0]);
            listAngle.Add(list[1]);
        }

        /// <summary>
        /// Create the DataTable of this object
        /// </summary>
        /// <param name="data">Not usefull for the moment</param>
        /// <returns>DataTable</returns>
        public override DataTable CreateDataTable(params DataTable[] data)
        {
            DataTable table = new DataTable();

            table.Columns.Add("PlayerMvt", typeof(object));

            for (int i = 0; i < listAngle.Count; i++)
            {
                table.Rows.Add(listAngle[i]);
            }

            return table;
        }
    }
}