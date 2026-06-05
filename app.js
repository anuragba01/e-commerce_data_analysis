/* ================================================
   E-Commerce Analytics Dashboard — app.js
   Tab routing, theme, simulators, predictive form
   ================================================ */

// ---- Theme ----
function toggleTheme() {
  const html = document.documentElement;
  const icon = document.getElementById('themeIcon');
  if (html.classList.contains('dark')) {
    html.classList.remove('dark');
    icon.className = 'fa-solid fa-moon text-sm';
    localStorage.theme = 'light';
  } else {
    html.classList.add('dark');
    icon.className = 'fa-solid fa-sun text-sm';
    localStorage.theme = 'dark';
  }
  renderAllCharts();
}

// ---- Tab routing ----
function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById('tab-' + tabId).classList.add('active');
  const btn = document.getElementById('tabBtn-' + tabId);
  if (btn) btn.classList.add('active');
  if (['ds1','ds2','descriptive'].includes(tabId)) setTimeout(renderAllCharts, 50);
}

// ---- Discount Simulator Data ----
const discountSimTable = {
  0:  { revenue: 660.92, quantity: 2.74, profit: 267.51, margin: 40.1 },
  5:  { revenue: 589.89, quantity: 2.65, profit: 223.18, margin: 37.1 },
  10: { revenue: 542.04, quantity: 2.77, profit: 185.27, margin: 33.4 },
  15: { revenue: 530.01, quantity: 2.79, profit: 153.06, margin: 28.8 },
  20: { revenue: 500.79, quantity: 2.82, profit: 136.38, margin: 25.5 },
  25: { revenue: 427.53, quantity: 2.58, profit: 77.22,  margin: 19.9 },
  30: { revenue: 486.93, quantity: 2.73, profit: 65.27,  margin: 14.5 },
  35: { revenue: 455.00, quantity: 2.73, profit: 32.09,  margin: 7.0  },
  40: { revenue: 423.07, quantity: 2.74, profit: -1.09,  margin: 0.4  },
  45: { revenue: 376.00, quantity: 2.75, profit: -31.00, margin: -10.0 },
  50: { revenue: 329.80, quantity: 2.77, profit: -62.04, margin: -21.1 }
};

function updateDiscountSimulator(val) {
  const v = parseInt(val);
  document.getElementById('discountValDisplay').innerText = v + '%';
  const stats = discountSimTable[v]; if (!stats) return;
  document.getElementById('simRevenue').innerText  = '$' + stats.revenue.toFixed(2);
  const qtyEl = document.getElementById('simQuantity');
  if (qtyEl) qtyEl.innerText = stats.quantity.toFixed(2);
  const profitEl  = document.getElementById('simProfit');
  const marginEl  = document.getElementById('simMargin');
  const statusEl  = document.getElementById('simStatus');
  const noteEl    = document.getElementById('simNote');
  profitEl.innerText = (stats.profit >= 0 ? '$' : '-$') + Math.abs(stats.profit).toFixed(2);
  marginEl.innerText = stats.margin.toFixed(1) + '%';
  if (stats.margin > 20) {
    profitEl.className = 'text-sm font-bold text-emerald-600 dark:text-emerald-400';
    marginEl.className = 'text-5xl font-black text-emerald-600 dark:text-emerald-400 tracking-tight my-2 block';
    statusEl.className = 'px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase text-emerald-600 bg-emerald-500/10 dark:text-emerald-400';
    statusEl.innerText = 'Profitable Zone';
    noteEl.innerText   = 'Keep discounts under 30% to preserve reasonable net profit margins.';
  } else if (stats.margin > 5) {
    profitEl.className = 'text-sm font-bold text-amber-600 dark:text-amber-400';
    marginEl.className = 'text-5xl font-black text-amber-600 dark:text-amber-400 tracking-tight my-2 block';
    statusEl.className = 'px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase text-amber-600 bg-amber-500/10 dark:text-amber-400';
    statusEl.innerText = 'Caution Zone';
    noteEl.innerText   = 'Margins are dangerously thin. Consider limiting this tier to clearance only.';
  } else {
    profitEl.className = 'text-sm font-bold text-red-600 dark:text-red-400';
    marginEl.className = 'text-5xl font-black text-red-600 dark:text-red-400 tracking-tight my-2 block';
    statusEl.className = 'px-3 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase text-red-600 bg-red-500/10 dark:text-red-400';
    statusEl.innerText = 'Loss Territory';
    noteEl.innerText   = 'Net loss per transaction. Every sale at this discount destroys value.';
  }
}

// ---- Rating Delay Table (Dataset 2) ----
const ratingDelayTable = {
  5: { transit: '10.69 Days', delay: '-12.69 Days (Early)', late: '3.01%',  colorClass: 'text-emerald-600 dark:text-emerald-400' },
  4: { transit: '12.32 Days', delay: '-11.68 Days (Early)', late: '5.04%',  colorClass: 'text-emerald-600 dark:text-emerald-400' },
  3: { transit: '14.28 Days', delay: '-10.07 Days (Early)', late: '11.07%', colorClass: 'text-amber-600 dark:text-amber-400' },
  2: { transit: '16.73 Days', delay: '-7.82 Days (Early)',  late: '20.66%', colorClass: 'text-red-600 dark:text-red-400' },
  1: { transit: '21.31 Days', delay: '-3.35 Days (Early)',  late: '37.64%', colorClass: 'text-red-600 dark:text-red-400' }
};

function selectRatingScore(score) {
  document.querySelectorAll('.rate-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById('rateBtn-' + score).classList.add('active');
  const data = ratingDelayTable[score];
  document.getElementById('rateTransit').innerText = data.transit;
  const delayEl = document.getElementById('rateDelay');
  delayEl.innerText   = data.delay;
  delayEl.className   = 'text-sm font-bold ' + data.colorClass;
  const lateEl = document.getElementById('rateLate');
  lateEl.innerText  = data.late;
  lateEl.className  = 'text-sm font-bold ' + (score <= 2 ? 'text-red-600 dark:text-red-400' : 'text-emerald-600 dark:text-emerald-400');
}

// ---- Live Profit Margin Predictor (GB approximation) ----
// Approximation: Margin ≈ intercept + coef_discount*discount + coef_unitprice*unitprice_scaled
// Intercept from OLS (≈35 at 0 discount), dominant terms only
function predictMargin() {
  const discount = parseFloat(document.getElementById('pred_discount').value) / 100 || 0;
  const unitPrice = parseFloat(document.getElementById('pred_unitprice').value) || 200;
  const quantity  = parseFloat(document.getElementById('pred_quantity').value)  || 3;
  const costEl    = document.getElementById('pred_cost');
  const cost      = costEl ? (parseFloat(costEl.value) || 150) : 150;

  // GB learned relationship (approximated from model output):
  // Discount dominates at 85.4% importance
  // Marginal effects: each 10% discount ≈ -8.5pp margin (from bucket data)
  const baseMargin = 40.1;                         // 0% discount base
  const discEffect = discount * -110.06;           // LR coefficient is accurate here
  const qtyEffect  = (quantity - 2.74) * 0.376;
  const priceScaled = (unitPrice - 300) / 300;
  const priceEffect = priceScaled * 1.2;           // small positive effect

  let predicted = baseMargin + discEffect + qtyEffect + priceEffect;
  // clamp to realistic range
  predicted = Math.max(-40, Math.min(55, predicted));

  const el = document.getElementById('predResult');
  const label = document.getElementById('predLabel');
  el.innerText = predicted.toFixed(1) + '%';
  if (predicted > 20) {
    el.className = 'text-4xl font-black text-emerald-600 dark:text-emerald-400 my-1';
    label.innerText = '✓ Profitable';
    label.className = 'text-xs font-bold text-emerald-600 dark:text-emerald-400';
  } else if (predicted > 5) {
    el.className = 'text-4xl font-black text-amber-600 dark:text-amber-400 my-1';
    label.innerText = '⚠ Thin Margin';
    label.className = 'text-xs font-bold text-amber-600 dark:text-amber-400';
  } else {
    el.className = 'text-4xl font-black text-red-600 dark:text-red-400 my-1';
    label.innerText = '✗ Loss Likely';
    label.className = 'text-xs font-bold text-red-600 dark:text-red-400';
  }
}

// ---- Init ----
window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.theme === 'dark') {
    document.documentElement.classList.add('dark');
    document.getElementById('themeIcon').className = 'fa-solid fa-sun text-sm';
  }
  switchTab('ds1');
  renderAllCharts();
  updateDiscountSimulator(20);
  predictMargin();
});
