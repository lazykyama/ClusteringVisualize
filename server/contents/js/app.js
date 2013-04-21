/**
 * app.js
 * @auther kyama http://sukimaprogrammer.blogspot.jp/
 * @since 0.0.1
 * @version 0.0.1
 * 
 * refers examples/ in three.js.
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

// require jQuery
// require util.js
// require conn.js

// definition.
kyama.app = kyama.app || {};

// consts.
kyama.app.constant = kyama.app.constant || {};
kyama.app.constant.kmeansResponseKey = kyama.app.constant.kmeansResponseKey || {};
kyama.app.constant.kmeansResponseKey.SESSION_ID_KEY = 'sessionId';
kyama.app.constant.kmeansResponseKey.RESULT_KEY = 'resultPairs';
kyama.app.constant.kmeansResponseKey.CONVERGED_KEY = 'isConverged';
kyama.app.constant.kmeansResponseKey.CENTROIDS_KEY = 'centroids';

kyama.app.constant.geometryKey = kyama.app.constant.geometryKey || {};
kyama.app.constant.geometryKey.LINE_MESH_ID = 'lines_mesh';
kyama.app.constant.geometryKey.SAMPLE_MESH_ID_PREFIX = 'sample_point_mesh_';
kyama.app.constant.geometryKey.CENTROID_MESH_ID_PREFIX = 'centroid_mesh_';

/**
 * initialize.
 */
kyama.app.init = function() {
    // parameters initialize.
    // @todo replace the initialize method can be repeatedly called.
    kyama.app.rotating = false;
    kyama.app.animRequestId = null;
    kyama.app.prevTime = Date.now();
    kyama.app.currTime = Date.now();

    kyama.app.data = {};
    
    // bind events.
    $(window).on('resize', kyama.app.onWindowResize);
    var changeBtn = $('#rot_change_btn');
    var resetBtn  = $('#reset_btn');
    var nextBtn   = $('#next_btn');

    changeBtn.on('click', kyama.app.changeRotation);
    resetBtn.on('click', kyama.app.resetState);
    nextBtn.on('click', kyama.app.executeNextStep);

    // initialize for WebGL.
    kyama.app.init3DCanvas();
    
    // reset state.
    kyama.app.resetState();
};

/**
 * callback method called when the window is resized.
 */
kyama.app.onWindowResize = function() {
    console.debug('onWindowResize.');
    kyama.app.camera.aspect = window.innerWidth / window.innerHeight;
    kyama.app.camera.updateProjectionMatrix();
    
    kyama.app.renderer.setSize(window.innerWidth, window.innerHeight);
};

/**
 * callback method called when the start/stop button is clicked.
 */
kyama.app.changeRotation = function() {
    console.debug('changeRotation: rotating? => ' + kyama.app.rotating);
    kyama.app.rotating = !kyama.app.rotating;

    // start animation if the flag is true.
    if (kyama.app.rotating) {
	kyama.app.currTime = Date.now();
	kyama.app.animate();
    } else {
	kyama.app.stopAnimate();
    }
};

/**
 * starts animation.
 */
kyama.app.animate = function() {
    kyama.app.animRequestId = requestAnimationFrame(kyama.app.animate);
    kyama.app.prevTime = kyama.app.currTime;
    kyama.app.currTime = Date.now();
    
    kyama.app.render();
};

/**
 * stops animation.
 */
kyama.app.stopAnimate = function() {
    if (null !== kyama.app.animRequestId) {
	cancelAnimationFrame(kyama.app.animRequestId);
	kyama.app.animRequestId = null;
    }
};

/**
 * callback method called when the reset button is clicked.
 */
kyama.app.resetState = function() {
    console.debug('resetState.')
    // get current input values.
    kyama.app.data.sampleSize  = parseInt($('#sample_num_input').val());
    kyama.app.data.clusterSize = parseInt($('#cluster_num_input').val());
    kyama.app.data.sessionId   = null;
    kyama.app.step = 0;
    
    // reset sample dataset and cluster assigns.
    kyama.app.executeNextStep();
};

/**
 * callback method called when the next button is clicked.
 */
kyama.app.executeNextStep = function() {
    console.debug('executeNextStep.');

    var params = {};
    if (null !== kyama.app.data.sessionId) {
	params.sessionid = kyama.app.data.sessionId;
    }
    params.step = kyama.app.step;
    params.size = kyama.app.data.sampleSize;
    params.k    = kyama.app.data.clusterSize;

    // reset sample dataset and cluster assigns.
    kyama.conn.update(params,
	kyama.app.update, 
	function() {
	    console.error('fail...');
	});
};

/**
 * updates the sample dataset and cluster assigns.
 * @param dataJson the server response json string.
 */
kyama.app.update = function(dataJson) {
    console.debug(dataJson);

    var jsonObj = JSON.parse(dataJson);

    var rawData = jsonObj[kyama.app.constant.kmeansResponseKey.RESULT_KEY];
    var sessionId = jsonObj[kyama.app.constant.kmeansResponseKey.SESSION_ID_KEY];
    var converged = jsonObj[kyama.app.constant.kmeansResponseKey.CONVERGED_KEY];
    var centroids = jsonObj[kyama.app.constant.kmeansResponseKey.CENTROIDS_KEY];
    
    var wasReset = false;
    if (null === kyama.app.data.sessionId) {
	wasReset = true;
    }

    // update.
    kyama.app.step++;
    kyama.app.data.sampleSize = rawData.length;
    kyama.app.data.sessionId  = sessionId;
    kyama.app.data.rawData    = rawData;
    kyama.app.data.centroids  = centroids;

    console.debug('isConverged: ' + converged);
    if (converged) {
	// notify learning is converged.
	console.debug('converged!');
    } else {
	// update geometry.
	kyama.app.updateGeometry(wasReset);
    }

    if (!kyama.app.rotating) {
	kyama.app.render();
    }
};

/**
 * updates the geometry with sample dataset and cluster assigns.
 * @param wasReset describes flag whether sample dataset was reset.
 */
kyama.app.updateGeometry = function(wasReset) {

    // clear geometries.
    if (wasReset) {
	var children = kyama.app.group.children;
	var childrenLength = children.length;
	for (var i = childrenLength - 1; i >= 0; i--) {
	    var child = children[i];
	    kyama.app.group.remove(child);
	}
    }

    // create objects.
    var linesGeometry = null;
    if (wasReset) {
	// lines.
	linesGeometry = new THREE.Geometry();
	var linesMaterial = new THREE.LineBasicMaterial({
	    vertexColors: true
	});
	var lineMesh = new THREE.Line(
	    linesGeometry, linesMaterial, THREE.LinePieces);
	lineMesh.id = kyama.app.constant.geometryKey.LINE_MESH_ID;
	kyama.app.group.add(lineMesh);
	for (var i = 0; i < (2 * kyama.app.data.sampleSize); i++) {
	    linesGeometry.vertices.push(new THREE.Vector3());
	    linesGeometry.colors.push(new THREE.Color());
	}
	
	// samples.
	var radius = 8;
	for (var i = 0; i < kyama.app.data.sampleSize; i++) {
	    var sphere = new THREE.SphereGeometry(radius, 10, 10);
	    var mesh = new THREE.Mesh(sphere);
	    kyama.app.group.add(mesh);
	    mesh.id = kyama.app.constant.geometryKey.SAMPLE_MESH_ID_PREFIX + i;
	}
	
	// centroids.
	radius = 20;
	for (var i = 0; i < kyama.app.data.clusterSize; i++) {
	    var sphere = new THREE.SphereGeometry(radius, 10, 10);
	    var material = new THREE.MeshPhongMaterial({
		ambient: 0xaaaaaa,
		specular: 0xaaaaaa
	    });
	    var mesh = new THREE.Mesh(sphere, material);
	    kyama.app.group.add(mesh);
	    mesh.id = kyama.app.constant.geometryKey.CENTROID_MESH_ID_PREFIX + i;
	}
	
    } else {
	// load exists object.
	var lineMesh = kyama.app.group.getObjectById(
	    kyama.app.constant.geometryKey.LINE_MESH_ID, false);
	linesGeometry = lineMesh.geometry;
	linesGeometry.colorsNeedUpdate = true;
	linesGeometry.verticesNeedUpdate = true;
    }

    // set coords & colors.
    var n = 120, n2  = n/2;
    var rawData = kyama.app.data.rawData;
    var centroids = kyama.app.data.centroids;
    for (var i = 0, srcIdx = 0; i < kyama.app.data.sampleSize; 
	 i++, srcIdx = (2 * i)) {
	var label = rawData[i][0];
	var rndColor = kyama.util.generateRandomColorFromCircle(
	    kyama.app.data.clusterSize, label);
	var hexRndColor = (rndColor.r * 255 << 16
	    | rndColor.g * 255 << 8 | rndColor.b * 255);
	var sampleData = rawData[i][1];
	var centroid = centroids[label];

	// set to sample.
	var sampleMesh = kyama.app.group.getObjectById(
	    kyama.app.constant.geometryKey.SAMPLE_MESH_ID_PREFIX + i, 
	    false);
	sampleMesh.position.x = sampleData[0] * n - n2;
	sampleMesh.position.y = sampleData[1] * n - n2;
	sampleMesh.position.z = sampleData[2] * n - n2;
	sampleMesh.material.color.setHex(hexRndColor);

	// set to line.
	linesGeometry.vertices[srcIdx].x = sampleMesh.position.x;
	linesGeometry.vertices[srcIdx].y = sampleMesh.position.y;
	linesGeometry.vertices[srcIdx].z = sampleMesh.position.z;

	linesGeometry.vertices[srcIdx + 1].x = centroid[0] * n - n2;
	linesGeometry.vertices[srcIdx + 1].y = centroid[1] * n - n2;
	linesGeometry.vertices[srcIdx + 1].z = centroid[2] * n - n2;

	linesGeometry.colors[srcIdx].setHex(hexRndColor);
	linesGeometry.colors[srcIdx + 1].setHex(hexRndColor);
    }

    // set coords & colors for centroids.
    for (var i = 0; i < kyama.app.data.clusterSize; i++) {
	var rndColor = kyama.util.generateRandomColorFromCircle(
	    kyama.app.data.clusterSize, i);
	var hexRndColor = (rndColor.r * 255 << 16
	    | rndColor.g * 255 << 8 | rndColor.b * 255);

	var centroidMesh = kyama.app.group.getObjectById(
	    kyama.app.constant.geometryKey.CENTROID_MESH_ID_PREFIX + i, 
	    false);

	centroidMesh.position.x = centroids[i][0] * n - n2;
	centroidMesh.position.y = centroids[i][1] * n - n2;
	centroidMesh.position.z = centroids[i][2] * n - n2;

	centroidMesh.material.color.setHex(hexRndColor);
    }
};

/**
 * initializes some objects for WebGL via Three.js.
 */
kyama.app.init3DCanvas = function() {
    // create objects for WebGL.
    kyama.app.container = $('#container')[0];
    kyama.app.camera = new THREE.PerspectiveCamera(
	27, (window.innerWidth / window.innerHeight), 1, 3500);
    kyama.app.camera.position.z = 2750;

    kyama.app.scene = new THREE.Scene();
    kyama.app.scene.fog = new THREE.Fog(0x050505, 2000, 3500);
    kyama.app.scene.add(new THREE.AmbientLight(0x444444));

    var light1 = new THREE.DirectionalLight(0xffffff, 0.5);
    light1.position.set(1, 1, 1);
    kyama.app.scene.add(light1);
    
    var light2 = new THREE.DirectionalLight(0xffffff, 1.5);
    light2.position.set(0, -1, 0);
    kyama.app.scene.add(light2);

    kyama.app.renderer = new THREE.WebGLRenderer({
	antialias: false, 
	alpha: false
    });
    kyama.app.renderer.setSize(window.innerWidth, window.innerHeight);
    kyama.app.renderer.setClearColor(kyama.app.scene.fog.color, 1);
    
    kyama.app.renderer.gammaInput = true;
    kyama.app.renderer.gammaOutput = true;
    kyama.app.renderer.physicallyBasedShading = true;
    
    kyama.app.container.appendChild(kyama.app.renderer.domElement);

    // initialize geometry.
    kyama.app.group = new THREE.Object3D();
    kyama.app.scene.add(kyama.app.group);
};

/**
 * callback method called to render the canvas.
 */
kyama.app.render = function() {
    var delta = (kyama.app.currTime -  kyama.app.prevTime);
    var tmpY = kyama.app.group.rotation.y;
    kyama.app.group.rotation.y = tmpY + (Math.PI * delta / 3000);
    
    kyama.app.renderer.render(
	kyama.app.scene, kyama.app.camera);
};

// execute initial functions.
kyama.app.init();
