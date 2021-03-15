inlets = 2;
outlets = 1;

var olddat = -6666.6;
var p = 5; // precision value

function dataPrecisionFilter(dat_ , p_){
	if(p_ >= 0){
		p = p_;
	}
	
	if(Math.abs(dat_ - olddat) > p){
		outlet(0, dat_);
		olddat = dat_;
	}
}