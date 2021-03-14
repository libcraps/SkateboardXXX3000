var rawdat = [0.0,0.0]; // array to store incoming raw data
var N = 10; // default moving mean window size

function mMean(dat, n){
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
	
	//Compute moving mean
	var meandat = 0;
	for( var i = 0; i < rawdat.length; i++ ){
		meandat += rawdat[i]; 
	}
	meandat /= rawdat.length;
	
	outlet(0, meandat);
}