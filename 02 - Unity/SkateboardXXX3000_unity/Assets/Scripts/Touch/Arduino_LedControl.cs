using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using System.Threading;

public class Arduino_LedControl : MonoBehaviour
{
	public SerialPort serial;

	public Thread serialThread;
	public bool gameRunning = true; // TO CHANGE

	string ledSerialData = "";

	// Led pannel
	int ROWS = 30;
	int COLS = 60;
	Color[] leds; // store leds data (Red, Green, Blue)
	Color[] newLedColor; // store leds data (Red, Green, Blue)
//	Texture2D screenTexture;

	public Camera cameraP1;

	void Start ()
	{
		// Initialize leds array to store color values
		leds = new Color[ROWS * COLS];
		newLedColor = new Color[ROWS * COLS];
		for (int i = 0; i < COLS; i++) {
			for (int j = 0; j < ROWS; j++) {
				//setLedColor (i,j,Color.black);
				leds[getLedIndex (i,j)] = Color.red;
				newLedColor[getLedIndex (i,j)] = Color.black;
			}
		}

		// -------------------------------------
		// -------------------------------------
		// Print available serial
		foreach(string str in SerialPort.GetPortNames())
		{
			Debug.Log(str);
		}

		// Initialize serial connection to leds pannel
		serial = new SerialPort ("COM3", 38400);
		Debug.Log ("Connection started");
		try {
			serial.Open ();
			serial.ReadTimeout = 400;
			serial.Handshake = Handshake.None;

			sendSerialMessage("connect");

			serialThread = new Thread (threadUpdate);
			serialThread.Start ();
			Debug.Log ("Port Opened!");
		} catch {
			Debug.Log ("Could not open serial port");
		}
	}

	public void OnApplicationQuit ()
	{
		if (serial != null) {
			if (serial.IsOpen) {
				sendSerialMessage("disconnect");  // stop leds
				print ("closing serial port");
				serial.Close ();
			}
			serial = null;
		}

		gameRunning = false; // strop thread
	}

	void Update(){
		// get texture from camera assigned to player 1
		Texture2D screenTexture = ScreenCapture.CaptureScreenshotAsTexture();
		//Texture2D screenTexture = GetRTPixels (cameraP1.targetTexture);

		// get pixel color to drive leds pannel
		int offsetX_ =  (int)(screenTexture.width/2f - screenTexture.height/2f);
		for (int i = 0; i < COLS; i++) {
			for (int j = 0; j < ROWS; j++) {
//				int gx_ = (int)(screenTexture.width * (0.8f * i / ((float)COLS) + 0.1f));
//				int gy_ = (int)(screenTexture.height * (0.8f * j / ((float)ROWS) + 0.1f));
				int gx_ = (int)(screenTexture.height * (i / ((float)COLS))) + offsetX_;
				int gy_ = (int)(screenTexture.height * ((j / ((float)ROWS))* 0.95f + 0.025f));
				newLedColor[getLedIndex(i,j)] = screenTexture.GetPixel (gx_, gy_);
			}
		}

		Destroy(screenTexture);
	}

	static public Texture2D GetRTPixels(RenderTexture rt)
	{
		// Remember currently active render texture
		RenderTexture currentActiveRT = RenderTexture.active;

		// Set the supplied RenderTexture as the active one
		RenderTexture.active = rt;

		// Create a new Texture2D and read the RenderTexture image into it
		Texture2D tex = new Texture2D(rt.width, rt.height);
		tex.ReadPixels(new Rect(0, 0, tex.width, tex.height), 0, 0);

		// Restorie previously active render texture
		RenderTexture.active = currentActiveRT;
		return tex;
	}

	void threadUpdate ()
	{
		while (gameRunning) {
			for (int i = 0; i < newLedColor.Length; i++) {
				setLedColor (i, newLedColor [i]);
			}
		}
	}

	private int getLedIndex (int x_, int y_)
	{
		// Convert X and Y coordinate into the led index
		x_ = Mathf.Clamp (x_, 0, COLS - 1);
		y_ = Mathf.Clamp (y_, 0, ROWS - 1);
		if (y_ % 2 == 0) {
			x_ = COLS-1 - x_;
		}
		y_ = ROWS-1 - y_;
		int ipix_ = y_ * COLS + x_;
		return ipix_;
	}

	public void setLedColor (int ipix_, Color col_)
	{
		// Do not send color value to the led if it_s already the same
		if (leds [ipix_] != col_) {
			int r_ = (int)(255 * col_.r);
			int g_ = (int)(255 * col_.g);
			int b_ = (int)(255 * col_.b);

			// Create data string to send and send it to serial port
			//ledSerialData = "" + ipix_.ToString("0000") + r_.ToString("000") + g_.ToString("000") + b_.ToString("000") + '_';   // decimal format
			ledSerialData = "" + ipix_.ToString("X3") + r_.ToString("X2") + g_.ToString("X2") + b_.ToString("X2") + '_'; 

			//-----------------------------------------------------
			// TO OPTIMIZE = color code 
			if (r_ == 0 && g_ == 0 && b_ == 0) {
				ledSerialData = "" + ipix_.ToString ("X3") + "0_";
			}
			if (r_ == 255 && g_ == 255 && b_ == 255) {
				ledSerialData = "" + ipix_.ToString ("X3") + "1_";
			}
			//-----------------------------------------------------

			// Send new color to leds pannel
			if (serial.IsOpen) {
				//print (ledSerialData);
				serial.Write (ledSerialData);
				leds [ipix_] = col_; // update led color values
			}
		}
	}

	public void sendSerialMessage(string mess_){
		if (serial.IsOpen) {
			serial.Write (mess_ + '_');
		}
	}
}