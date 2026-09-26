/**
 * Three.js 3D Food & Exploded Molecular Layer Scene
 */

export class ThreeFoodScene {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    this.camera.position.set(0, 0, 7);

    this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    this.clock = new THREE.Clock();
    this.initObjects();
    this.initLights();
    this.initEvents();
    this.animate();
  }

  initObjects() {
    this.foodMasterGroup = new THREE.Group();
    this.foodMasterGroup.position.set(2.4, 0, 0);
    this.scene.add(this.foodMasterGroup);

    // 1. Outer Orange Peel (Two separating hemispheres)
    const peelMat = new THREE.MeshStandardMaterial({
      color: 0xff6600,
      roughness: 0.4,
      metalness: 0.05,
    });

    const peelGeomLeft = new THREE.SphereGeometry(1.6, 32, 32, 0, Math.PI);
    this.peelMeshLeft = new THREE.Mesh(peelGeomLeft, peelMat);
    this.foodMasterGroup.add(this.peelMeshLeft);

    const peelGeomRight = new THREE.SphereGeometry(1.6, 32, 32, Math.PI, Math.PI);
    this.peelMeshRight = new THREE.Mesh(peelGeomRight, peelMat);
    this.foodMasterGroup.add(this.peelMeshRight);

    // 2. Inner Pulp / Hydration Core (Translucent PBR Sphere)
    const pulpGeom = new THREE.SphereGeometry(1.2, 32, 32);
    const pulpMat = new THREE.MeshPhysicalMaterial({
      color: 0xffaa00,
      transmission: 0.6,
      opacity: 0.85,
      transparent: true,
      roughness: 0.2,
      ior: 1.33,
    });
    this.pulpMesh = new THREE.Mesh(pulpGeom, pulpMat);
    this.foodMasterGroup.add(this.pulpMesh);

    // 3. Molecular Micronutrient Orbiting Particles (Vitamin C & Potassium)
    this.nutrientGroup = new THREE.Group();
    const particleGeom = new THREE.SphereGeometry(0.08, 16, 16);
    const vitCMat = new THREE.MeshStandardMaterial({ color: 0x00f2ff, emissive: 0x00f2ff, emissiveIntensity: 0.8 });
    const potMat = new THREE.MeshStandardMaterial({ color: 0x10b981, emissive: 0x10b981, emissiveIntensity: 0.8 });

    for (let i = 0; i < 40; i++) {
      const isVitC = Math.random() > 0.5;
      const p = new THREE.Mesh(particleGeom, isVitC ? vitCMat : potMat);
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      const radius = 1.3 + Math.random() * 0.4;

      p.position.set(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi)
      );
      this.nutrientGroup.add(p);
    }
    this.foodMasterGroup.add(this.nutrientGroup);

    // 4. Outer Glowing HUD Orbit Ring
    const ringGeom = new THREE.TorusGeometry(2.2, 0.015, 16, 100);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x00f2ff, transparent: true, opacity: 0.25 });
    this.ringMesh = new THREE.Mesh(ringGeom, ringMat);
    this.ringMesh.rotation.x = Math.PI / 3;
    this.foodMasterGroup.add(this.ringMesh);
  }

  initLights() {
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    this.scene.add(ambientLight);

    const cyanLight = new THREE.PointLight(0x00f2ff, 3.0, 50);
    cyanLight.position.set(5, 5, 5);
    this.scene.add(cyanLight);

    const orangeLight = new THREE.PointLight(0xff7700, 3.5, 50);
    orangeLight.position.set(-5, -3, 4);
    this.scene.add(orangeLight);
  }

  initEvents() {
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    const elapsedTime = this.clock.getElapsedTime();

    this.foodMasterGroup.rotation.y = elapsedTime * 0.2;
    this.nutrientGroup.rotation.y = -elapsedTime * 0.4;
    this.ringMesh.rotation.z = elapsedTime * 0.15;

    this.renderer.render(this.scene, this.camera);
  }
}
