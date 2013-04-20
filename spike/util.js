// util.js

kyama = kyama || {};
kyama.app = kyama.app || {};

// generate random color on 
kyama.app.generateRandomColorFromCircle = function(splitSize, index) {
    if (splitSize <= 0) {
	throw new Error('negative splitSize[' + splitSize + '] is invalid.');
    }
    if (index < 0) {
	throw new Error('negative index[' + index + '] is invalid.');
    }

    var PI_DEGREE = 360.0;
    var interval = PI_DEGREE / splitSize;
    var hue = (index * interval);
    var sat = 1.0;
    var val = 1.0;

    // this code written in reference to the following site and Wikipedia.
    // http://www.technotype.net/tutorial/tutorial.php?fileId=%7BImage%20processing%7D&sectionId=%7B-converting-between-rgb-and-hsv-color-space%7D
    var hi = Math.floor(hue / 60.0) % 6;
    var f  = (hue / 60.0) - hi;
    var p  = Math.round(val * (1.0 - sat));
    var q  = Math.round(val * (1.0 - sat * f));
    var t  = Math.round(val * (1.0 - sat * (1.0 - f)));

    switch(hi) {
    case 0:
	return {
	    r: val,
	    g: t,
	    b: p
	};
    case 1:
	return {
	    r: q,
	    g: val,
	    b: p
	};
    case 2:
	return {
	    r: p,
	    g: val,
	    b: t
	};
    case 3:
	return {
	    r: p,
	    g: q,
	    b: val
	};
    case 4:
	return {
	    r: t,
	    g: p,
	    b: val
	};
    case 5:
	return {
	    r: val,
	    g: p,
	    b: q
	};
    }
};
