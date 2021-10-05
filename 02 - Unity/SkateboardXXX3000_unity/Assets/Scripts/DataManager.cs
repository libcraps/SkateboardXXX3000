using System.Collections;
using System.Collections.Generic;
using System.IO;
using System;
using System.Data;
using UnityEngine;


/// <summary>
/// Namespace relative to Data
/// </summary>
namespace Movuino.Data
{
    /// <summary>
    /// MonoBehaviour class, it represent the DataManager, it is associated to each PlayerCameraObject in the HitBox project.
    /// </summary>
    public class DataManager : MonoBehaviour
    {
//--------------------------    ATTRIBUTS    -------------------------------
        private bool _exportIntoFile;
        public bool ExportIntoFile
        {
            get
            {
                return _exportIntoFile;
            }
        }

        private bool _editDataTable = false;
        public bool EditDataTable
        {
            get
            {
                if (ExportIntoFile == false)
                {
                    _editDataTable = false;
                }
                return _editDataTable;
            }
            set
            {
                _editDataTable = value;
            }
        }

        public bool EndScenarioForData { get; set; }

        private string _filePath;
        public string FilePath
        {
            get
            {
                return _filePath;
            }
            set
            {
                _filePath = value;
            }
        }

        private List<DataTable> _dataBase;
        public List<DataTable> DataBase
        {
            get
            {
                return _dataBase;
            }
            set
            {
                _dataBase = value;
            }
        }

        //List that sum up the session that we will put in a text file
        private Dictionary<string, Dictionary<string,string>> _sessionSumUp;
        public Dictionary<string, Dictionary<string, string>> SessionSumUp
        {
            get
            {
                return _sessionSumUp;
            }
            set
            {
                _sessionSumUp = value;
            }
        }

        private Dictionary<string, string> _generaralSectionSumUp;
        public Dictionary<string, string> GeneraralSectionSumUp
        {
            get
            {
                return _generaralSectionSumUp;
            }
            set
            {
                _generaralSectionSumUp = value;
            }
        }

        //---------------------------     METHODS    -------------------------------
        private void Awake()
        {
            //INITIALISATION OF VARIABLES 
            _sessionSumUp = new Dictionary<string, Dictionary<string, string>>();
            _generaralSectionSumUp = new Dictionary<string, string>();
            _dataBase = new List<DataTable>();
        }
        private void OnDestroy()
        {
            if (_exportIntoFile == true) //We export the file t the end of the session if t
            {
                if (!Directory.Exists(_filePath))
                {
                    Debug.Log(_filePath + " has been created");
                    Directory.CreateDirectory(_filePath);
                }
                DicoToTXT(_sessionSumUp, _filePath + "SessionSumUp.txt");
                //_dataManager.ToCSV(_dataManager.DataBase[_indexScenario - 1], ".\\_data\\" + GetNameScenarioI(_indexScenario - 1) + ".csv");
                ToCSVGlobal(_dataBase, _filePath + "GlobalSessionData.csv");
                //ToCSVGlobal(Database_static, _filePath + "GlobalSessionData_TEST.csv");

            }
        }


        //--> Methods we use to stock data in file
        public static void ToCSV(DataTable dtDataTable, string strFilePath)
        {
            /*
             * Stock a DataTable in a csv
             */
            StreamWriter sw = new StreamWriter(strFilePath, false);
            //headers    
            for (int i = 0; i < dtDataTable.Columns.Count; i++)
            {
                sw.Write(dtDataTable.Columns[i]);
                if (i < dtDataTable.Columns.Count - 1)
                {
                    sw.Write(";");
                }
            }
            sw.Write(sw.NewLine);
            foreach (DataRow dr in dtDataTable.Rows)
            {
                for (int i = 0; i < dtDataTable.Columns.Count; i++)
                {
                    sw.Write(dr[i].ToString());
                    if (i < dtDataTable.Columns.Count - 1)
                    {
                        sw.Write(";");
                    }
                }
                sw.Write(sw.NewLine);
            }
            sw.Close();
        }
        public void ToCSVGlobal(List<DataTable> dtDataBase, string strFilePath)
        {
            /*
             * Stock a List of DataTable in a csv
             */
            StreamWriter sw = new StreamWriter(strFilePath, false);

            List<string> sumUpKeys = new List<string>();
            sumUpKeys = new List<string>(_sessionSumUp.Keys);

            for (int j = 1; j < sumUpKeys.Count;j++)
            {
                DataTable dtDataTable = dtDataBase[j-1];
                sw.Write(sumUpKeys[j]);
                sw.Write(sw.NewLine);
                //We add the data of the session
                //headers    
                for (int i = 0; i < dtDataTable.Columns.Count; i++)
                {
                    sw.Write(dtDataTable.Columns[i]);
                    if (i < dtDataTable.Columns.Count - 1)
                    {
                        sw.Write(";");
                    }
                }
                sw.Write(sw.NewLine);
                foreach (DataRow dr in dtDataTable.Rows)
                {
                    for (int i = 0; i < dtDataTable.Columns.Count; i++)
                    {

                        sw.Write(dr[i].ToString());
                        if (i < dtDataTable.Columns.Count - 1)
                        {
                            sw.Write(";");
                        }
                    }
                    sw.Write(sw.NewLine);
                }
                sw.Write(sw.NewLine);
            }
            sw.Close();
            Debug.Log(strFilePath + " has been created");
        }
        public void DicoToTXT(Dictionary<string, Dictionary<string, string>> dico, string strFilePath)
        {
            /*
             * Stock the SessionSumUp in a .txt file
             */
            StreamWriter sw = new StreamWriter(strFilePath, false);
            
            foreach (string globalKey in dico.Keys)
            {
                sw.Write("--> " + globalKey + " :");
                sw.Write(sw.NewLine);
                
                foreach(string key in dico[globalKey].Keys)
                {
                    sw.Write("  - " + key + " : " + dico[globalKey][key]);
                    sw.Write(sw.NewLine);
                }
                sw.WriteLine(sw.NewLine);
            }
            sw.Close();
            Debug.Log(strFilePath + " has been created");
        }

//--> Methods that manage data conteners
        public static Dictionary<string, string> StructToDictionary<StructType>(StructType structure)
        {
            /* 
             * Generic method that go throw a structure and get her data into a dictionary
             * 
             * Arguments :
             *      StructType structure : StructType is the generique of the function, and structure is the structure that we extract her data
             *      
             * Return :
             *      A dictionary Dictionary<string, string> that contain the data 
             */
            Dictionary<string, string> dico = new Dictionary<string, string>();

            foreach (var field in typeof(StructType).GetProperties())
            {
                dico.Add(field.Name, field.GetValue(structure).ToString());
            }

            return dico;
        }
        public void AddContentToSumUp(string key, Dictionary<string, string> content)
        {
            /*
             * Method that Add to the _sessionSumUp dictionary a new item "content" a the key "key"
             * 
             * Arguments : 
             *      string key : key of the content
             *      Dictionary<string, string> content : Dictionary of a new content
             */
            _sessionSumUp.Add(key, content);
        }
        public void InitGeneralSectionSumUp(string name, string filepath, int NbScenarios)
        {
            //Initialization of the GeneralSectionSumUp
            this.GeneraralSectionSumUp.Add("Date : ", DateTime.Now.ToString());
            this.GeneraralSectionSumUp.Add("Athlete : ", name);
            this.GeneraralSectionSumUp.Add("File path : ", filepath);
            this.GeneraralSectionSumUp.Add("Nb scenarios : ", NbScenarios.ToString());
            this.AddContentToSumUp("General", this.GeneraralSectionSumUp);
        }

        /// <summary>
        /// Initializes datasettings
        /// </summary>
        /// <param name="export"></param>
        /// <param name="filepath"></param>
        public void Init(bool export, string filepath)
        {
            //Set DataManager's attributs
            _exportIntoFile = export;
            _filePath = filepath;
        }
    }
}
