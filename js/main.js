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
  const form = document.getElementById('scan-form');
  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const notice = document.getElementById('scan-notice');
    notice.textContent = 'Analyzing…';
    try {
      const response = await fetch('/api/scan', { method: 'POST', body: new FormData(form) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Scan failed');
      const rows = data.predictions.map(item => `<div class="food-item-row"><span>${item.name}</span><span class="food-item-stats">Model score: ${(item.score * 100).toFixed(1)}%</span></div>`).join('');
      document.getElementById('items-list').innerHTML = rows;
      const macroBox = document.getElementById('macro-results');
      if (data.macro_match) {
        const m = data.macro_match.per_100g;
        macroBox.innerHTML = `<strong>Possible USDA match: ${data.macro_match.food_name}</strong><p>Per 100 g: ${m.calories_kcal ?? '—'} kcal · Protein ${m.protein_g ?? '—'} g · Carbohydrates ${m.carbs_g ?? '—'} g · Fat ${m.fat_g ?? '—'} g</p><small>Source: USDA FoodData Central (FDC ID ${data.macro_match.fdc_id}). Check that the match fits your food. Values are not portion totals.</small>`;
      } else {
        macroBox.textContent = 'No USDA macro match found for this prediction.';
      }
      notice.textContent = data.notice;
    } catch (error) { notice.textContent = error.message; }
  });
});
