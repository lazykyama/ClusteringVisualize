// app.js
// refers examples/webgl_buffergeometry.html in three.js 
kyama.app = {};

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

kyama.app.init = function() {
    // load container object.
    kyama.app.container = document.getElementById('container');

    // create & init. a camera & scene.
    kyama.app.camera = new THREE.PerspectiveCamera(
	27, window.innerWidth / window.innerHeight, 1, 3500);
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

    // prepare label assigns.
    var triangles = kyama.dummy.samples.length;
    var LABELS_NUM = 5;

    var randomAssigns = [];
    for (var i = 0; i < triangles; i++) {
	var eachAssign = Math.floor(Math.random() * 1000) % LABELS_NUM;
	randomAssigns.push(eachAssign);
    }

    // prepare geometries.
    var geometry = new THREE.BufferGeometry();
    geometry.attributes = {
	index: {
	    itemSize: 1,
	    array: new Uint16Array(triangles * 3),
	    numItems: triangles * 3
	},
	position: {
	    itemSize: 3,
	    array: new Float32Array(triangles * 3 * 3),
	    numItems: triangles * 3 * 3
	},
	normal: {
	    itemSize: 3,
	    array: new Float32Array(triangles * 3 * 3),
	    numItems: triangles * 3 * 3
	},
	color: {
	    itemSize:  3,
	    array: new Float32Array(triangles * 3 * 3),
	    numItems: triangles * 3 * 3
	}
    }

    // break geometry into
    // chunks of 21,845 triangles (3 unique vertices per triangle)
    // for indices to fit into 16 bit integer number
    // floor(2^16 / 3) = 21845
    var chunkSize = 21845;
    var indices = geometry.attributes.index.array;
    for (var i = 0; i < indices.length; i++) {
	indices[i] = i % (3 * chunkSize);
    }
    
    var positions = geometry.attributes.position.array;
    var normals = geometry.attributes.normal.array;
    var colors = geometry.attributes.color.array;
    
    var color = new THREE.Color();
    
    var n = 150, n2 = n/2;	// triangles spread in the cube
    var d = 36, d2 = d/2;	// individual triangle size
    
    var pA = new THREE.Vector3();
    var pB = new THREE.Vector3();
    var pC = new THREE.Vector3();

    var cb = new THREE.Vector3();
    var ab = new THREE.Vector3();
    
    for (var i = 0; i < positions.length; i += 9) {
	// positions
	var sampleIndex = Math.floor(i / 9);
	
	var x = kyama.dummy.samples[sampleIndex][0] * n - n2;
	var y = kyama.dummy.samples[sampleIndex][1] * n - n2;
	var z = kyama.dummy.samples[sampleIndex][2] * n - n2;
	
	var ax = x + Math.random() * d - d2;
	var ay = y + Math.random() * d - d2;
	var az = z + Math.random() * d - d2;
	
	var bx = x + Math.random() * d - d2;
	var by = y + Math.random() * d - d2;
	var bz = z + Math.random() * d - d2;
	
	var cx = x + Math.random() * d - d2;
	var cy = y + Math.random() * d - d2;
	var cz = z + Math.random() * d - d2;
	
	positions[i]     = ax;
	positions[i + 1] = ay;
	positions[i + 2] = az;

	positions[i + 3] = bx;
	positions[i + 4] = by;
	positions[i + 5] = bz;
	
	positions[i + 6] = cx;
	positions[i + 7] = cy;
	positions[i + 8] = cz;
	
	// flat face normals
	pA.set(ax, ay, az);
	pB.set(bx, by, bz);
	pC.set(cx, cy, cz);

	cb.subVectors(pC, pB);
	ab.subVectors(pA, pB);
	cb.cross(ab);

	cb.normalize();
	
	var nx = cb.x;
	var ny = cb.y;
	var nz = cb.z;
	
	normals[i]     = nx;
	normals[i + 1] = ny;
	normals[i + 2] = nz;
	
	normals[i + 3] = nx;
	normals[i + 4] = ny;
	normals[i + 5] = nz;
	
	normals[i + 6] = nx;
	normals[i + 7] = ny;
	normals[i + 8] = nz;
	
	// colors
	var sampleLabel = randomAssigns[sampleIndex];
	var tmpColor = kyama.app.generateRandomColorFromCircle(
	    LABELS_NUM, sampleLabel);
	color.setRGB(tmpColor.r, tmpColor.g, tmpColor.b);

	colors[i]     = color.r;
	colors[i + 1] = color.g;
	colors[i + 2] = color.b;
	
	colors[ i + 3 ] = color.r;
	colors[ i + 4 ] = color.g;
	colors[ i + 5 ] = color.b;
	
	colors[i + 6] = color.r;
	colors[i + 7] = color.g;
	colors[i + 8] = color.b;
    }
    geometry.offsets = [];
    
    var offsets = triangles / chunkSize;
    for (var i = 0; i < offsets; i++) {
	var offset = {
	    start: i * chunkSize * 3,
	    index: i * chunkSize * 3,
	    count: Math.min(triangles - (i * chunkSize), chunkSize) * 3
	};
	geometry.offsets.push(offset);
    }
    geometry.computeBoundingSphere();
    
    var material = new THREE.MeshPhongMaterial( {
	color: 0xaaaaaa, ambient: 0xaaaaaa, specular: 0xffffff, shininess: 250,
	side: THREE.DoubleSide, vertexColors: THREE.VertexColors
    } );
    
    kyama.app.mesh = new THREE.Mesh(geometry, material);
    kyama.app.scene.add(kyama.app.mesh);
    
    kyama.app.renderer = new THREE.WebGLRenderer({
	antialias: false, 
	clearColor: 0x333333, 
	clearAlpha: 1,
	alpha: false
    });
    kyama.app.renderer.setSize(window.innerWidth, window.innerHeight);
    kyama.app.renderer.setClearColor(kyama.app.scene.fog.color, 1);
    
    kyama.app.renderer.gammaInput = true;
    kyama.app.renderer.gammaOutput = true;
    kyama.app.renderer.physicallyBasedShading = true;
    
    kyama.app.container.appendChild(kyama.app.renderer.domElement);
    
    // add event listener.
    window.addEventListener('resize', kyama.app.onWindowResize, false);

    var changeBtn = document.getElementById('change_btn');
    var stepBtn = document.getElementById('step_btn');
    kyama.app.isRunning = true;
    
    changeBtn.addEventListener('click', function() {
	kyama.app.isRunning = !kyama.app.isRunning;
	kyama.app.currTime = Date.now();
	kyama.app.animate();
    }, false);
    stepBtn.addEventListener('click', function() {
	kyama.app.isRunning = false;
	kyama.app.animate();	
    }, false);

    // store now.
    kyama.app.currTime = Date.now();
};

kyama.app.onWindowResize = function() {
    kyama.app.camera.aspect = window.innerWidth / window.innerHeight;
    kyama.app.camera.updateProjectionMatrix();
    
    kyama.app.renderer.setSize(window.innerWidth, window.innerHeight);
};

kyama.app.animate = function() {
    kyama.app.prevTime = kyama.app.currTime;
    kyama.app.currTime = Date.now();
    
    if (kyama.app.isRunning) {
	requestAnimationFrame(kyama.app.animate);
    }
    kyama.app.render();
};

kyama.app.render = function() {
    if (false) {
	var time = Date.now() * 0.001;
	kyama.app.mesh.rotation.x = time * 0.25;
	kyama.app.mesh.rotation.y = time * 0.5;
    } else {
	var delta = (kyama.app.currTime - kyama.app.prevTime);
	var tmpX = kyama.app.mesh.rotation.x;
	var tmpY = kyama.app.mesh.rotation.y;
	// PI rad. / 5000msec
	kyama.app.mesh.rotation.x = tmpX + (Math.PI * delta / 5000);
	// PI rad. / 2500msec
	kyama.app.mesh.rotation.y = tmpY + (Math.PI * delta / 2500);
    }
    
    kyama.app.renderer.render(
	kyama.app.scene, kyama.app.camera);
};

// execute initial functions.
kyama.app.init();
kyama.app.animate();
