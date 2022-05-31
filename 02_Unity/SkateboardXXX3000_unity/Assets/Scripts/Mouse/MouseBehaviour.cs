using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Movuino;
using Device;

public class MouseBehaviour : MonoBehaviour
{
    MovuinoBehaviour movuino;
    void Start()
    {
        movuino = GetComponent<MovuinoBehaviour>();
    }

    // Update is called once per frame
    void Update()
    {
        print(movuino.deltaAccel);
        //this.gameObject.transform.Translate(new Vector3(movuino.angleOrientation.y * (float)0.001, - movuino.angleOrientation.x * (float)0.001, 0));
    }
}
