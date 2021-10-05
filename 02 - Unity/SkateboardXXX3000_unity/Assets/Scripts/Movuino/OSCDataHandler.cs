/*
 * http://thomasfredericks.github.io/UnityOSC/
 * 
 * https://github.com/thomasfredericks/UnityOSC
 */

using System.Collections.Generic;
using UnityEngine;

namespace Device
{
	/// <summary>
	/// Inherit this if you want to represent a Movuino Data Type.
	/// </summary>
	/// <para>it allows you to connect on an OSC server and get data of the correspondant address:
	/// <list type="OSCAdressList">
	/// <item>
	/// <term>/data</term>
	/// <description>movuino 9axes</description>
	/// </item>
	/// <item>
	/// <term>/gesture</term>
	/// <description>xmm</description>
	/// </item>
	/// <item>
	/// <term>/bm</term>
	/// <description>polar</description>
	/// </item>
	/// </list>
	/// </para>
	public abstract class OSCDataHandler
	{
		/*
		 * Mother class that represent and connect device on OSC server
		 * Type of data handled : movuino 9axes, bpm, and xmm (gesture)
		 * OSCAddress :
		 *		/data : movuino 9axes
		 *		/gesture : xmm
		 *		/bpm : polar
		 */
		public string OSCAddress { get { return GetAddress (); } }
		public class WrongOSCDataHandlerFormatException : UnityException
		{

		};

		/// <summary>
		/// Constructor of an OSCDataHandlerObject
		/// </summary>
		/// <typeparam name="T">Must be OSCDataHandler</typeparam>
		/// <returns></returns>
		public static T CreateOSCDataHandler<T> () where T : OSCDataHandler, new()
		{
			T newMovuinoData = new T ();
			return newMovuinoData;
		}

		//Method that read data of an OSCmessage
		/// <summary>
		/// Read data of an OSCmessage
		/// </summary>
		/// <param name="message">Message to read cf OSC documentation</param>
		public abstract void ToOSCDataHandler (OscMessage message);

		/// <summary>
		/// GetAddress
		/// </summary>
		/// <returns></returns>
		protected abstract string GetAddress();

		public static void DebugAllMessage(OscMessage msg)
		{
			Debug.Log(msg.address);
			Debug.Log(msg.values);
		}
	}

	/// <summary>
	/// Data of the accelerometer, the gyroscope and the magnetometer of Movuino
	/// </summary>
	/// <inheritdoc cref="OSCDataHandler"/>
	public class OSCMovuinoSensorBasicData : OSCDataHandler
	{
		/// <summary>
		/// Accelerometer data.
		/// </summary>
		public Vector3 accelerometer;
		/// <summary>
		/// Gysocope data.
		/// </summary>
		public Vector3 gyroscope;
		/// <summary>
		/// Magnetometer data.
		/// </summary>
		public Vector3 magnetometer;

		public static string address = "/data";

		public override void ToOSCDataHandler (OscMessage message)
		{
			float ax = message.GetFloat(0);
			float ay = message.GetFloat(1);
			float az = message.GetFloat(2);
			float gx = message.GetFloat(3);
			float gy = message.GetFloat(4);
			float gz = message.GetFloat(5);
			float mx = message.GetFloat(6);
			float my = message.GetFloat(7);
			float mz = message.GetFloat(8);
			accelerometer = new Vector3(ax, ay, az);
			gyroscope = new Vector3(gx, gy, gz);
			magnetometer = new Vector3(mx, my, mz);

		}

		protected override string GetAddress ()
		{
			return address;
		}

		public override string ToString ()
		{
			return string.Format ("[MovuinoSensorData] = "
			+ "Accelerometer = "
			+ accelerometer.ToString ()
			+ " Gyroscope = "
			+ gyroscope.ToString ()
			+ " Magnetometer = "
			+ magnetometer.ToString ());
		}
	}
	/// <summary>
	/// Data of the accelerometer, the gyroscope and the magnetometer and euler angles of Movuino
	/// </summary>
	/// <inheritdoc cref="OSCDataHandler"/>
	public class OSCMovuinoSensorExtendedData : OSCDataHandler
	{
		/// <summary>
		/// Accelerometer data.
		/// </summary>
		public Vector3 accelerometer;
		/// <summary>
		/// Gysocope data.
		/// </summary>
		public Vector3 gyroscope;
		/// <summary>
		/// Magnetometer data.
		/// </summary>
		public Vector3 magnetometer;
		/// <summary>
		/// Euler angles data.
		/// </summary>
		public Vector3 eulerAngle;

		public static string address = "/dataExtended";

		public override void ToOSCDataHandler(OscMessage message)
		{
		
			float ax = message.GetFloat(0);
			float ay = message.GetFloat(1);
			float az = message.GetFloat(2);
			float gx = message.GetFloat(3);
			float gy = message.GetFloat(4);
			float gz = message.GetFloat(5);
			float mx = message.GetFloat(6);
			float my = message.GetFloat(7);
			float mz = message.GetFloat(8);
			float ex = message.GetFloat(9);
			float ey = message.GetFloat(10);
			float ez = message.GetFloat(11);
			accelerometer = new Vector3(ax, ay, az);
			gyroscope = new Vector3(gx, gy, gz);
			magnetometer = new Vector3(mx, my, mz);
			eulerAngle = new Vector3(ex, ey, ez);

		}

		protected override string GetAddress()
		{
			return address;
		}

		public override string ToString()
		{
			return string.Format("[MovuinoSensorData] = "
			+ "Accelerometer = "
			+ accelerometer.ToString()
			+ " Gyroscope = "
			+ gyroscope.ToString()
			+ " Magnetometer = "
			+ magnetometer.ToString());
		}
	}


	/// <summary>
	/// Data of the XMM from the pathMax (normally)
	/// </summary>
	/// <remarks>It gets the gesture ID and his progression</remarks>
	public class OSCMovuinoXMM : OSCDataHandler
	{
		/// <summary>
		/// ID of gesture
		/// </summary>
		public int gestId;
		/// <summary>
		/// Progression of the gesture
		/// </summary>
		public float gestProg;

		public static string address = "/gesture";

		public override void ToOSCDataHandler (OscMessage message)
		{
			gestId = message.GetInt(0);
			gestProg = message.GetFloat(1);
		}
			
		protected override string GetAddress ()
		{
			return address;
		}

		public override string ToString ()
		{
			return string.Format ("[MovuinoXMM] = "
			+ "xmmGestId = "
			+ gestId.ToString ()
			+ "xmmGestProg = "
			+ gestProg.ToString ());
		}
	}


	/// <summary>
	/// Data of the accelerometer, the gyroscope and the magnetometer of Movuino
	/// </summary>
	/// <inheritdoc cref="OSCDataHandler"/>
	public class OSCPolarBPM : OSCDataHandler
	{
		public float bpm;

		public static string address = "/bpm";

		public override void ToOSCDataHandler(OscMessage message)
		{
			bpm = message.GetFloat(0);
			Debug.Log("BPM recu via OSC : " + bpm);

		}

		protected override string GetAddress()
		{
			return address;
		}

		public override string ToString()
		{
			return string.Format("[PolarBPM] = "
			+ "bpm = " + bpm);
		}
	}
}

