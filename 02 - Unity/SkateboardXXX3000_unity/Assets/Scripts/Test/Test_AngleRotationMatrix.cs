using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Movuino
{
    public class Test_AngleRotationMatrix : ObjectMovuino_visu
    {
        [SerializeField] private GameObject x;
        [SerializeField] private GameObject y;
        [SerializeField] private GameObject z;



        // Start is called before the first frame update
        void Start()
        {

        }

        // Update is called once per frame
        void Update()
        {
            //this.transform.localPosition = movuinoBehaviour.magnetometerSmooth.normalized/2;
            x.transform.localPosition = movuinoBehaviour.movuinoCoordinates.xAxis.normalized / 2;
            y.transform.localPosition = movuinoBehaviour.movuinoCoordinates.yAxis.normalized / 2;
            z.transform.localPosition = movuinoBehaviour.movuinoCoordinates.zAxis.normalized / 2;

            print(movuinoBehaviour.movuinoCoordinates.xAxis);

            
        }
    }

}