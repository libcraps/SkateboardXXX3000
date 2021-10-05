using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Device;
using Movuino;

public class SphereBehaviour : MonoBehaviour
{
    MovuinoBehaviour movuinoBehaviour;
    Vector3 angle;

    
    public void Awake()
    {
        angle = new Vector3();
        movuinoBehaviour = GetComponent<MovuinoBehaviour>();
    }

    public void FixedUpdate()
    {
        angle = movuinoBehaviour.angleGyrOrientation;
        this.gameObject.transform.Rotate(movuinoBehaviour.gyroscopeRaw * Time.deltaTime);
        if (Input.GetKeyDown(KeyCode.G))
        {
            this.gameObject.transform.eulerAngles = GameObject.Find("OrbitCamera").transform.eulerAngles;
        }
    }


#if UNITY_EDITOR
    public void Update()
    {
        GetMouse();
    }
    public void GetMouse()
    {
        float x = Input.GetAxis("Mouse X")*3;
        float y = Input.GetAxis("Mouse Y")*3;
        print(Input.GetAxis("Mouse X"));
        this.gameObject.transform.Rotate(new Vector3(0,-y,-x));
    }

}
#endif
