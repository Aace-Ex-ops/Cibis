/** Cibis food scan page interactions. */
document.addEventListener('DOMContentLoaded', () => {
  window.lucide?.createIcons();
  const form = document.getElementById('scan-form');
  const fileInput = document.getElementById('scan-image');
  const preview = document.getElementById('photo-preview');
  const previewImage = document.getElementById('preview-image');
  const notice = document.getElementById('scan-notice');
  let previewUrl;

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    if (!file) { preview.hidden = true; return; }
    previewUrl = URL.createObjectURL(file);
    previewImage.src = previewUrl;
    preview.hidden = false;
    notice.textContent = `${file.name} selected. Run the scan when ready.`;
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button');
    button.disabled = true;
    button.textContent = 'Analyzing photo…';
    notice.textContent = 'The first scan may take a few minutes while the food model downloads.';
    try {
      const response = await fetch('/api/scan', { method: 'POST', body: new FormData(form) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Scan failed. Please try again.');
      const dishRows = data.predictions.map((item, index) =>
        `<button class="prediction-row" type="button" data-food="${item.name}"><span class="prediction-rank">${String(index + 1).padStart(2, '0')}</span><strong>${item.name}</strong><span class="prediction-score">${(item.score * 100).toFixed(1)}%</span></button>`
      ).join('');
      const commonRows = data.common_foods.map((item, index) =>
        `<button class="prediction-row" type="button" data-food="${item.name}"><span class="prediction-rank">${String(index + 1).padStart(2, '0')}</span><strong>${item.name}</strong><span class="prediction-score">${(item.score * 100).toFixed(1)}%</span></button>`
      ).join('');
      document.getElementById('items-list').innerHTML = `<div class="eyebrow list-label">DISH SUGGESTIONS</div>${dishRows}<div class="eyebrow list-label">FRUITS & COMMON FOODS</div>${commonRows || '<p class="empty-state">No common food label detected.</p>'}`;
      document.querySelectorAll('.prediction-row').forEach(row => row.addEventListener('click', () => {
        document.querySelectorAll('.prediction-row').forEach(button => button.classList.toggle('selected', button === row));
        lookupNutrition(row.dataset.food);
      }));
      document.querySelector('.prediction-row')?.click();
      notice.textContent = data.notice;
    } catch (error) { notice.textContent = error.message; }
    finally { button.disabled = false; button.innerHTML = '<i data-lucide="scan-line"></i> Analyze photo'; window.lucide?.createIcons(); }
  });

  async function lookupNutrition(food) {
    const box = document.getElementById('macro-results');
    box.innerHTML = `<div class="eyebrow">USDA NUTRITION LOOKUP</div><h3>${food}</h3><label class="weight-label" for="serving-weight">Serving weight</label><div class="weight-control"><input id="serving-weight" type="number" min="1" max="5000" value="100"><span>grams</span><button id="weight-submit" class="nav-btn" type="button">Update</button></div><div id="portion-values" class="empty-state">Looking up a matching USDA food entry…</div>`;
    const run = async () => {
      const grams = document.getElementById('serving-weight').value;
      const output = document.getElementById('portion-values');
      output.textContent = 'Looking up USDA reference data…';
      try {
        const response = await fetch('/api/nutrition', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({food, grams}) });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Nutrition lookup failed');
        const m = result.portion;
        output.innerHTML = `<strong>Possible match: ${result.match.food_name}</strong><div class="macro-grid"><div><strong>${m.calories_kcal ?? '—'}</strong><span>kcal</span></div><div><strong>${m.protein_g ?? '—'} g</strong><span>protein</span></div><div><strong>${m.carbs_g ?? '—'} g</strong><span>carbs</span></div><div><strong>${m.fat_g ?? '—'} g</strong><span>fat</span></div></div><small>For ${result.grams} g · USDA FDC #${result.match.fdc_id}</small><p class="lookup-note">${result.notice}</p>`;
      } catch(error) { output.textContent = error.message; }
    };
    document.getElementById('weight-submit').addEventListener('click', run);
    run();
  }
});
