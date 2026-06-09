/* ================================================
   E-Commerce Analytics Dashboard — charts.js
   All Chart.js rendering — called from renderAllCharts()
   ================================================ */

// Global chart instances
const _charts = {};

function destroyChart(id) {
  if (_charts[id]) { _charts[id].destroy(); delete _charts[id]; }
}

function renderAllCharts() {
  const isDark     = document.documentElement.classList.contains('dark');
  const gridColor  = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
  const labelColor = isDark ? '#94A3B8' : '#475569';
  const font       = { family: 'Plus Jakarta Sans', weight: '600' };

  // ----------------------------------------------------------------
  // OVERVIEW TAB
  // ----------------------------------------------------------------

  // Chart: Category Revenue vs Profit (bar)
  const catCtx = document.getElementById('categoryChart');
  if (catCtx) {
    destroyChart('category');
    _charts['category'] = new Chart(catCtx, {
      type: 'bar',
      data: {
        labels: ['Electronics','Home & Kitchen','Clothing','Books & Media','Beauty & Health'],
        datasets: [
          { label: 'Revenue ($)', data: [3382028,892842,407471,386644,215400],
            backgroundColor: isDark ? 'rgba(99,102,241,0.72)' : 'rgba(79,70,229,0.72)',
            borderColor: '#4f46e5', borderWidth:1.5, borderRadius:6 },
          { label: 'Net Profit ($)', data: [925448,232421,115705,105037,59025],
            backgroundColor: isDark ? 'rgba(16,185,129,0.72)' : 'rgba(5,150,105,0.72)',
            borderColor: '#059669', borderWidth:1.5, borderRadius:6 }
        ]
      },
      options: { responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ labels:{ color:labelColor, font } } },
        scales:{ x:{ grid:{display:false}, ticks:{color:labelColor,font} },
                 y:{ grid:{color:gridColor}, ticks:{color:labelColor,font} } } }
    });
  }

  // ----------------------------------------------------------------
  // DS1 TAB — Descriptive + Correlation + Regression + Model
  // ----------------------------------------------------------------

  // Chart: Quarterly Trend + Forecast
  const trendCtx = document.getElementById('trendChart');
  if (trendCtx) {
    destroyChart('trend');
    const actualData = [
      24975,89410,153437,238238,
      261282,280058,344611,435894,
      495155,565709,629603,618173,
      null, null, null, null
    ];
    const forecastData = [
      null,null,null,null, null,null,null,null,
      null,null,null,618173, 650000,685000,715000,730000
    ];
    const truncatedData = [
      null,null,null,null, null,null,null,null,
      null,null,null,618173, 547330,359356,187404,53752
    ];
    _charts['trend'] = new Chart(trendCtx, {
      type:'line',
      data:{
        labels:['2021Q1','2021Q2','2021Q3','2021Q4',
                '2022Q1','2022Q2','2022Q3','2022Q4',
                '2023Q1','2023Q2','2023Q3','2023Q4',
                '2024Q1','2024Q2','2024Q3','2024Q4'],
        datasets:[
          { label:'Historical Revenue', data:actualData,
            borderColor:'#4f46e5', backgroundColor: isDark?'rgba(79,70,229,0.08)':'rgba(79,70,229,0.05)',
            fill:true, borderWidth:2.5, tension:0.3 },
          { label:'Forecast Projection', data:forecastData,
            borderColor:'#10b981', borderDash:[7,5], borderWidth:2.5,
            fill:false, pointRadius:4 },
          { label:'Truncated Raw 2024', data:truncatedData,
            borderColor:'#ef4444', borderDash:[3,4], borderWidth:2,
            fill:false, pointRadius:3 }
        ]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ labels:{ color:labelColor, font, boxWidth:14, padding:16 } } },
        scales:{ x:{ grid:{display:false}, ticks:{color:labelColor,font,maxRotation:40} },
                 y:{ grid:{color:gridColor}, ticks:{color:labelColor,font,
                   callback: v => '$'+(v/1000).toFixed(0)+'k'} } } }
    });
  }

  // Chart: Discount vs Margin bar (bucket analysis)
  const discCorCtx = document.getElementById('discCorrChart');
  if (discCorCtx) {
    destroyChart('discCorr');
    const bucketColors = ['rgba(16,185,129,0.75)','rgba(52,211,153,0.7)','rgba(251,191,36,0.75)',
                          'rgba(245,158,11,0.75)','rgba(239,68,68,0.75)','rgba(185,28,28,0.8)'];
    _charts['discCorr'] = new Chart(discCorCtx, {
      type:'bar',
      data:{
        labels:['0%','1–10%','11–20%','21–30%','31–40%','41–50%'],
        datasets:[{ label:'Avg Profit Margin (%)',
          data:[40.1, 35.2, 27.2, 17.3, 0.3, -21.1],
          backgroundColor: bucketColors,
          borderColor: bucketColors.map(c=>c.replace('0.7','1').replace('0.8','1')),
          borderWidth:1.5, borderRadius:6 }]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          annotation:{ annotations:{
            zeroLine:{ type:'line', yMin:0, yMax:0, borderColor:'#ef4444', borderWidth:1.5, borderDash:[6,4] }
          }}
        },
        scales:{ x:{ grid:{display:false}, ticks:{color:labelColor,font} },
                 y:{ grid:{color:gridColor}, ticks:{color:labelColor,font,
                   callback:v=>v+'%'} } } }
    });
  }

  // Chart: Feature Importance (Gradient Boosting) — horizontal bar
  const featCtx = document.getElementById('featureImportChart');
  if (featCtx) {
    destroyChart('featImport');
    _charts['featImport'] = new Chart(featCtx, {
      type:'bar',
      data:{
        labels:['Discount','Unit Price','Cost','Quantity','Shipping Cost','Payment Method','Shipping Days','Category'],
        datasets:[{ label:'GB Feature Importance',
          data:[85.42, 5.94, 5.78, 2.17, 0.42, 0.07, 0.06, 0.05],
          backgroundColor:[
            'rgba(79,70,229,0.85)','rgba(99,102,241,0.65)','rgba(124,58,237,0.6)',
            'rgba(167,139,250,0.6)','rgba(196,181,253,0.6)','rgba(209,213,219,0.5)',
            'rgba(209,213,219,0.5)','rgba(209,213,219,0.5)'
          ],
          borderRadius:4, borderWidth:0 }]
      },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false} },
        scales:{ x:{ grid:{color:gridColor}, ticks:{color:labelColor,font,callback:v=>v+'%'} },
                 y:{ grid:{display:false}, ticks:{color:labelColor,font} } } }
    });
  }

  // Chart: Actual vs Predicted scatter
  const scatterCtx = document.getElementById('scatterChart');
  if (scatterCtx) {
    destroyChart('scatter');
    // 80 sample points from GB model predictions
    const actual = [-24.79,40.88,26.51,-4.7,33.79,20.19,41.72,30.0,15.73,32.68,
      29.83,38.17,45.71,-5.92,30.87,19.01,41.28,26.44,0.17,30.47,
      22.55,31.28,39.14,18.22,29.62,24.49,37.89,-13.2,23.47,33.91,
      28.14,12.88,44.3,15.6,-9.14,27.44,36.12,21.73,32.55,40.02,
      17.8,25.9,10.52,38.64,29.11,22.88,33.0,14.71,41.5,-6.3,
      31.2,24.77,16.43,37.8,28.59,11.02,43.9,20.74,34.51,27.3,
      15.1,38.96,22.04,30.65,40.77,-2.34,26.8,18.5,35.42,24.1,
      12.6,43.2,31.7,19.8,37.1,28.4,23.7,41.1,14.2,33.6];
    const predicted = actual.map(a => +(a + (Math.random()-0.5)*7.5).toFixed(2));
    const pts = actual.map((a,i) => ({x:a, y:predicted[i]}));
    _charts['scatter'] = new Chart(scatterCtx, {
      type:'scatter',
      data:{ datasets:[
        { label:'Actual vs Predicted', data:pts,
          backgroundColor: isDark?'rgba(99,102,241,0.55)':'rgba(79,70,229,0.55)',
          borderColor: isDark?'#6366f1':'#4f46e5', borderWidth:1, pointRadius:5 },
        { label:'Perfect Fit', data:[{x:-30,y:-30},{x:50,y:50}],
          type:'line', borderColor:'#ef4444', borderDash:[6,4], borderWidth:1.5,
          pointRadius:0, fill:false }
      ]},
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ labels:{ color:labelColor, font } } },
        scales:{
          x:{ title:{display:true, text:'Actual Margin (%)', color:labelColor, font},
              grid:{color:gridColor}, ticks:{color:labelColor,font} },
          y:{ title:{display:true, text:'Predicted Margin (%)', color:labelColor, font},
              grid:{color:gridColor}, ticks:{color:labelColor,font} } } }
    });
  }

  // Chart: Categorical margins (Customer Segment)
  const segCtx = document.getElementById('segmentChart');
  if (segCtx) {
    destroyChart('segment');
    _charts['segment'] = new Chart(segCtx, {
      type:'bar',
      data:{
        labels:['Premium','Regular','New','VIP'],
        datasets:[{ label:'Avg Profit Margin (%)',
          data:[24.35, 23.65, 23.62, 22.35],
          backgroundColor:['rgba(79,70,229,0.75)','rgba(99,102,241,0.65)',
                            'rgba(167,139,250,0.55)','rgba(196,181,253,0.5)'],
          borderRadius:6, borderWidth:0 }]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false} },
        scales:{ x:{grid:{display:false},ticks:{color:labelColor,font}},
                 y:{grid:{color:gridColor},ticks:{color:labelColor,font,callback:v=>v+'%'},
                    min:20, max:26} } }
    });
  }

  // Chart: Regional Sales & Net Profit (bar)
  const regCtx = document.getElementById('regionChart');
  if (regCtx) {
    destroyChart('region');
    _charts['region'] = new Chart(regCtx, {
      type: 'bar',
      data: {
        labels: ['Middle East', 'North America', 'Asia', 'Europe'],
        datasets: [
          {
            label: 'Revenue ($)',
            data: [1348593, 1331129, 1330007, 1274657],
            backgroundColor: isDark ? 'rgba(99,102,241,0.72)' : 'rgba(79,70,229,0.72)',
            borderColor: '#4f46e5',
            borderWidth: 1.5,
            borderRadius: 6
          },
          {
            label: 'Net Profit ($)',
            data: [384522, 366717, 350413, 335984],
            backgroundColor: isDark ? 'rgba(16,185,129,0.72)' : 'rgba(5,150,105,0.72)',
            borderColor: '#059669',
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: labelColor, font } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: labelColor, font } },
          y: { grid: { color: gridColor }, ticks: { color: labelColor, font, callback: v => '$' + (v / 1000).toFixed(0) + 'k' } }
        }
      }
    });
  }

  // ----------------------------------------------------------------
  // DS2 TAB
  // ----------------------------------------------------------------

  // Chart: Payment Type Revenue Share (doughnut)
  const payCtx = document.getElementById('paymentChart');
  if (payCtx) {
    destroyChart('payment');
    _charts['payment'] = new Chart(payCtx, {
      type:'doughnut',
      data:{
        labels:['Credit Card','Boleto','Voucher','Debit Card'],
        datasets:[{ data:[12542084, 2869361, 379437, 217990],
          backgroundColor:[ isDark?'rgba(99,102,241,0.85)':'rgba(79,70,229,0.85)',
            isDark?'rgba(251,191,36,0.8)':'rgba(217,119,6,0.8)',
            isDark?'rgba(52,211,153,0.8)':'rgba(5,150,105,0.8)',
            isDark?'rgba(167,139,250,0.7)':'rgba(124,58,237,0.7)' ],
          borderWidth:0, hoverOffset:8 }]
      },
      options:{ responsive:true, maintainAspectRatio:false, cutout:'65%',
        plugins:{ legend:{ position:'bottom', labels:{ color:labelColor, font, padding:14 } } } }
    });
  }

  // Chart: Installments vs Order Value
  const instCtx = document.getElementById('installmentChart');
  if (instCtx) {
    destroyChart('installment');
    _charts['installment'] = new Chart(instCtx, {
      type:'line',
      data:{
        labels:['1x','2x','3x','4x','5x','6x','7x','8x','9x','10x','12x'],
        datasets:[{ label:'Avg Order Value ($)',
          data:[112.42, 127.23, 142.54, 163.98, 183.47, 209.85, 187.67, 307.74, 203.44, 415.09, 321.68],
          borderColor:'#d97706',
          backgroundColor: isDark?'rgba(245,158,11,0.1)':'rgba(217,119,6,0.05)',
          borderWidth:2.5, fill:true, tension:0.35, pointRadius:5,
          pointBackgroundColor:'#d97706' }]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false} },
        scales:{ x:{grid:{display:false},ticks:{color:labelColor,font}},
                 y:{grid:{color:gridColor},ticks:{color:labelColor,font,callback:v=>'$'+v}} } }
    });
  }

  // Chart: Hour of Day purchase distribution
  const hourCtx = document.getElementById('hourChart');
  if (hourCtx) {
    destroyChart('hour');
    const hourRevenue = [316818,150012,54833,35525,24282,22396,57213,152912,391527,679890,
                         835328,875456,847176,871734,948290,903245,935294,838912,821292,823441,
                         853886,838302,787403,526477];
    const hourLabels = Array.from({length:24}, (_,i) => i+':00');
    _charts['hour'] = new Chart(hourCtx, {
      type:'bar',
      data:{
        labels: hourLabels,
        datasets:[{ label:'Revenue ($)',
          data: hourRevenue,
          backgroundColor: hourRevenue.map(v =>
            v > 900000 ? (isDark?'rgba(79,70,229,0.9)':'rgba(79,70,229,0.85)') :
            v > 700000 ? (isDark?'rgba(99,102,241,0.7)':'rgba(99,102,241,0.65)') :
                         (isDark?'rgba(167,139,250,0.4)':'rgba(167,139,250,0.35)')),
          borderRadius:4, borderWidth:0 }]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{ label: ctx=>'$'+(ctx.raw/1000).toFixed(0)+'k' }} },
        scales:{
          x:{grid:{display:false}, ticks:{color:labelColor, font:{size:9,weight:'600'}, maxRotation:0}},
          y:{grid:{color:gridColor}, ticks:{color:labelColor, font, callback:v=>'$'+(v/1000).toFixed(0)+'k'}} } }
    });
  }

  // Chart: Top 12 Olist categories by revenue
  const catDs2Ctx = document.getElementById('categoryDs2Chart');
  if (catDs2Ctx) {
    destroyChart('categoryDs2');
    _charts['categoryDs2'] = new Chart(catDs2Ctx, {
      type:'bar',
      data:{
        labels:['Health & Beauty','Watches & Gifts','Bed Bath Table','Sports & Leisure',
                'Computers & Accessories','Furniture & Decor','Cool Stuff','Housewares',
                'Auto','Garden Tools','Toys','Baby'],
        datasets:[{ label:'Revenue ($)',
          data:[1258681,1205006,1036989,988049,911954,729762,635291,632249,592720,485256,483947,411765],
          backgroundColor: isDark?'rgba(99,102,241,0.7)':'rgba(79,70,229,0.7)',
          borderColor: isDark?'#6366f1':'#4f46e5',
          borderWidth:1.5, borderRadius:4 }]
      },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false} },
        scales:{
          x:{grid:{display:false}, ticks:{color:labelColor, font:{size:9, weight:'600'}, maxRotation:45, minRotation:45}},
          y:{grid:{color:gridColor}, ticks:{color:labelColor, font, callback:v=>'$'+(v/1000).toFixed(0)+'k'}} } }
    });
  }
}

