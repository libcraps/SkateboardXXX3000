using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Movuino;

/// <summary>
/// Class for the  camera to follow a target around a sphere
/// </summary>
public class FollowingBehaviour : MonoBehaviour
{
    public GameObject target;
    public GameObject CameraTracker;
    public float thetaLim;
    public float thetaMin;

    MovuinoBehaviour movuino;


    bool toRecenter;
    void Start()
    {
        movuino = target.transform.parent.gameObject.GetComponent<MovuinoBehaviour>();
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 angleEuler = target.transform.parent.transform.eulerAngles;
        Vector3 angleCame = transform.eulerAngles;
        Vector3 angleVect = angleEuler - angleCame;

        Vector3 vectCentre = transform.right;
        Vector3 orientTargetVect = target.transform.parent.transform.right;
        Vector3 VectCamSphere = (target.transform.position - CameraTracker.transform.position).normalized;

        float angle = Vector3.SignedAngle(vectCentre, orientTargetVect, vectCentre);
        if (Mathf.Abs(angle) > thetaLim)
        {
                Vector3 omega = new Vector3(movuino.gyroscopeRaw.x, movuino.gyroscopeRaw.y, movuino.gyroscopeRaw.z);
                transform.Rotate(omega * Time.deltaTime*1.5f);
                
        }

        if (angleVect.x < -180)
            angleVect.x += 360;
        else if (angleVect.x > 180)
            angleVect.x -= 360;

        if (angleVect.y < -180)
            angleVect.y += 360;
        else if (angleVect.y > 180)
            angleVect.y -= 360;

        if (angleVect.z < -180)
            angleVect.z += 360;
        else if (angleVect.z > 180)
            angleVect.z -= 360;

        //print("angle :" + angleVect);
        transform.Rotate(angleVect/180);
    }
}
