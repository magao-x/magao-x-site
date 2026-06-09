<script setup lang="ts">
import type * as THREE from "three";
interface Props {
  layout?: "left" | "right" | "center";
}
const { layout = "center" } = defineProps<Props>();

import { onMounted, onUnmounted, ref } from "vue";

const containerRef = ref<HTMLElement | null>(null);

const FRAMES_PER_SECOND = 24.0;
const throttleFrameRate = true;
const DEG2RAD = Math.PI / 180.0;

onMounted(async () => {
  const THREE = await import("three");
  const { LineMaterial } = await import("three/addons/lines/LineMaterial.js");
  const { Wireframe } = await import("three/addons/lines/Wireframe.js");
  const { LineSegmentsGeometry } = await import("three/addons/lines/LineSegmentsGeometry.js");

  const { OrbitControls } = await import("three/examples/jsm/controls/OrbitControls.js");
  const { GLTFLoader } = await import("three/addons/loaders/GLTFLoader.js");
  if (!containerRef.value) return;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x101020);

  // Camera
  const width = containerRef.value.clientWidth;
  const height = containerRef.value.clientHeight;
  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  const desktopLatDeg = 45.0;
  const mobileLatDeg = 30.0;
  const desktopCameraDist = 50.0;
  // Tighter orbit on mobile keeps the camera inside the secondary-telescope
  // bounding sphere instead of grazing/clipping through its wireframe.
  const mobileCameraDist = 65.0;
  const lngDeg = 180.0;
  const thetaLng = lngDeg * DEG2RAD;

  camera.far = 10000;
  camera.filmGauge = 35;

  // Hack to offset the center of the orbit rotation
  // - Desktop: shift horizontally via filmOffset so the overlay sits beside the wireframe
  // - Mobile: lower the camera elevation (more horizon-ish) + shift vertically via setViewOffset
  const mobileMedia = window.matchMedia("(max-width: 768px)");
  let controls: any;
  const applyCameraOffset = () => {
    camera.clearViewOffset();
    camera.filmOffset = 0;
    const latDeg = mobileMedia.matches ? mobileLatDeg : desktopLatDeg;
    const cameraDist = mobileMedia.matches ? mobileCameraDist : desktopCameraDist;
    const phiLat = (90.0 - latDeg) * DEG2RAD;
    camera.position.x = cameraDist * Math.cos(thetaLng) * Math.sin(phiLat);
    camera.position.z = cameraDist * Math.sin(thetaLng) * Math.sin(phiLat);
    camera.position.y = cameraDist * Math.cos(phiLat);
    if (mobileMedia.matches) {
      const w = containerRef.value?.clientWidth || 0;
      const h = containerRef.value?.clientHeight || 0;
      if (w > 0 && h > 0) {
        const fullHeight = h * 1.3;
        const yOffset = h * 0.3;
        camera.setViewOffset(w, fullHeight, 0, yOffset, w, h);
      }
    } else if (layout == "left") {
      camera.filmOffset = (-3 * camera.filmGauge) / 4;
    } else if (layout == "right") {
      camera.filmOffset = (3 * camera.filmGauge) / 4;
    }
    camera.updateProjectionMatrix();
    controls?.update();
  };
  applyCameraOffset();
  mobileMedia.addEventListener("change", applyCameraOffset);

  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "low-power" });
  renderer.setSize(width, height);
  containerRef.value.appendChild(renderer.domElement);

  const solidMeshMaterial = new THREE.MeshStandardMaterial({
    color: 0x222a35,
    opacity: 0.7,
    transparent: true,
  });

  const matLine = new LineMaterial({
    color: 0x4080ff,
    linewidth: 2,
    dashed: false,
  });

  const gltfLoader = new GLTFLoader();
  const loadGLTF = (url: string) =>
    new Promise<any>((resolve, reject) => {
      gltfLoader.load(url, resolve, undefined, reject);
    });

  const contourMaterial = new THREE.ShaderMaterial({
    uniforms: {
      peakY: { value: 0 },
      heightRange: { value: 1 },
      numContours: { value: 100 },
      peakBias: { value: 1.0 },
      colorLow: { value: new THREE.Color(0xA8612A) },
      colorMid: { value: new THREE.Color(0xE3C38C) },
      colorHigh: { value: new THREE.Color(0xF5B157) },
      colorPeak: { value: new THREE.Color(0xA5B2BE) },
    },
    vertexShader: `
      varying float vWorldY;
      void main() {
        vec4 worldPos = modelMatrix * vec4(position, 1.0);
        vWorldY = worldPos.y;
        gl_Position = projectionMatrix * viewMatrix * worldPos;
      }
    `,
    fragmentShader: `
      varying float vWorldY;
      uniform float peakY;
      uniform float heightRange;
      uniform float numContours;
      uniform float peakBias;
      uniform vec3 colorLow;
      uniform vec3 colorMid;
      uniform vec3 colorHigh;
      uniform vec3 colorPeak;
      void main() {
        float depth = max(peakY - vWorldY, 0.0) / heightRange;
        float scaled = pow(depth, peakBias) * numContours;
        float d = abs(fract(scaled - 0.5) - 0.5);
        float w = fwidth(scaled);
        float alpha = 1.0 - smoothstep(0.0, w, d);
        if (alpha < 0.01) discard;
        float t = clamp(1.0 - depth, 0.0, 1.0);
        vec3 color;
        if (t < 0.33) {
          color = mix(colorLow, colorMid, t / 0.33);
        } else if (t < 0.66) {
          color = mix(colorMid, colorHigh, (t - 0.33) / 0.33);
        } else {
          color = mix(colorHigh, colorPeak, (t - 0.66) / 0.34);
        }
        gl_FragColor = vec4(color, alpha);
      }
    `,
    transparent: true,
    side: THREE.DoubleSide,
  });

  const terrainMeshes: Array<{ mesh: THREE.Mesh; originalMaterial: THREE.Material | THREE.Material[] }> = [];
  let showTexturedTerrain = false;

  Promise.all([loadGLTF("/stylized_magellan.glb"), loadGLTF("/terrain.glb")])
    .then(([magellanGltf, terrainGltf]) => {
      // --- Terrain ---
      terrainGltf.scene.traverse((child: THREE.Object3D) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          terrainMeshes.push({ mesh, originalMaterial: mesh.material });
          mesh.material = contourMaterial;
        }
      });
      scene.add(terrainGltf.scene);
      terrainGltf.scene.updateMatrixWorld(true);

      const raycaster = new THREE.Raycaster();
      raycaster.set(new THREE.Vector3(0, 100000, 0), new THREE.Vector3(0, -1, 0));
      const originHits = raycaster.intersectObject(terrainGltf.scene, true);
      if (originHits.length > 0) {
        terrainGltf.scene.position.y -= originHits[0].point.y;
        terrainGltf.scene.updateMatrixWorld(true);
      }

      const bbox = new THREE.Box3().setFromObject(terrainGltf.scene);
      contourMaterial.uniforms.peakY.value = bbox.max.y;
      contourMaterial.uniforms.heightRange.value = Math.max(bbox.max.y - bbox.min.y, 0.001);

      // --- Telescope #1 at origin ---
      magellanGltf.scene.position.set(0, 0, 0);
      magellanGltf.scene.rotation.y = (5 * Math.PI) / 4;
      scene.add(magellanGltf.scene);
      magellanGltf.scene.updateMatrixWorld(true);

      const meshes: THREE.Mesh[] = [];
      magellanGltf.scene.traverse((child: THREE.Object3D) => {
        if ((child as THREE.Mesh).isMesh) {
          meshes.push(child as THREE.Mesh);
        }
      });
      const wireframeGroup = new THREE.Group();
      meshes.forEach((mesh) => {
        mesh.material = solidMeshMaterial;
        (mesh.material as THREE.Material).polygonOffset = true;
        (mesh.material as any).polygonOffsetFactor = 1.0;
        (mesh.material as any).polygonOffsetUnits = 1.0;
        const edges = new THREE.EdgesGeometry(mesh.geometry);
        edges.applyMatrix4(mesh.matrixWorld);
        const geometry = new LineSegmentsGeometry();
        geometry.fromEdgesGeometry(edges);
        const wireframe = new Wireframe(geometry, matLine);
        wireframe.computeLineDistances();
        wireframeGroup.add(wireframe);
      });
      scene.add(wireframeGroup);

      // --- Telescope #2: 55 m southeast (+X east, +Z south) ---
      const seDist = 55 / Math.SQRT2;
      raycaster.set(new THREE.Vector3(seDist, 100000, seDist), new THREE.Vector3(0, -1, 0));
      const seHits = raycaster.intersectObject(terrainGltf.scene, true);
      const seY = seHits.length > 0 ? seHits[0].point.y : 0;
      const sePos = new THREE.Vector3(seDist, seY, seDist);

      const magellan2 = magellanGltf.scene.clone(true);
      magellan2.position.copy(sePos);
      scene.add(magellan2);

      const wireframeGroup2 = wireframeGroup.clone(true);
      wireframeGroup2.position.copy(sePos);
      scene.add(wireframeGroup2);
    })
    .catch((error) => {
      console.error("Error loading GLB:", error);
    });

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "t" || e.key === "T") {
      showTexturedTerrain = !showTexturedTerrain;
      terrainMeshes.forEach(({ mesh, originalMaterial }) => {
        mesh.material = showTexturedTerrain ? originalMaterial : contourMaterial;
      });
    }
  };
  window.addEventListener("keydown", handleKeyDown);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;
  controls.autoRotate = true;
  controls.autoRotateSpeed = -0.75;

  // Responsive resize
  const handleResize = () => {
    const w = containerRef.value?.clientWidth || 0;
    const h = containerRef.value?.clientHeight || 0;
    camera.aspect = w / h;
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    applyCameraOffset();
  };
  window.addEventListener("resize", handleResize);

  let lastTimeStampMillis = 0;
  let timeStampMillis = 0;

  const millisPerFrame = 1000 / FRAMES_PER_SECOND;
  const animate = (dt: DOMHighResTimeStamp) => {
    lastTimeStampMillis = timeStampMillis;
    timeStampMillis = dt;
    const millisSinceLastFrame = dt - lastTimeStampMillis;
    const remainingMillisPerFrame = Math.max(0, millisPerFrame - millisSinceLastFrame);
    controls.update();
    renderer.render(scene, camera);
    if (throttleFrameRate) {
      setTimeout(() => {
        requestAnimationFrame(animate);
      }, remainingMillisPerFrame);
    } else {
      requestAnimationFrame(animate);
    }
  };

  handleResize();
  animate(0);

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
    window.removeEventListener("keydown", handleKeyDown);
    mobileMedia.removeEventListener("change", applyCameraOffset);
    renderer.dispose();
    containerRef.value?.removeChild(renderer.domElement);
  });
});
</script>

<template>
  <div ref="containerRef" class="telescope-model-container"></div>
</template>

<style lang="scss">
.telescope-model-container {
  width: 100%;
  height: 100%;
}
</style>
