/**
 * Chart.js 120-Minute Postprandial CGM Blood Glucose Simulation
 */

export class CGMGlucoseChart {
  constructor(canvasId) {
    this.ctx = document.getElementById(canvasId).getContext('2d');
    this.timeLabels = Array.from({ length: 25 }, (_, i) => `${i * 5}m`);
    this.chart = this.initChart();
  }

  initChart() {
    return new Chart(this.ctx, {
      type: 'line',
      data: {
        labels: this.timeLabels,
        datasets: [
          {
            label: 'Predicted Glucose Response (mg/dL)',
            data: [90, 91.2, 92.5, 94.0, 95.3, 96.4, 97.1, 96.8, 96.0, 95.1, 94.0, 93.1, 92.2, 91.5, 90.9, 90.5, 90.2, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0],
            borderColor: '#00f2ff',
            backgroundColor: 'rgba(0, 242, 255, 0.08)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: '#00f2ff',
          },
          {
            label: 'Fasting Baseline (90 mg/dL)',
            data: Array(25).fill(90),
            borderColor: 'rgba(255, 255, 255, 0.25)',
            borderDash: [5, 5],
            borderWidth: 1.5,
            pointRadius: 0,
            fill: false,
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12 } }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
          },
          y: {
            min: 70,
            max: 160,
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
          }
        }
      }
    });
  }

  updateData(newData) {
    this.chart.data.datasets[0].data = newData;
    this.chart.update();
  }
}
