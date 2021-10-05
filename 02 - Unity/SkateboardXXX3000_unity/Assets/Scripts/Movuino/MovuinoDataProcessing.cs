using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace Movuino
{
    /// <summary>
    /// Static class that contains usefull methods for process data of the movuino
    /// </summary>
    public static class MovuinoDataProcessing
    {
        public static float RAD_TO_DEG = 180 / Mathf.PI;
        public static float DEG_TO_RAD = 1/RAD_TO_DEG;

        /// <summary>
        /// Integrate with Euler methods incoming data
        /// </summary>
        /// <param name="vectorInstDerivate">Derivate data</param>
        /// <param name="vectorIntegrate">Integrate data</param>
        /// <param name="dt">delta time (sampling period)</param>
        /// <returns>Integrate a time t vector</returns>
        public static Vector3 GetEulerIntegration(Vector3 vectorInstDerivate, Vector3 vectorIntegrate, float dt)
        {
            vectorIntegrate.x += vectorInstDerivate.x * dt;
            vectorIntegrate.y += vectorInstDerivate.y * dt;
            vectorIntegrate.z += vectorInstDerivate.z * dt;
            return vectorIntegrate;
        }


        /// <summary>
        /// Return the angle Vector between gravity and incoming acceleration 
        /// </summary>
        /// <param name="U">Acceleration</param>
        /// <returns></returns>
        public static Vector3 ComputeAngleAccel(Vector3 U)
        {
            Vector3 angle;

            float alpha; //z angle
            float beta; //x angle
            float gamma; //y angle

            U = U.normalized;

            alpha = Mathf.Acos(U.x);
            beta = Mathf.Acos(U.y);
            gamma = Mathf.Acos(U.z);

            angle = new Vector3(alpha, beta, gamma) * 360 / (2 * Mathf.PI);
            return angle;
        }

        /// <summary>
        /// return the angle Vector between earth magnetic field and the movuino
        /// </summary>
        /// <param name="U">Bmov</param>
        /// <returns></returns>
        public static Vector3 ComputeAngleMagnetometer(Vector3 U)
        {
            Vector3 angle;

            float alpha; //z angle
            float beta; //x angle
            float gamma; //y angle

            U = U.normalized;

            alpha = Mathf.Acos(U.x);
            beta = Mathf.Acos(U.y);
            gamma = Mathf.Atan(U.z);

            angle = new Vector3(alpha, beta, gamma) * 360 / (2 * Mathf.PI);
            //print(angle + " ---- " + U);
            return angle;
        }


        /// <summary>
        /// Filtered incoming data, BP filter
        /// </summary>
        /// <param name="rawDat">Incoming data</param>
        /// <param name="listMean"></param>
        /// <returns></returns>
        public static float MovingMean(float rawDat, ref List<float> listMean, int nbPointFilter)
        {
            float meanDat = 0;
            listMean.Add(rawDat);

            if (listMean.Count - nbPointFilter > 0)
            {
                // remove oldest data if N unchanged (i=0 removed)
                // remove from 0 to rawdat.length - N + 1 if new N < old N
                for (int i = 0; i < listMean.Count - nbPointFilter + 1; i++)
                {
                    listMean.RemoveAt(0);
                }
            }
            foreach (float number in listMean)
            {
                meanDat += number;
            }
            meanDat /= listMean.Count;
            return meanDat;
        }


        public static Vector3 MovingMean(Vector3 rawDat, ref List<Vector3> listMean, int nbPointFilter)
        {
            Vector3 meanDat = new Vector3(0, 0, 0);
            listMean.Add(rawDat);

            if (listMean.Count - nbPointFilter > 0)
            {
                // remove oldest data if N unchanged (i=0 removed)
                // remove from 0 to rawdat.length - N + 1 if new N < old N
                for (int i = 0; i < listMean.Count - nbPointFilter + 1; i++)
                {
                    listMean.RemoveAt(0);
                }
            }
            foreach (Vector3 vector in listMean)
            {
                meanDat += vector;
            }
            meanDat /= listMean.Count;
            return meanDat;
        }

        /// <summary>
        /// HP filter
        /// </summary>
        /// <param name="fc">Cut frequency</param>
        /// <param name="Te">Sampling period</param>
        /// <param name="sn_last">Last HP value</param>
        /// <param name="en">Current entry value</param>
        /// <param name="en_last">Previous entry value</param>
        /// <returns>HP value</returns>
        public static float HighPassFilter(float fc, float Te, float sn_last, float en, float en_last)
        {
            float tau = 1 / (2 * Mathf.PI * fc);
            float sn = sn_last * (1 - Te / tau) + en - en_last;
            return sn;
        }

        /// <summary>
        /// HP filter.
        /// </summary>
        /// <param name="fc">Cut frequency</param>
        /// <param name="Te">Sampling period</param>
        /// <param name="sn_last">Last HP value</param>
        /// <param name="en">Current entry value</param>
        /// <param name="en_last">Previous entry value</param>
        /// <returns>HP value</returns>
        public static Vector3 HighPassFilter(float fc, float Te, Vector3 sn_last, Vector3 en, Vector3 en_last)
        {
            Vector3 sn;
            float gx = HighPassFilter(fc, Te, sn_last.x, en.x, en_last.x);
            float gy = HighPassFilter(fc, Te, sn_last.y, en.y, en_last.y);
            float gz = HighPassFilter(fc, Te, sn_last.z, en.z, en_last.z);
            sn = new Vector3(gx, gy, gz);

            return sn;
        }


        /// <summary>
        /// Return euler angles of the rotation matrix.
        /// </summary>
        /// <param name="rotationMatrix">Rotation Matrix</param>
        /// <returns>Euler angles of the rotation matrix</returns>
        public static Vector3 GetEulerAngle(Matrix4x4 rotationMatrix)
        {
            float a00 = rotationMatrix.m00;
            float a10 = rotationMatrix.m10;
            float a20 = rotationMatrix.m20;
            float a01 = rotationMatrix.m01;
            float a11 = rotationMatrix.m11;
            float a21 = rotationMatrix.m21;
            float a02 = rotationMatrix.m02;
            float a12 = rotationMatrix.m12;
            float a22 = rotationMatrix.m22;

            float theta;
            float psi;
            float phi;

            float sy = Mathf.Sqrt(a00 * a00 + a10 * a10);
            float sw = Mathf.Acos(Mathf.Sqrt(a21 * a21 + a22 * a22));
            float sz = -Mathf.Asin(a20);

            bool singuler = sy < 0.0001;

            if (!singuler)
            {
                phi = Mathf.Atan2(a21, a22);
                theta = Mathf.Atan2(-a20, sy);
                psi = Mathf.Atan2(a10, a00);

            }
            else
            {

                phi = Mathf.Atan2(a21, a22);
                theta = Mathf.Atan2(a20, sy);
                psi = 0;
            }

            return new Vector3(phi, theta, psi);
        }

        public static void AngleRange(ref float psi)
        {
            //Angle continuity for the pen :
            if (psi < -180 && psi >= -360)
            {
                psi += 360;
            }
            else if (psi > 180 && psi <= 360)
            {
                psi -= 360;
            }
        }


    }
}

