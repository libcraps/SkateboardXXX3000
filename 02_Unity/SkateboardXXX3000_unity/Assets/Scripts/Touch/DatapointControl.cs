using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class DatapointControl : MonoBehaviour
{
	List<float> rawVals = new List<float>();  // array list to store each new incoming raw data
	public  int N = 15;                       // size of the list
	private float curSmoothVal = 0.0f;        // current smooth data = mean of the current raw data list
	private float oldSmoothVal = 0.0f;        // last smooth data
	public float curDerivVal = 0.0f;          // difference between current and previous smooth data
	private float smoothValOffset = 0.0f;     // reference data value
	public float curSRelativeVal = 0.0f;      // curSmoothVal offset from smoothValOffset (curSRelativeVal = curSmoothVal - smoothValOffset)
	public float curRemapVal = 0.0f;          // remap data based on the entire row, range between 0.0 and 1.0

	/////////////////////////////////////////////////////////////////////////////////////////
	/// /////////////////////////////////////////////////////////////////////////////////////////
	public int threshImpact = 0; // TO REMOVE /////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////
	/// /////////////////////////////////////////////////////////////////////////////////////////

	// Colors
	private Color curCol = Color.white;
	private Color red =	 new Color(245f/255f, 91f/255f, 85f/255f);
	private Color blue = new Color(125f/255f, 222f/255f, 227f/255f);
	private Color yellow = new Color(243f/255f, 240f/255f, 114f/255f);
	private Color purple = new Color(73f/255f, 81f/255f, 208f/255f);

	public int maxRadius = 8;
	private Vector3 oldAcceleration = Vector3.zero;
	
	void Update(){
		if (Input.GetKeyDown("space"))
			setOffsetValue();

		this.shiftRawVal ();

//		this.curCol = getLerpColor(this.curRemapVal);
		this.curCol = getLerpColor(this.curDerivVal);

		this.gameObject.GetComponent<Renderer> ().material.color = this.curCol;

		// DIPLAY POINT
		//this.gameObject.transform.localScale = new Vector3 (this.maxRadius*this.curRemapVal,this.maxRadius*this.curRemapVal,this.maxRadius*this.curRemapVal);
		if (this.curDerivVal > this.threshImpact) {
			this.gameObject.transform.localScale = new Vector3 (this.maxRadius * this.curDerivVal, this.maxRadius * this.curDerivVal, this.maxRadius * this.curDerivVal);
		} else {
			this.gameObject.transform.localScale = Vector3.zero;
		}

		// shift position based on acceleration vector
		this.gameObject.transform.position -= this.oldAcceleration;
		Vector3 curAcceleration_ = GameObject.FindGameObjectWithTag ("MainCamera").GetComponent<Arduino_TouchSurface>().acceleration;
		this.gameObject.transform.position += curAcceleration_;
		this.oldAcceleration = curAcceleration_;
	}

	public void pushNewRawVal(float rawVal_){
		// Add a new raw data value in the list
		if(rawVal_ > 0){
			this.rawVals.Add (rawVal_); // add new raw value
		}
		else{
			this.rawVals.Add (0);       // value can not be negative, so default = 0
		}

		while(this.rawVals.Count > this.N){
			this.rawVals.RemoveAt(0);       // remove older data from the list
		}

		if(this.rawVals.Count > 0){
			this.updateDataVals();        // update all data vals based on new incoming raw data 
		}
	}

	//----------------------------------------------------------------------------

	private void updateDataVals(){
		this.getSmoothVal();          // call function to smooth raw data
		this.getSmoothRelativeVal();  // call function to get the smooth relative data
		this.getDerivVal();           // call function to get derivative of current data
	}

	private void getSmoothVal(){
		// Compute mean of last N incoming data
		int meanVal_ = 0;
		foreach(int i in this.rawVals)
		{
			meanVal_ += i;
		}
		this.curSmoothVal = meanVal_ / ((float)this.rawVals.Count);
	}

	private void getSmoothRelativeVal(){
		this.curSRelativeVal = this.curSmoothVal - this.smoothValOffset; // offset data value
	}

	private void getDerivVal(){
		this.curDerivVal = this.curSmoothVal - this.oldSmoothVal;
		this.oldSmoothVal = this.curSmoothVal;
	}

	//----------------------------------------------------------------------------

	public void setOffsetValue(){
		this.smoothValOffset = this.curSmoothVal; // set current value as reference value
	}

	//----------------------------------------------------------------------------

	public void shiftRawVal(){
		// Update data list to keep a stable data flow
		if(this.rawVals.Count >= N){
			this.rawVals.Add (this.rawVals[this.rawVals.Count-1]); // duplicate last value
			this.rawVals.RemoveAt(0); // remove first value
			// Call functions to update values
			this.updateDataVals();        // update all data vals based on new incoming raw data
		}
	}

	//----------------------------------------------------------------------------

	private Color getLerpColor(float amt_){
		// Set the color of the data point based on its value
		Color newColor_ = this.purple;
		if(amt_ > 0.5){
			// shade from yellow to red if value between .5 and 1.0
			newColor_ = Color.Lerp(this.yellow, this.red, 2*(amt_ - 0.5f));
		}
		else{
			// shade from blue to yellow if value between .0 and .5
			newColor_ = Color.Lerp(this.blue, this.yellow, 2*amt_);
		}
		return newColor_;
	}
}