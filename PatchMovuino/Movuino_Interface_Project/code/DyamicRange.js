inlets = 2;
outlets = 5;

var rawdat = [0.0,0.0]; // array to store incoming raw data
var N = 10; // default moving mean window size
var mini = 666.6;
var maxi = -666.6;

function getRange(dat, n){
	rawdat.push(dat); // add incoming data to rawdat array
	
	// Check to update the window size
	if(n > 0){
		// N can't be equal to 0 or negative
		N = n;
	}
	
	if(rawdat.length - N > 0){
		// remove oldest data if N unchanged (i=0 removed)
		// remove from 0 to rawdat.length - N + 1 if new N < old N
		for(i=0; i < rawdat.length - N + 1 ; i++){
			rawdat.splice(i, 1);
		}
	}
	
	// Compute dynamic range limits
	mini = 66666.6;
    maxi = -66666.6;
	for( var i = 0; i < rawdat.length; i++ ){
		if(rawdat[i] < mini){
			mini = rawdat[i];
		}
		if(rawdat[i] > maxi){
			maxi = rawdat[i];
		}
	}
	
	// Compute dynamic average
	var avr_ = 0.0;
	for(i=0 ; i < rawdat.length ; i++){
		avr_ += rawdat[i];
	}
	avr_ /= rawdat.length;
	
	// Outlets
	outlet(0, maxi-mini);   // output dynamic range
	outlet(1, avr_);            // output dynamic average
	outlet(2, (maxi+mini)/2);   // output dynamic mean
	outlet(3, mini);            // output dynamic minimum
	outlet(4, maxi);            // output dynamic maximum
}