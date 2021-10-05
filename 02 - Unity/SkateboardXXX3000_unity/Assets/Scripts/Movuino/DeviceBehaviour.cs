using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Namespace relative to device
/// </summary>
namespace Device
{
    /// <summary>
    /// MonoBehaviour class used to described e bit more DeviceBehaviours
    /// </summary>
    /// <remarks></remarks>
    public class DeviceBehaviour : MonoBehaviour
    {
        /// <summary>
        /// Id of the device
        /// </summary>
        public string id { get; set; }

        /// <summary>
        /// OSCDataHandlerObject cf Polar for use
        /// </summary>
        public OSCDataHandler oscData;

        /// <summary>
        /// Initialize device parameters
        /// </summary>
        /// <param name="structure">Device parameters</param>
        /// <param name="id">Id of the device</param>
        public virtual void Init(string id)
        {
            this.id = id;
        }
    }

}