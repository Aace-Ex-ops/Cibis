/**
 * Cibis AI Web Application Main Entrypoint
 */

import { ThreeFoodScene } from './threeScene.js';
import { initGsapAnimations } from './gsapAnimations.js';
import { CGMGlucoseChart } from './cgmChart.js';
import { FoodScannerManager } from './scanner.js';

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // 2. Initialize 3D Three.js Scene
  const threeScene = new ThreeFoodScene('webgl-canvas-container');

  // 3. Initialize GSAP ScrollTrigger Animations
  initGsapAnimations(threeScene);

  // 4. Initialize CGM Chart
  const cgmChart = new CGMGlucoseChart('cgmChart');

  // 5. Initialize Food Scanner Manager
  new FoodScannerManager(cgmChart);
});
