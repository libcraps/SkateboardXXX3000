using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Movuino
{
    /// <summary>
    /// Abstract class for a device that use a movuino.
    /// </summary>
    /// <remarks>It can be used offline or online.</remarks>
    public abstract class ObjectMovuino_visu: MonoBehaviour
    {

        private MovuinoDataSet _movuinoDataSet;
        private MovuinoBehaviour _movuinoBehaviour;

        /// <summary>
        /// Represents the graph
        /// </summary>
        [System.NonSerialized]
        public Vector3 graphData;

        /// <summary>
        /// Boolean that indicates if the play mode is online.
        /// </summary>
        /// <remarks>It'll be set to false if both of mode are selected.</remarks>
        public bool onlineMode 
        {
            get
            {
                if (movuinoBehaviour.enabled && !movuinoDataSet.enabled)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        /// <summary>
        /// Boolean that indicates if the play mode is offline.
        /// </summary>
        /// <remarks>It'll be set to false if both of mode are selected.</remarks>
        public bool offlineMode
        {
            get
            {
                if (movuinoDataSet.enabled && !movuinoBehaviour.enabled)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        /// <summary>
        /// Used for the offline mode, it contains a set of data.
        /// </summary>
        public MovuinoDataSet movuinoDataSet { get { return _movuinoDataSet; } }

        /// <summary>
        /// Used for the online mode, it represents the movuino.
        /// </summary>
        public MovuinoBehaviour movuinoBehaviour { get { return _movuinoBehaviour; } }

        /// <summary>
        /// Initialise movuinoDataSet, movuinoBehaviour, and the graph.
        /// </summary>
        public void Awake()
        {
            _movuinoDataSet = GetComponent<MovuinoDataSet>();
            _movuinoBehaviour = GetComponent<MovuinoBehaviour>();
            graphData = new Vector3(0, 0, 0);
        }

    }

}
