/**
 * Food Scanner Telemetry & Test Case Controller
 */

export const testCases = {
  thali: {
    title: "Indian Thali Lunch Tray",
    itemsCount: "4 Compartments Identified",
    image: "thali_scanned_result.jpg",
    mass: "496.5 g",
    calories: "740.3 kcal",
    protein: "61.6 g",
    carbs: "34.7 g",
    gastricNote: "High protein (61.6g) and fiber slow digestion by 4.05x, eliminating glucose spikes.",
    items: [
      { name: "🥩 Spiced Shredded Sabzi", stats: "181.1g | 335.0 kcal | 38.9g Protein" },
      { name: "🥚 Egg Masala (2 Eggs)", stats: "153.2g | 237.4 kcal | 17.2g Protein" },
      { name: "🫓 Whole Wheat Roti (2 pcs)", stats: "49.7g | 147.6 kcal | 23.0g Net Carbs" },
      { name: "🥗 Cucumber & Onion Salad", stats: "112.6g | 20.3 kcal | 1.4g Fiber" }
    ],
    cgmData: [90, 91.2, 92.5, 94.0, 95.3, 96.4, 97.1, 96.8, 96.0, 95.1, 94.0, 93.1, 92.2, 91.5, 90.9, 90.5, 90.2, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
  },
  fruit: {
    title: "Fresh Fruit Basket Still-Life",
    itemsCount: "5 Produce Items Identified",
    image: "scanned_nutrition_result.jpg",
    mass: "923.7 g",
    calories: "463.7 kcal",
    protein: "5.9 g",
    carbs: "102.2 g",
    gastricNote: "High sugar in grapes causes a predicted spike to 137.5 mg/dL at 35 mins.",
    items: [
      { name: "🍊 Mandarin Orange", stats: "76.4g | 35.9 kcal | 40.6mg Vit C" },
      { name: "🍓 Strawberries (Bowl)", stats: "350.8g | 112.2 kcal | 206.3mg Vit C" },
      { name: "🍇 Green Seedless Grapes", stats: "306.2g | 211.3 kcal | 47.4g Sugar" },
      { name: "🍎 Red Fuji Apple", stats: "84.0g | 43.7 kcal | 2.0g Fiber" },
      { name: "🍐 Yellow Bartlett Pear", stats: "106.3g | 60.6 kcal | 3.3g Fiber" }
    ],
    cgmData: [90, 98.4, 114.2, 129.5, 137.5, 135.0, 126.8, 118.0, 110.2, 104.5, 99.8, 96.4, 94.0, 92.5, 91.4, 90.8, 90.4, 90.2, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
  }
};

export class FoodScannerManager {
  constructor(cgmChart) {
    this.cgmChart = cgmChart;
    this.initButtons();
    this.selectTestCase('thali');
  }

  initButtons() {
    const tabThali = document.getElementById('tab-thali');
    const tabFruit = document.getElementById('tab-fruit');

    if (tabThali) tabThali.addEventListener('click', () => this.selectTestCase('thali'));
    if (tabFruit) tabFruit.addEventListener('click', () => this.selectTestCase('fruit'));
  }

  selectTestCase(key) {
    const data = testCases[key];
    if (!data) return;

    const tabThali = document.getElementById('tab-thali');
    const tabFruit = document.getElementById('tab-fruit');
    if (tabThali) tabThali.classList.toggle('active', key === 'thali');
    if (tabFruit) tabFruit.classList.toggle('active', key === 'fruit');

    const imgDisplay = document.getElementById('scanner-image-display');
    if (imgDisplay) imgDisplay.src = data.image;

    document.getElementById('telemetry-meal-title').textContent = data.title;
    document.getElementById('telemetry-items-count').textContent = data.itemsCount;
    document.getElementById('stat-mass').textContent = data.mass;
    document.getElementById('stat-calories').textContent = data.calories;
    document.getElementById('stat-protein').textContent = data.protein;
    document.getElementById('stat-carbs').textContent = data.carbs;
    document.getElementById('cgm-gastric-note').textContent = data.gastricNote;

    const listContainer = document.getElementById('items-list');
    if (listContainer) {
      listContainer.innerHTML = data.items.map(it => `
        <div class="food-item-row">
          <span>${it.name}</span>
          <span class="food-item-stats">${it.stats}</span>
        </div>
      `).join('');
    }

    if (this.cgmChart) {
      this.cgmChart.updateData(data.cgmData);
    }
  }
}
