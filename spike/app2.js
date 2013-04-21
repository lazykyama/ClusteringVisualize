// app2.js
// refers examples/ in three.js
kyama.app = kyama.app || {};

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

    // ジオメトリを初期化
    initializeSamplesGeometry();

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
	kyama.dummy.updateRandomAssigns();
	kyama.dummy.updateMeans();

	updateSamplesGeometry(false);
	kyama.app.animate();	
    }, false);

    // store now.
    kyama.app.currTime = Date.now();
};

/**
 * ジオメトリ更新
 */
var updateSamplesGeometry = function(isInit) {
    // init samples.
    var linesGeometry = null;
    if (isInit) {
	linesGeometry = new THREE.Geometry();
	var linesMaterial = new THREE.LineBasicMaterial({
	    vertexColors: true
	});
	var lineMesh = new THREE.Line(
	    linesGeometry, linesMaterial, THREE.LinePieces);
	lineMesh.id = 'lines_mesh';
	kyama.app.group.add(lineMesh);
    } else {
	var lineMesh = kyama.app.group.getObjectById('lines_mesh', false);
	linesGeometry = lineMesh.geometry;
	linesGeometry.colorsNeedUpdate = true;
    }
    
    var radius = 8;
    var n = 300, n2 = n/2;
    for (var i = 0; i < kyama.dummy.samples.length; i++) {
	var sampleLabel = kyama.dummy.randomAssigns[i];
	var rndColor = kyama.app.generateRandomColorFromCircle(
	    kyama.dummy.LABELS_NUM, sampleLabel
	);
	
	if (isInit) {
	    var sphere = new THREE.SphereGeometry(radius, 10, 10);
	    var material = new THREE.MeshBasicMaterial({
		color: (rndColor.r * 255 << 16 
			| rndColor.g * 255 << 8 | rndColor.b * 255),
		shininess: 255
	    });
	    
	    var mesh = new THREE.Mesh(sphere, material);
	    mesh.position.x = kyama.dummy.samples[i][0] * n - n2;
	    mesh.position.y = kyama.dummy.samples[i][1] * n - n2;
	    mesh.position.z = kyama.dummy.samples[i][2] * n - n2;
	    mesh.id = 'sample_point_mesh_' + i;
	    kyama.app.group.add(mesh);
	    
	    linesGeometry.vertices.push(new THREE.Vector3(
		mesh.position.x, mesh.position.y, mesh.position.z
	    ));
	    linesGeometry.vertices.push(new THREE.Vector3(
		kyama.dummy.means[sampleLabel][0] * n - n2, 
		kyama.dummy.means[sampleLabel][1] * n - n2,
		kyama.dummy.means[sampleLabel][2] * n - n2
	    ));

	    linesGeometry.colors.push(new THREE.Color(
		rndColor.r * 255 << 16 
		    | rndColor.g * 255 << 8 | rndColor.b * 255));
	    linesGeometry.colors.push(new THREE.Color(
		rndColor.r * 255 << 16 
		    | rndColor.g * 255 << 8 | rndColor.b * 255));
	} else {
	    var mesh = kyama.app.group.getObjectById(
		('sample_point_mesh_' + i),
		false);
	    mesh.material.color.setHex(
		rndColor.r * 255 << 16 
		    | rndColor.g * 255 << 8 | rndColor.b * 255);
	    
	    var srcIdx = (2 * i);
	    var dstIdx = (2 * i + 1);
	    var srcColor = linesGeometry.colors[srcIdx];
	    srcColor.setHex(
		rndColor.r * 255 << 16
		    | rndColor.g * 255 << 8 | rndColor.b * 255);
	    var dstColor = linesGeometry.colors[dstIdx];
	    dstColor.setHex(
		rndColor.r * 255 << 16 
		    | rndColor.g * 255 << 8 | rndColor.b * 255);
	}
    }

    radius = 20;
    for (var i = 0; i < kyama.dummy.means.length; i++) {
	var rndColor = kyama.app.generateRandomColorFromCircle(
	    kyama.dummy.LABELS_NUM, i);

	if (isInit) {
	    var sphere = new THREE.SphereGeometry(radius, 10, 10);
	    var material = new THREE.MeshPhongMaterial({
		color: (rndColor.r * 255 << 16 
			| rndColor.g * 255 << 8 | rndColor.b * 255),
		ambient: 0xaaaaaa,
		specular: 0xaaaaaa,
		shininess: 128
	    });
	    
	    var mesh = new THREE.Mesh(sphere, material);
	    mesh.position.x = kyama.dummy.means[i][0] * n - n2;
	    mesh.position.y = kyama.dummy.means[i][1] * n - n2;
	    mesh.position.z = kyama.dummy.means[i][2] * n - n2;
	    mesh.id = 'centroid_mesh_' + i;
	    kyama.app.group.add(mesh);
	} else {
	    var mesh = kyama.app.group.getObjectById(
		('centroid_mesh_' + i),
		false);

	    mesh.position.x = kyama.dummy.means[i][0] * n - n2;
	    mesh.position.y = kyama.dummy.means[i][1] * n - n2;
	    mesh.position.z = kyama.dummy.means[i][2] * n - n2;

	    mesh.material.color.setHex(
		rndColor.r * 255 << 16 
		    | rndColor.g * 255 << 8 | rndColor.b * 255);
	}
    }
};

/**
 * ジオメトリ初期化
 */
var initializeSamplesGeometry = function() {
    // create & regist
    kyama.app.group = new THREE.Object3D();
    kyama.app.scene.add(kyama.app.group);

    // update.
    updateSamplesGeometry(true);
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
    if (kyama.app.isRunning && false) {
	var time = Date.now() * 0.001;
	//kyama.app.group.rotation.x = time * 0.25;
	kyama.app.group.rotation.y = time * 0.5;
    } else if (kyama.app.isRunning) {
	var delta = (kyama.app.currTime - kyama.app.prevTime);
	var tmpX = kyama.app.group.rotation.x;
	var tmpY = kyama.app.group.rotation.y;
	// PI rad. / 5000msec
	//kyama.app.group.rotation.x = tmpX + (Math.PI * delta / 5000);
	// PI rad. / 2500msec
	kyama.app.group.rotation.y = tmpY + (Math.PI * delta / 2500);
    }
    
    kyama.app.renderer.render(
	kyama.app.scene, kyama.app.camera);
};

// execute initial functions.
kyama.app.init();
kyama.app.animate();
