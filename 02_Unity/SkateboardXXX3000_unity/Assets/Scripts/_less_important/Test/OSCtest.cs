using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace MovuinoTemplate
{

    public class OSCtest : MonoBehaviour
    {

        public OSC oscManager;

        void Start()
        {
            oscManager.SetAddressHandler("/CubeX", GetMessageValue);
        }

        void Update()
        {

        }

        void GetMessageValue(OscMessage message)
        {
            float x = message.GetFloat(0);
            float y = message.GetFloat(1);
            float z = message.GetFloat(2);
            transform.position = new Vector3(x, y, z);

            Debug.Log(message);
            Send("ok", 1234);
            Send("non", "oui");
        }

        void Send(string address, object val)
        {
            OscMessage message = new OscMessage();
            message.address = address;
            message.values.Add(val);
            oscManager.Send(message);
        }


    }

}