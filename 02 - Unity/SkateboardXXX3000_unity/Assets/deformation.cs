using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class deformation : MonoBehaviour
{

    public MeshFilter mesh;
    public List<Vector3> vertices;
    public List<Vector3> Initvertices;

    public int timeInterval=0;

    private int updateCount=0;
    private int i=0;

    // Start is called before the first frame update
    void Start()
    {
        mesh = this.gameObject.GetComponent<MeshFilter>();
        
        for (int i = 0; i < mesh.mesh.vertices.Length; i++)
        {
            vertices.Add(mesh.mesh.vertices[i]);
            Initvertices.Add(mesh.mesh.vertices[i]);
        }
        Debug.Log(vertices[0]);
        vertices[0] = transform.InverseTransformPoint(vertices[0]);
        Debug.Log(vertices[0]);
        mesh.mesh.SetVertices(vertices);
    }

    // Update is called once per frame
    void Update()
    {
        /*
        if (updateCount >= timeInterval)
        {
            vertices[i] = new Vector3(vertices[i][0], 0, vertices[i][2]);
            vertices[i] = transform.InverseTransformPoint(vertices[i]);
            mesh.sharedMesh.SetVertices(vertices);
            updateCount = 0;
            i++;
        }*/
        mesh.mesh.SetVertices(vertices);
        updateCount++;
    }

    private void OnDisable()
    {
       
    }
}
