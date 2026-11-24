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
      document.getElementById('items-list').innerHTML = data.predictions.map((item, index) =>
        `<div class="prediction-row"><span class="prediction-rank">${String(index + 1).padStart(2, '0')}</span><strong>${item.name}</strong><span class="prediction-score">${(item.score * 100).toFixed(1)}%</span></div>`
      ).join('');
      const box = document.getElementById('macro-results');
      if (data.macro_match) {
        const m = data.macro_match.per_100g;
        box.innerHTML = `<div class="eyebrow">POSSIBLE USDA MATCH</div><h3>${data.macro_match.food_name}</h3><div class="macro-grid"><div><strong>${m.calories_kcal ?? '—'}</strong><span>kcal</span></div><div><strong>${m.protein_g ?? '—'} g</strong><span>protein</span></div><div><strong>${m.carbs_g ?? '—'} g</strong><span>carbs</span></div><div><strong>${m.fat_g ?? '—'} g</strong><span>fat</span></div></div><small>Per 100 g · USDA FDC #${data.macro_match.fdc_id}</small>`;
      } else {
        box.innerHTML = '<p class="empty-state">No nutrition match found for the top suggestion.</p>';
      }
      notice.textContent = data.notice;
    } catch (error) { notice.textContent = error.message; }
    finally { button.disabled = false; button.innerHTML = '<i data-lucide="scan-line"></i> Analyze photo'; window.lucide?.createIcons(); }
  });
});
