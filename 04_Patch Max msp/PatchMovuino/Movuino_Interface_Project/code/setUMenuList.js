inlets = 1;
outlets = 1;

function setUmenuList() {
	var myList = arguments;
	var umenuRequest = 'append ' + String(myList[0]);
	
	for(i=1; i<myList.length; i++){
		umenuRequest += ', append ' + String(myList[i]);
	}
	
	outlet(0, String(umenuRequest));
}