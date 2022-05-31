inlets = 1;
outlets = 5;

var dataCollect = [0.0,0.0];
var N = 50;
var index = 0;
var mini = 0;
var maxi = 0;
var olddat = 0;

while(dataCollect.length < N){
	dataCollect.push(0.0); // initialize array
}


function stepDetection(dat){
	// Update min & max data
	if(index < N){
		// Fill data array
		dataCollect[index] = dat;
		index++;
	}
	else{
		// Compute min & max once array is full (every N incoming data)
		index = 0;
		
		maxi = -66666;
		mini = 66666;
		
		for(i=0 ; i < dataCollect.length ; i++){
			maxi = Math.max(dataCollect[i],maxi);
			mini = Math.min(dataCollect[i],mini);
		}
	}
	
	// Step detection up
	if(dat >= (maxi+mini)/2 && olddat < (maxi+mini)/2){
		outlet(0, "bang");		
	}
	
	// Step detection down
	if(dat <= (maxi+mini)/2 && olddat > (maxi+mini)/2){
		outlet(1, "bang");		
	}
	
	
	outlet(2, (maxi+mini)/2);	// output mean val
	outlet(3, mini);	        // output minimum
	outlet(4, maxi);	        // output maximum
	
	olddat = dat;
}