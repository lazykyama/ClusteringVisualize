/**
 * util.js
 * @auther kyama http://sukimaprogrammer.blogspot.jp/
 * @since 0.0.1
 * @version 0.0.1
 * 
 * This source is distributed under the MIT License.
 * 
 * Copyright (c) 2013 kyama http://sukimaprogrammer.blogspot.jp/
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

kyama = kyama || {};
kyama.util = kyama.util || {};
kyama.util.version = '0.0.1';

kyama.util.constant = kyama.constant || {};
kyama.util.constant.TWO_PI_DEGREE = 360.0;

// generate random color on 
kyama.util.generateRandomColorFromCircle = function(splitSize, index) {
    if (splitSize <= 0) {
	throw new Error('negative splitSize[' + splitSize + '] is invalid.');
    }
    if (index < 0) {
	throw new Error('negative index[' + index + '] is invalid.');
    }

    var interval = kyama.util.constant.TWO_PI_DEGREE / splitSize;
    var hue = (index * interval);
    var sat = 1.0;
    var val = 1.0;

    // this code written in reference to the following site and Wikipedia.
    // http://www.technotype.net/tutorial/tutorial.php?fileId=%7BImage%20processing%7D&sectionId=%7B-converting-between-rgb-and-hsv-color-space%7D
    var hi = Math.floor(hue / 60.0) % 6;
    var f  = (hue / 60.0) - hi;
    var p  = val * (1.0 - sat);
    var q  = val * (1.0 - sat * f);
    var t  = val * (1.0 - sat * (1.0 - f));

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
    default:
	throw new Error('unexpected error: args = ' + splitSize + ', ' + index);
    }
};
