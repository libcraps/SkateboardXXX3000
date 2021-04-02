using System;
using System.IO;
using System.Globalization;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SkateBehaviour : MonoBehaviour
{
    private string dataPath = ".\\Data_visu\\Movuino-360flip_50HZ_smooth15treated.csv";
    List<float[]> rawData = new List<float[]>();
    Dictionary<string, List<float>> completeCSV = new Dictionary<string, List<float>>();
    float startTime;
    int i;
    bool end;
    void Start()
    {
        rawData = ReadCSV(dataPath);
        i = 0;
        startTime = Time.time;
        end = false;
        //this.gameObject.transform.Rotate(new Vector3(5, 0, 0));

    }
    private void FixedUpdate()
    {
        //if (i < rawData.Count && Time.time - startTime >= rawData[i][0] * 0.001 && Time.time - startTime <= rawData[i + 1][0] * 0.001)
        if (i < rawData.Count-1)
        {
            //Vector3 velocity = new Vector3(-rawData[i][13] * (float)0.5, -rawData[i][14] * (float)0.5, -rawData[i][15] * (float)0.5);
            //this.gameObject.GetComponent<Rigidbody>().AddForce(new Vector3(rawData[i][1], rawData[i][3], rawData[i][2]), ForceMode.Acceleration);
            float deltaRotX = (rawData[i + 1][10] - rawData[i][10]) * (float)(360 / 0.25);
            float deltaRotY = (rawData[i + 1][11] - rawData[i][11]) * (float)(360 / 0.25);
            float deltaRotZ = (rawData[i + 1][12] - rawData[i][12]) * (float)(360 / 0.25);
            this.gameObject.transform.Rotate(new Vector3(deltaRotX, deltaRotY, deltaRotZ));

            //this.gameObject.transform.Translate(velocity);
            //this.gameObject.transform.Rotate(new Vector3(rawData[i][4] * (float)(360 / 0.25), rawData[i][5] * (float)(360 / 0.25), rawData[i][6] * (float)(360 / 0.25)));
            i += 1;
        }

    }


    List<float[]> ReadCSV(string dataPath)
    {
        StreamReader sr = new StreamReader(dataPath);

        List<float[]> data = new List<float[]>();
        float[] tData = new float[21];
        string value = "";

        string line = sr.ReadLine();
        line = sr.ReadLine();
        int i = 0;

        while (line != null)
        {
            foreach (char a in line)
            {
                if (a == ',')
                {
                    tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                    Debug.Log(i);
                    value = "";
                    i += 1;
                } 
                else
                {
                    value += a;
                }
                
            }
            i = 0;
            data.Add(tData);
            tData = new float[21];
            value = "";
            line = sr.ReadLine();
        }
        return data;
    }
}
