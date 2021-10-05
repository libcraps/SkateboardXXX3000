using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetControl : MonoBehaviour {

	private Rigidbody rb;

	// Use this for initialization
	void Start () {
		rb = gameObject.GetComponent<Rigidbody>();
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetMouseButtonUp (0)) {
			Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
			setForce (new Vector3(0,0,500), ray.origin);
		}
	}

	public void setForce(Vector3 force, Vector3 position){
		RaycastHit hit;
		if (Physics.Raycast(position, Vector3.forward, out hit)){
			if (hit.collider != null && hit.transform.tag == "target")  {
				rb.AddForceAtPosition (force, position);
			}
		}
	}
}
