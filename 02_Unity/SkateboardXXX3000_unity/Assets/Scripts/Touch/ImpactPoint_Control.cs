using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ImpactPoint_Control : MonoBehaviour {

	private Vector3 acceleration;
	private GameObject[] pointGrid;

	// Point of impact
	private float xG = 0f;            // X coordinate of current impact
	private float yG = 0f;			  // X coordinate of current impact
	private float totG = 0;           // total pressure of current impact
	public int threshImpact = 20;     // min value to detect impact
	private float oldXG = -666;    
	private float oldYG = -666;    
	public int delayOffHit = 50;      // minimum time (in ms) between 2 impacts to be validated (minimum 50ms <=> maximum 50 hits/s)
	private float timerOffHit0 = 0;     // time of the last valid impact

	int countHit = 0;          // number of hit

	void Start () {		
		this.acceleration = GameObject.FindGameObjectWithTag ("MainCamera").GetComponent<Arduino_TouchSurface>().acceleration;
		this.pointGrid = GameObject.FindGameObjectsWithTag ("datapoint");
	}
	
	void Update () {
		

		// Get instant center of pressure
		float totG_ = 0.0f;   // instant total pressure
		float xG_ = 0f;       // instant X coordinate of center of pressure
		float yG_ = 0f;       // instant Y coordinate of center of pressure;

		foreach (GameObject datapoint_ in pointGrid) {
			if (datapoint_.GetComponent<DatapointControl>().curDerivVal > this.threshImpact) {

				/////////////////////////////////////////////////////////////////////////////////////
				/// /////////////////////////////////////////////////////////////////////////////////////
				datapoint_.GetComponent<DatapointControl> ().threshImpact = this.threshImpact;   // TO REMOVE
				/////////////////////////////////////////////////////////////////////////////////////
				/// /////////////////////////////////////////////////////////////////////////////////////

				totG_ += datapoint_.GetComponent<DatapointControl>().curRemapVal;
				xG_ += datapoint_.GetComponent<DatapointControl>().curRemapVal * datapoint_.transform.position.x;
				yG_ += datapoint_.GetComponent<DatapointControl>().curRemapVal * datapoint_.transform.position.y;
				this.timerOffHit0 = Time.time;
			}
		}

		// Get current impact
		if(1000 * (Time.time - this.timerOffHit0) > this.delayOffHit && this.totG != 0f){
			// Get current impact positon
			this.xG /= this.totG;   // get X coordinate of current impact
			this.yG /= this.totG;   // get Y coordinate of current impact

			// Set impact point object at new position
			this.gameObject.transform.position = new Vector3(xG, yG,0);
			this.gameObject.transform.position += this.acceleration;  // get instant acceleration and shift pressure center

			GameObject.FindGameObjectWithTag ("target").GetComponent<TargetControl>().setForce(new Vector3(0,0,500), this.gameObject.transform.position) ;

			this.oldXG = xG;
			this.oldYG = yG;    
			this.xG = 0;     // reset X coordinate of current impact
			this.yG = 0;     // reset Y coordinate of current impact
			this.totG = 0;   // reset pressure of current impact

			this.countHit++;   // increment number of hit
		}
		else{
			this.xG += xG_;
			this.yG += yG_;
			this.totG += totG_;
		}
		
	}
}
