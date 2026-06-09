<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import type * as THREE from "three";
import * as solar from "solar-calculator";

const containerRef = ref<HTMLElement | null>(null);
const dateTextRef = ref<HTMLElement | null>(null);
const lcoLat = -29.014026993317913,
  lcoLng = -70.69271530816395;

interface Star {
  id: number;
  name: string;
  ra: number;
  dec: number;
  vmag: number;
}

const DEG2RAD = Math.PI / 180.0;
const CELESTIAL_SPHERE_RADIUS = 100;
const FRAMES_PER_SECOND = 24.0;
const throttleFrameRate = true;

function vertexShader() {
  return `
        attribute float size;
        attribute vec4 color;
        varying vec4 vColor;
        void main() {
            vColor = color;
            vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 );
            gl_PointSize = 2.0;
            gl_Position = projectionMatrix * mvPosition;
        }
    `;
}

function fragmentShader() {
  return `
        varying vec4 vColor;
            void main() {
                gl_FragColor = vec4( vColor );
            }
    `;
}

onMounted(async () => {
  if (!containerRef.value) return;
  if (!dateTextRef.value) return;

  const THREE = await import("three");

  const { OrbitControls } = await import("three/examples/jsm/controls/OrbitControls.js");
  const ThreeGlobe = (await import("three-globe")).default;

  class StarField extends THREE.Points {
    constructor(stars: Array<Star>) {
      const positions: Array<number> = [];
      const colors: Array<number> = [];
      const sizes: Array<number> = [];
      const color = new THREE.Color().setHex(0xffffff);
      stars.forEach((star) => {
        const phi = DEG2RAD * (90 - star.dec);
        const theta = DEG2RAD * star.ra;
        const x = CELESTIAL_SPHERE_RADIUS * Math.cos(theta) * Math.sin(phi);
        positions.push(x);
        const y = CELESTIAL_SPHERE_RADIUS * Math.sin(theta) * Math.sin(phi);
        positions.push(y);
        const z = CELESTIAL_SPHERE_RADIUS * Math.cos(phi);
        positions.push(z);

        const size = (star.vmag * 26) / 255 + 0.18;

        colors.push(color.r);
        colors.push(color.g);
        colors.push(color.b);
        colors.push(size);
        sizes.push(size);
      });

      const starsGeometry = new THREE.BufferGeometry();
      starsGeometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
      starsGeometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 4));
      starsGeometry.setAttribute("size", new THREE.Float32BufferAttribute(sizes, 1));

      const starsMaterial = new THREE.ShaderMaterial({
        vertexShader: vertexShader(),
        fragmentShader: fragmentShader(),
        transparent: true,
      });
      super(starsGeometry, starsMaterial);
    }
  }

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x101020);

  // Camera
  const width = containerRef.value.clientWidth;
  const height = containerRef.value.clientHeight;
  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);

  camera.filmGauge = 35;

  const phiLatDeg = Math.abs(lcoLat) - 30,
    thetaLngDeg = lcoLng;
  const phiLat = DEG2RAD * phiLatDeg,
    thetaLng = DEG2RAD * thetaLngDeg;

  const mobileMedia = window.matchMedia("(max-width: 768px)");

  // Desktop frames the globe tightly (paired with a horizontal filmOffset
  // shift so the overlay sits beside it). Mobile stacks the overlay below
  // the globe in normal flow, so the camera pulls back to fit the entire
  // sphere with a small margin inside whatever aspect the container has.
  const GLOBE_RADIUS = 100;
  const computeCameraDistance = (): number => {
    if (!mobileMedia.matches) return 180;
    const w = containerRef.value?.clientWidth || 0;
    const h = containerRef.value?.clientHeight || 0;
    if (w === 0 || h === 0) return 240;
    const fovRad = camera.fov * DEG2RAD;
    const aspect = w / h;
    const hFovRad = 2 * Math.atan(Math.tan(fovRad / 2) * aspect);
    const limitingHalfFov = Math.min(fovRad / 2, hFovRad / 2);
    const targetFraction = 0.8;
    return GLOBE_RADIUS / Math.sin(targetFraction * limitingHalfFov);
  };

  const positionCamera = () => {
    const dist = computeCameraDistance();
    camera.position.x = dist * Math.cos(phiLat) * Math.sin(thetaLng);
    camera.position.y = dist * Math.sin(phiLat) * Math.sin(thetaLng);
    camera.position.z = dist * Math.cos(thetaLng);
  };
  positionCamera();

  // Scale the camera radially to a new distance without resetting the
  // user's orbit rotation — used on plain resize (e.g. browser window).
  const setCameraDistance = (dist: number) => {
    const len = camera.position.length();
    if (len === 0) positionCamera();
    else camera.position.multiplyScalar(dist / len);
  };

  const applyCameraOffset = () => {
    camera.clearViewOffset();
    camera.filmOffset = mobileMedia.matches ? 0 : (3 * camera.filmGauge) / 4;
    camera.updateProjectionMatrix();
  };
  applyCameraOffset();
  mobileMedia.addEventListener("change", () => {
    positionCamera();
    applyCameraOffset();
  });

  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "low-power" });
  renderer.setSize(width, height);
  containerRef.value.appendChild(renderer.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  // Compute the sun's sub-solar point (lng, lat) at a given JS Date / millis.
  // Same formulation as three-globe's day-night-cycle example.
  const sunPosAt = (dt: number | Date): [number, number] => {
    const ms = +dt;
    const day = new Date(ms).setUTCHours(0, 0, 0, 0);
    const t = solar.century(ms);
    const longitude = ((day - ms) / 864e5) * 360 - 180;
    return [longitude - solar.equationOfTime(t) / 4, solar.declination(t)];
  };

  const timeEl = dateTextRef.value;

  const arcsData = [
    // Flatiron Institute, New York, New York, USA
    {
      startLat: 40.7405113959079,
      startLng: -73.99091302611822,
      endLat: lcoLat,
      endLng: lcoLng,
      color: "#ce3232",
    },
    // Steward Observatory, Tucson, Arizona, USA
    {
      startLat: 32.23295846381152,
      startLng: -110.9484604795582,
      endLat: lcoLat,
      endLng: lcoLng,
      color: "#AB0520",
    },
    // Leiden Observatory, Leiden, the Netherlands
    {
      startLat: 52.16774442720691,
      startLng: 4.461019002337261,
      endLat: lcoLat,
      endLng: lcoLng,
      color: "#42b9ff",
    },
    // UMich Astro, Ann Arbor, Michigan, USA
    {
      startLat: 42.27573454127685,
      startLng: -83.73621881408133,
      endLat: lcoLat,
      endLng: lcoLng,
      color: "#ffcb05",
    },
    // Carnegie EPL, Washington D.C., USA
    {
      startLat: 38.958779377779265,
      startLng: -77.06277220851486,
      endLat: lcoLat,
      endLng: lcoLng,
      color: "#efefef",
    },
  ];

  const Globe = new ThreeGlobe()
    .bumpImageUrl("/earth-topology.png")
    .arcsData(arcsData)
    .arcStroke(0.7)
    .arcColor("color")
    .arcDashLength(0.05)
    .arcDashGap(0.025)
    .arcDashAnimateTime(50000);

  // Day/night blended shader for the globe surface — adapted from
  // three-globe's day-night-cycle example.
  const dayNightShader = {
    vertexShader: `
      varying vec3 vNormal;
      varying vec2 vUv;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      #define PI 3.141592653589793
      uniform sampler2D dayTexture;
      uniform sampler2D nightTexture;
      uniform vec2 sunPosition;
      uniform vec2 globeRotation;
      varying vec3 vNormal;
      varying vec2 vUv;

      float toRad(in float a) {
        return a * PI / 180.0;
      }

      vec3 Polar2Cartesian(in vec2 c) { // [lng, lat]
        float theta = toRad(90.0 - c.x);
        float phi = toRad(90.0 - c.y);
        return vec3(
          sin(phi) * cos(theta),
          cos(phi),
          sin(phi) * sin(theta)
        );
      }

      void main() {
        float invLon = toRad(globeRotation.x);
        float invLat = -toRad(globeRotation.y);
        mat3 rotX = mat3(
          1, 0, 0,
          0, cos(invLat), -sin(invLat),
          0, sin(invLat), cos(invLat)
        );
        mat3 rotY = mat3(
          cos(invLon), 0, sin(invLon),
          0, 1, 0,
          -sin(invLon), 0, cos(invLon)
        );
        vec3 rotatedSunDirection = rotX * rotY * Polar2Cartesian(sunPosition);
        float intensity = dot(normalize(vNormal), normalize(rotatedSunDirection));
        vec4 dayColor = texture2D(dayTexture, vUv);
        vec4 nightColor = texture2D(nightTexture, vUv);
        float blendFactor = smoothstep(-0.1, 0.1, intensity);
        gl_FragColor = mix(nightColor, dayColor, blendFactor);
        #include <colorspace_fragment>
      }
    `,
  };

  let globeMaterial: THREE.ShaderMaterial | null = null;
  const textureLoader = new THREE.TextureLoader();
  Promise.all([
    textureLoader.loadAsync("/earth-day.jpg"),
    textureLoader.loadAsync("/earth-night.jpg"),
  ])
    .then(([dayTexture, nightTexture]) => {
      // r152+: color textures need to be marked sRGB or they render dark/black
      // once sampled into a linear-workflow shader.
      dayTexture.colorSpace = THREE.SRGBColorSpace;
      nightTexture.colorSpace = THREE.SRGBColorSpace;
      const { lng: camLng, lat: camLat } = Globe.toGeoCoords(camera.position);
      globeMaterial = new THREE.ShaderMaterial({
        uniforms: {
          dayTexture: { value: dayTexture },
          nightTexture: { value: nightTexture },
          sunPosition: { value: new THREE.Vector2(...sunPosAt(Date.now())) },
          globeRotation: { value: new THREE.Vector2(camLng, camLat) },
        },
        vertexShader: dayNightShader.vertexShader,
        fragmentShader: dayNightShader.fragmentShader,
      });
      Globe.globeMaterial(globeMaterial);
    })
    .catch((err) => {
      console.error("StarGlobe: failed to load earth textures", err);
    });

  scene.add(Globe);
  scene.add(new THREE.AmbientLight(0xcccccc, Math.PI));
  scene.add(new THREE.DirectionalLight(0xffffff, 0.6 * Math.PI));

  // Orbit Controls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.zoomSpeed = 4;
  controls.enableZoom = false;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0.5;
  controls.addEventListener("change", () => {
    // Pass the current camera-relative globe orientation to the shader so
    // the sun direction stays correctly oriented as the user orbits.
    if (!globeMaterial) return;
    const { lng, lat } = Globe.toGeoCoords(camera.position);
    globeMaterial.uniforms.globeRotation.value.set(lng, lat);
  });

  // Responsive resize
  const handleResize = () => {
    const w = containerRef.value?.clientWidth || 0;
    const h = containerRef.value?.clientHeight || 0;
    camera.aspect = w / h;
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    setCameraDistance(computeCameraDistance());
    applyCameraOffset();
  };
  window.addEventListener("resize", handleResize);

  // Animation loop
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
    // Push current real-time sun position into the day/night shader.
    if (globeMaterial) {
      const now = Date.now();
      globeMaterial.uniforms.sunPosition.value.set(...sunPosAt(now));
      timeEl.textContent = new Date(now).toLocaleString();
    }
    if (throttleFrameRate) {
      setTimeout(() => {
        requestAnimationFrame(animate);
      }, remainingMillisPerFrame);
    } else {
      requestAnimationFrame(animate);
    }
  };

  fetch("/brightStarCatalog_v_gt_11.json")
    .then((response) => response.json())
    .then((stars: Array<Star>) => {
      const starField = new StarField(stars);
      starField.scale.multiplyScalar(5);
      scene.add(starField);
      handleResize();
      animate(0);
    });
  animate(0);

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
    mobileMedia.removeEventListener("change", applyCameraOffset);
    renderer.dispose();
    containerRef.value?.removeChild(renderer.domElement);
  });
});
</script>

<template>
  <div class="star-globe-wrapper">
    <div ref="containerRef" class="star-globe-container"></div>
    <div ref="dateTextRef" class="date-text"></div>
  </div>
</template>

<style lang="scss">
.star-globe-wrapper {
  width: 100%;
  height: 100%;

  .date-text {
    position: absolute;
    bottom: 0;
    left: 0;
  }
}

.star-globe-container {
  width: 100%;
  height: 100%;
}
</style>
