using System;
using System.Collections;
using System.Collections.Generic;
using Movuino;
using UnityEngine;
using UnityEngine.UI;


namespace Graph
{
    /// <summary>
    /// Class that manages the graph representation and his curves
    /// </summary>
    public class WindowGraph : MonoBehaviour
    {
        //---- Window part -----
        [Tooltip("Dot representation.")]
        [SerializeField] private Sprite circleSprite;
        [Tooltip("Graph that will contain every cuvres (must have a RectTransform components).")]
        [SerializeField] private RectTransform graphContainer;
        [Tooltip("Curve prefab (must have a script 'Curve' as components).")]
        [SerializeField] private Curve curvePrefab;
        [Tooltip("Vertical maximum value (from the middle of the graph.")]
        [SerializeField] private int _yMax;
        [Tooltip("Number of dots that you wwill have in the graph.")]
        [SerializeField] private int nbDot;

        private List<Curve> curveList;
        private int nbCurve;

        private GameObject rawDataText;

        //usefull bc movuino
        private Text angleX;
        private Text angleY;
        private Text angleZ;

        //--------- Movuino part -----
        /// <summary>
        /// Movuino object that you want to represent
        /// </summary>
        [Tooltip("Must have a script component that inherit from 'ObjectMovuino_visu'.")]
        [SerializeField] private ObjectMovuino_visu objectVisu;

        //test
        private List<float> liste;
        private int i = 0;

        /// <summary>
        /// Initialise and instantitaes objects that you will need during the 
        /// </summary>
        private void Awake()
        {
            curveList = new List<Curve>();
            nbCurve = 3;

            //Instantiation and initialisation of curves
            for (int k = 0; k < nbCurve; k++)
            {
                GameObject go = Instantiate(curvePrefab.gameObject, graphContainer);
                go.GetComponent<Curve>().Init(circleSprite, graphContainer, _yMax, nbDot);
                go.name = go.name + "_" + Curve.index;
                curveList.Add(go.GetComponent<Curve>());
            }

            curveList[0].curveColor = new Color(200, 0, 0);
            curveList[1].curveColor = new Color(0, 200, 0);
            curveList[2].curveColor = new Color(0, 0, 200);

            rawDataText = this.gameObject.transform.Find("RawDataTexte").gameObject;
            angleX = rawDataText.transform.Find("AngleX").GetComponent<Text>();
            angleY = rawDataText.transform.Find("AngleY").GetComponent<Text>();
            angleZ = rawDataText.transform.Find("AngleZ").GetComponent<Text>();
        }
        /// <summary>
        /// Update graph values
        /// </summary>
        private void Update()
        {
            float valX=0;
            float valY=0;
            float valZ=0;

            //Data of differents curve
            if (objectVisu.onlineMode)
            {
                valX = objectVisu.graphData.x;
                valY = objectVisu.graphData.y;
                valZ = objectVisu.graphData.z;
            }
            else if (objectVisu.offlineMode)
            {
                valX = objectVisu.graphData.x;
                valY = objectVisu.graphData.y;
                valZ = objectVisu.graphData.z;
            }
            else
            {
                valX = 0;
                valY = 0;
                valZ = 0;
            }
           
            curveList[0].valueList.Add(valX);
            curveList[1].valueList.Add(valY);
            curveList[2].valueList.Add(valZ);

            angleX.text = "Angle X : " + (int)valX;
            angleY.text = "Angle Y : " + (int)valY;
            angleZ.text = "Angle Z : " + (int)valZ;

            for (int k =0; k<nbCurve; k++)
            {
                curveList[k].RefreshCurve();
            }
        }

    }



}