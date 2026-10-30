// RoadVision AI - Intelligent Road Condition Classification System for Indian Roads
// Civil Engineering & AIML Mini Project (CO3 & CO4)
// Complies with IRC:82-2015, IRC:37-2018 & MoRTH Guidelines

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initFormBindings();
  initPresets();
  initClassifier();
  initDatasetExplorer();
  initCharts();
  initConfusionMatrix();
  initTestComparisonTable();
  initModals();
  initTeamPersistence();
});

/* =========================================================
   1. NAVIGATION & ACTIVE SCROLL TRACKER
   ========================================================= */
function initNavigation() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      const isVisible = navLinks.style.display === 'flex';
      navLinks.style.display = isVisible ? 'none' : 'flex';
      if (!isVisible) {
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '100%';
        navLinks.style.left = '0';
        navLinks.style.width = '100%';
        navLinks.style.background = '#0d1527';
        navLinks.style.padding = '20px';
        navLinks.style.borderBottom = '2px solid var(--road-yellow)';
      }
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          navLinks.style.display = 'none';
        }
      });
    });
  }

  // Active section indicator on scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const navItem = document.querySelector(`.nav-links a[href*="${sectionId}"]`);
      
      if (navItem) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navItem.classList.add('active');
        } else {
          navItem.classList.remove('active');
        }
      }
    });
  });
}

/* =========================================================
   2. INPUT SYNCHRONIZATION (SLIDERS & NUMBER BOXES)
   ========================================================= */
const inputsConfig = [
  { sliderId: 'slider-iri', numId: 'num-iri', default: 2.4 },
  { sliderId: 'slider-potholes', numId: 'num-potholes', default: 1 },
  { sliderId: 'slider-cracks', numId: 'num-cracks', default: 4.5 },
  { sliderId: 'slider-rutting', numId: 'num-rutting', default: 3.2 },
  { sliderId: 'slider-age', numId: 'num-age', default: 2.0 },
  { sliderId: 'slider-traffic', numId: 'num-traffic', default: 16500 }
];

function initFormBindings() {
  inputsConfig.forEach(item => {
    const slider = document.getElementById(item.sliderId);
    const num = document.getElementById(item.numId);
    if (!slider || !num) return;

    slider.addEventListener('input', () => {
      num.value = slider.value;
      clearPresetActiveState();
    });

    num.addEventListener('input', () => {
      slider.value = num.value;
      clearPresetActiveState();
    });
  });

  const drainageSelect = document.getElementById('select-drainage');
  if (drainageSelect) {
    drainageSelect.addEventListener('change', () => {
      clearPresetActiveState();
    });
  }
}

function clearPresetActiveState() {
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
}

/* =========================================================
   3. INDIAN ROAD DEMONSTRATION PRESETS
   ========================================================= */
const PRESETS = {
  good: {
    iri: 1.8,
    potholes: 0,
    cracks: 2.5,
    rutting: 2.2,
    age: 1.2,
    drainage: 'Good',
    traffic: 22000,
    label: 'NH-48 Pune-Bengaluru 6-Lane Expressway (Good)'
  },
  fair: {
    iri: 4.2,
    potholes: 3,
    cracks: 12.0,
    rutting: 8.5,
    age: 4.5,
    drainage: 'Moderate',
    traffic: 34000,
    label: 'Mumbai Western Express Highway Arterial (Fair)'
  },
  poor: {
    iri: 6.8,
    potholes: 8,
    cracks: 26.0,
    rutting: 15.5,
    age: 8.0,
    drainage: 'Poor',
    traffic: 18000,
    label: 'Delhi Post-Monsoon Urban Collector (Poor)'
  },
  veryPoor: {
    iri: 10.4,
    potholes: 18,
    cracks: 48.0,
    rutting: 26.0,
    age: 12.5,
    drainage: 'Poor',
    traffic: 28000,
    label: 'Nagpur Heavy Freight Industrial Corridor (Very Poor)'
  }
};

function initPresets() {
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.getAttribute('data-preset');
      const p = PRESETS[presetKey];
      if (!p) return;

      setFormValues(p.iri, p.potholes, p.cracks, p.rutting, p.age, p.drainage, p.traffic);

      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Run analysis immediately
      runClassification();
    });
  });
}

function setFormValues(iri, potholes, cracks, rutting, age, drainage, traffic) {
  document.getElementById('slider-iri').value = iri;
  document.getElementById('num-iri').value = iri;

  document.getElementById('slider-potholes').value = potholes;
  document.getElementById('num-potholes').value = potholes;

  document.getElementById('slider-cracks').value = cracks;
  document.getElementById('num-cracks').value = cracks;

  document.getElementById('slider-rutting').value = rutting;
  document.getElementById('num-rutting').value = rutting;

  document.getElementById('slider-age').value = age;
  document.getElementById('num-age').value = age;

  document.getElementById('select-drainage').value = drainage;

  document.getElementById('slider-traffic').value = traffic;
  document.getElementById('num-traffic').value = traffic;
}

/* =========================================================
   4. CLASSIFICATION CONTROLLER (RANDOM FOREST RUNTIME)
   ========================================================= */
function initClassifier() {
  const form = document.getElementById('road-classifier-form');
  const resetBtn = document.getElementById('btn-reset-form');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      runClassification();
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      setFormValues(2.4, 1, 4.5, 3.2, 2.0, 'Good', 16500);
      clearPresetActiveState();
      
      const emptyState = document.getElementById('result-empty-state');
      const resultContent = document.getElementById('result-content');
      if (emptyState && resultContent) {
        emptyState.style.display = 'block';
        resultContent.classList.remove('active');
      }
    });
  }
}

function runClassification() {
  const iri = parseFloat(document.getElementById('num-iri').value);
  const potholes = parseInt(document.getElementById('num-potholes').value);
  const cracks = parseFloat(document.getElementById('num-cracks').value);
  const rutting = parseFloat(document.getElementById('num-rutting').value);
  const age = parseFloat(document.getElementById('num-age').value);
  const drainageStr = document.getElementById('select-drainage').value;
  const traffic = parseInt(document.getElementById('num-traffic').value);

  const drainageMap = { 'Good': 0, 'Moderate': 1, 'Poor': 2 };
  const drainageEncoded = drainageMap[drainageStr] !== undefined ? drainageMap[drainageStr] : 1;

  const features = [
    iri,
    potholes,
    cracks,
    rutting,
    age,
    drainageEncoded,
    traffic
  ];

  const submitBtn = document.getElementById('btn-classify');
  if (submitBtn) {
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing Indian Road Segment (100 Trees)...';
    submitBtn.disabled = true;

    setTimeout(() => {
      // Evaluate live using genuine Random Forest runtime
      const prediction = predictRoadCondition(features);
      renderClassificationResult(prediction, { iri, potholes, cracks, rutting, age, drainageStr, traffic });
      
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }, 250);
  } else {
    const prediction = predictRoadCondition(features);
    renderClassificationResult(prediction, { iri, potholes, cracks, rutting, age, drainageStr, traffic });
  }
}

function renderClassificationResult(res, inputs) {
  const emptyState = document.getElementById('result-empty-state');
  const resultContent = document.getElementById('result-content');

  if (emptyState) emptyState.style.display = 'none';
  if (resultContent) resultContent.classList.add('active');

  const conditionPill = document.getElementById('res-condition-pill');
  const confidenceVal = document.getElementById('res-confidence-val');
  const healthBarFill = document.getElementById('res-health-bar-fill');
  const healthPercent = document.getElementById('res-health-percent');
  const explanationText = document.getElementById('res-explanation-text');
  const maintTitle = document.getElementById('res-maint-title');
  const maintDesc = document.getElementById('res-maint-desc');

  const condition = res.predicted_condition;
  const condLower = condition.toLowerCase().replace(' ', '-');

  // Pill styling: Good=Green, Fair=Yellow, Poor=Orange, Very Poor=Red
  if (conditionPill) {
    conditionPill.className = `condition-pill ${condLower}`;
    const iconMap = {
      'Good': 'fa-check-circle',
      'Fair': 'fa-exclamation-circle',
      'Poor': 'fa-exclamation-triangle',
      'Very Poor': 'fa-times-circle'
    };
    conditionPill.innerHTML = `<i class="fas ${iconMap[condition] || 'fa-road'}"></i> ${condition}`;
  }

  // Model Confidence
  if (confidenceVal) {
    confidenceVal.innerText = `${res.confidence}%`;
  }

  // Calculate Civil Engineering Pavement Health Index (PCI equivalent 0-100)
  let healthScore = 100 - (
    (inputs.iri / 12) * 35 +
    (inputs.cracks / 60) * 30 +
    (inputs.rutting / 35) * 20 +
    (inputs.potholes / 25) * 15
  );
  healthScore = Math.max(5, Math.min(98, Math.round(healthScore)));

  if (healthBarFill && healthPercent) {
    healthBarFill.style.width = `${healthScore}%`;
    healthPercent.innerText = `${healthScore} / 100`;

    const colorMap = {
      'Good': '#10b981',      // Green
      'Fair': '#eab308',      // Yellow
      'Poor': '#f97316',      // Orange
      'Very Poor': '#ef4444'  // Red
    };
    healthBarFill.style.backgroundColor = colorMap[condition] || 'var(--road-yellow)';
  }

  // Probabilities Bars
  const probBarsContainer = document.getElementById('res-prob-bars');
  if (probBarsContainer && res.probabilities) {
    let html = '';
    const categories = ['Good', 'Fair', 'Poor', 'Very Poor'];
    const barColors = {
      'Good': '#10b981',      // Green
      'Fair': '#eab308',      // Yellow
      'Poor': '#f97316',      // Orange
      'Very Poor': '#ef4444'  // Red
    };

    categories.forEach(cat => {
      const prob = res.probabilities[cat] !== undefined ? res.probabilities[cat] : 0;
      html += `
        <div class="prob-row">
          <span class="prob-label">${cat}</span>
          <div class="prob-track">
            <div class="prob-fill" style="width: ${prob}%; background: ${barColors[cat]};"></div>
          </div>
          <span class="prob-val">${prob}%</span>
        </div>
      `;
    });
    probBarsContainer.innerHTML = html;
  }

  // Engineering Explanations & IRC:82 Maintenance Advice
  let explanation = '';
  let actionTitle = '';
  let actionDesc = '';

  if (condition === 'Good') {
    explanation = `Surface roughness (IRI: <strong>${inputs.iri} m/km</strong>) complies with IRC:SP:16 benchmarks for Indian National & State Highways. Potholes are minimal (<strong>${inputs.potholes}</strong>) and crack area covers only <strong>${inputs.cracks}%</strong> of the section. Pavement exhibits sound structural integrity and optimal skid resistance.`;
    actionTitle = 'Routine Maintenance & Periodic Inspection (IRC:82 Tier 1)';
    actionDesc = 'Apply routine crack sealing on hairline fissures, clean roadside storm drainage channels, and conduct semi-annual visual inspections to preserve the bitumen binder.';
  } else if (condition === 'Fair') {
    explanation = `Moderate surface aging detected. Roughness (IRI: <strong>${inputs.iri} m/km</strong>) and fatigue cracking (<strong>${inputs.cracks}%</strong>) indicate initial bitumen binder oxidation after ${inputs.age} years of traffic (${inputs.traffic.toLocaleString()} vpd). Timely surface renewal is critical before monsoon rainwater infiltrates the sub-base.`;
    actionTitle = 'Preventive Surface Treatment (IRC:82 Tier 2)';
    actionDesc = 'Apply preventive micro-surfacing or slurry seal (20mm premix carpet) and patch localized potholes immediately with polymer-modified bitumen to prevent base saturation.';
  } else if (condition === 'Poor') {
    explanation = `Significant pavement distress observed. Structural cracking (<strong>${inputs.cracks}%</strong>) combined with <strong>${inputs.potholes} potholes</strong> and rutting depth of <strong>${inputs.rutting} mm</strong> indicate sub-base shear strain under commercial heavy vehicle axle loading. Drainage is rated as ${inputs.drainageStr}.`;
    actionTitle = 'Milling & Structural Resurfacing (IRC:82 Tier 3)';
    actionDesc = 'Perform cold milling to level longitudinal wheelpath ruts, followed by a 40mm Bituminous Concrete (BC) overlay over a Dense Bituminous Macadam (DBM) base renewal per IRC:37 standards.';
  } else {
    explanation = `Critical pavement structural failure and major traffic safety hazard. Severe roughness (IRI: <strong>${inputs.iri} m/km</strong>), extensive alligator cracking (<strong>${inputs.cracks}%</strong>), and <strong>${inputs.potholes} hazardous potholes</strong> indicate subgrade moisture saturation and base collapse. Rutting (${inputs.rutting} mm) causes high vehicle hydroplaning and rollover risk.`;
    actionTitle = 'Full-Depth Reconstruction / FDR (IRC:82 Tier 4)';
    actionDesc = 'Execute immediate emergency safety warning signs, conduct Benkelman Beam Deflection (BBD) or Falling Weight Deflectometer (FWD) survey, and execute Full-Depth Reclamation (FDR) with subgrade geotextile stabilization.';
  }

  if (explanationText) explanationText.innerHTML = explanation;
  if (maintTitle) maintTitle.innerHTML = `<i class="fas fa-tools"></i> ${actionTitle}`;
  if (maintDesc) maintDesc.innerText = actionDesc;
}

/* =========================================================
   5. INDIAN ROAD DATASET EXPLORER (SEARCH, FILTER, PAGINATION, CSV)
   ========================================================= */
let currentDatasetPage = 1;
const recordsPerPage = 10;
let filteredRecords = [];

function initDatasetExplorer() {
  if (typeof ROADVISION_DATA === 'undefined') return;

  filteredRecords = [...ROADVISION_DATA.all_records];
  renderDatasetTable();

  const searchInput = document.getElementById('dataset-search');
  const cityFilter = document.getElementById('dataset-filter-city');
  const condFilter = document.getElementById('dataset-filter-condition');
  const drainageFilter = document.getElementById('dataset-filter-drainage');
  const prevBtn = document.getElementById('btn-page-prev');
  const nextBtn = document.getElementById('btn-page-next');
  const downloadBtn = document.getElementById('btn-download-csv');

  function applyFilters() {
    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const selectedCity = cityFilter ? cityFilter.value : 'all';
    const cond = condFilter ? condFilter.value : 'all';
    const drainage = drainageFilter ? drainageFilter.value : 'all';

    filteredRecords = ROADVISION_DATA.all_records.filter(row => {
      const matchesQuery = !query || 
        row.record_id.toLowerCase().includes(query) || 
        row.city.toLowerCase().includes(query) ||
        row.road_segment.toLowerCase().includes(query) ||
        row.road_type.toLowerCase().includes(query);

      const matchesCity = selectedCity === 'all' || row.city.toLowerCase().includes(selectedCity.toLowerCase());
      const matchesCond = cond === 'all' || row.condition_category === cond;
      const matchesDrainage = drainage === 'all' || row.drainage_condition === drainage;

      return matchesQuery && matchesCity && matchesCond && matchesDrainage;
    });

    currentDatasetPage = 1;
    renderDatasetTable();
  }

  if (searchInput) searchInput.addEventListener('input', applyFilters);
  if (cityFilter) cityFilter.addEventListener('change', applyFilters);
  if (condFilter) condFilter.addEventListener('change', applyFilters);
  if (drainageFilter) drainageFilter.addEventListener('change', applyFilters);

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentDatasetPage > 1) {
        currentDatasetPage--;
        renderDatasetTable();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      const maxPages = Math.ceil(filteredRecords.length / recordsPerPage) || 1;
      if (currentDatasetPage < maxPages) {
        currentDatasetPage++;
        renderDatasetTable();
      }
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', exportDatasetCSV);
  }
}

function renderDatasetTable() {
  const tbody = document.getElementById('dataset-tbody');
  const countSpan = document.getElementById('dataset-total-count');
  const pageSpan = document.getElementById('dataset-page-info');
  const prevBtn = document.getElementById('btn-page-prev');
  const nextBtn = document.getElementById('btn-page-next');

  if (!tbody) return;

  const total = filteredRecords.length;
  const maxPages = Math.ceil(total / recordsPerPage) || 1;
  const startIdx = (currentDatasetPage - 1) * recordsPerPage;
  const pageRows = filteredRecords.slice(startIdx, startIdx + recordsPerPage);

  if (countSpan) countSpan.innerText = `${total} records`;
  if (pageSpan) pageSpan.innerText = `Page ${currentDatasetPage} of ${maxPages}`;
  if (prevBtn) prevBtn.disabled = currentDatasetPage <= 1;
  if (nextBtn) nextBtn.disabled = currentDatasetPage >= maxPages;

  if (pageRows.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="10" style="text-align: center; padding: 24px; color: var(--text-muted);">
          No Indian road segments match the selected criteria.
        </td>
      </tr>
    `;
    return;
  }

  let html = '';
  pageRows.forEach(row => {
    const condClass = row.condition_category.toLowerCase().replace(' ', '-');
    html += `
      <tr>
        <td><strong>${row.record_id}</strong></td>
        <td>
          <div style="font-weight: 700; color: var(--text-primary); font-size: 0.88rem;">${row.city}</div>
          <div style="font-size: 0.76rem; color: var(--text-secondary);">${row.road_segment}</div>
          <div style="font-size: 0.70rem; color: var(--text-muted);">${row.road_type}</div>
        </td>
        <td>${row.iri_m_per_km}</td>
        <td>${row.pothole_count}</td>
        <td>${row.crack_percentage}%</td>
        <td>${row.rutting_depth_mm}</td>
        <td>${row.pavement_age_years}</td>
        <td>${row.traffic_volume_vpd.toLocaleString()}</td>
        <td>${row.drainage_condition}</td>
        <td><span class="table-tag ${condClass}">${row.condition_category}</span></td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

function exportDatasetCSV() {
  if (typeof ROADVISION_DATA === 'undefined') return;

  const records = ROADVISION_DATA.all_records;
  const headers = [
    'record_id',
    'city',
    'road_segment',
    'road_type',
    'iri_m_per_km',
    'pothole_count',
    'crack_percentage',
    'rutting_depth_mm',
    'pavement_age_years',
    'traffic_volume_vpd',
    'drainage_condition',
    'condition_category'
  ];

  let csvContent = headers.join(',') + '\n';

  records.forEach(r => {
    const row = [
      r.record_id,
      `"${r.city.replace(/"/g, '""')}"`,
      `"${r.road_segment.replace(/"/g, '""')}"`,
      `"${r.road_type}"`,
      r.iri_m_per_km,
      r.pothole_count,
      r.crack_percentage,
      r.rutting_depth_mm,
      r.pavement_age_years,
      r.traffic_volume_vpd,
      r.drainage_condition,
      r.condition_category
    ];
    csvContent += row.join(',') + '\n';
  });

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', 'indian_road_condition_dataset.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/* =========================================================
   6. INTERACTIVE CHARTS (CHART.JS)
   ========================================================= */
function initCharts() {
  if (typeof Chart === 'undefined' || typeof ROADVISION_DATA === 'undefined') return;

  Chart.defaults.color = '#94a3b8';
  Chart.defaults.font.family = "'Inter', sans-serif";

  // Chart 1: Feature Importance (Horizontal Bar)
  const featCtx = document.getElementById('chart-feature-importance');
  if (featCtx) {
    const importances = ROADVISION_DATA.feature_importances;
    const sortedFeats = Object.entries(importances).sort((a, b) => b[1] - a[1]);
    
    const labelNames = {
      'iri_m_per_km': 'Roughness Index (IRI)',
      'crack_percentage': 'Crack Percentage (%)',
      'rutting_depth_mm': 'Rutting Depth (mm)',
      'pavement_age_years': 'Pavement Surface Age (yrs)',
      'pothole_count': 'Pothole Count',
      'drainage_encoded': 'Drainage Rating',
      'traffic_volume_vpd': 'Traffic Volume (AADT)'
    };

    new Chart(featCtx, {
      type: 'bar',
      data: {
        labels: sortedFeats.map(f => labelNames[f[0]] || f[0]),
        datasets: [{
          label: 'Gini Feature Importance (%)',
          data: sortedFeats.map(f => (f[1] * 100).toFixed(2)),
          backgroundColor: [
            '#fbbf24', '#f59e0b', '#d97706', '#b45309', '#78350f', '#451a03', '#1e293b'
          ],
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `Importance: ${ctx.raw}%`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Contribution Weight (%)' }
          },
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }

  // Chart 2: Road Condition Distribution (Donut)
  const distCtx = document.getElementById('chart-condition-dist');
  if (distCtx) {
    new Chart(distCtx, {
      type: 'doughnut',
      data: {
        labels: ['Good (30)', 'Fair (30)', 'Poor (30)', 'Very Poor (30)'],
        datasets: [{
          data: [30, 30, 30, 30],
          backgroundColor: ['#10b981', '#eab308', '#f97316', '#ef4444'],
          borderColor: '#0d1527',
          borderWidth: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' }
        },
        cutout: '65%'
      }
    });
  }

  // Chart 3: Defect Severity Comparison across Categories
  const defectCtx = document.getElementById('chart-defect-comparison');
  if (defectCtx) {
    new Chart(defectCtx, {
      type: 'bar',
      data: {
        labels: ['Good', 'Fair', 'Poor', 'Very Poor'],
        datasets: [
          {
            label: 'Avg IRI (m/km)',
            data: [2.1, 4.1, 6.8, 9.8],
            backgroundColor: '#38bdf8',
            borderRadius: 4
          },
          {
            label: 'Avg Potholes (#)',
            data: [0.5, 3.2, 8.4, 18.2],
            backgroundColor: '#eab308',
            borderRadius: 4
          },
          {
            label: 'Avg Cracks (%)',
            data: [3.5, 12.8, 26.5, 46.5],
            backgroundColor: '#f97316',
            borderRadius: 4
          },
          {
            label: 'Avg Rutting (mm)',
            data: [3.2, 8.5, 16.2, 26.5],
            backgroundColor: '#ef4444',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: { mode: 'index', intersect: false }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
        }
      }
    });
  }
}

/* =========================================================
   7. CONFUSION MATRIX HEATMAP RENDERER (CO4)
   ========================================================= */
function initConfusionMatrix() {
  if (typeof ROADVISION_DATA === 'undefined') return;

  const cmGrid = document.getElementById('confusion-matrix-grid');
  if (!cmGrid) return;

  const cm = ROADVISION_DATA.summary.metrics.confusion_matrix;
  const categories = ROADVISION_DATA.summary.categories;

  let html = `
    <div class="cm-cell cm-header" style="font-size:0.7rem; color:var(--text-muted);">Actual \\ Pred</div>
    <div class="cm-cell cm-header">Good</div>
    <div class="cm-cell cm-header">Fair</div>
    <div class="cm-cell cm-header">Poor</div>
    <div class="cm-cell cm-header">Very Poor</div>
  `;

  categories.forEach((actualCat, r) => {
    html += `<div class="cm-cell cm-header" style="text-align:right; padding-right:8px;">${actualCat}</div>`;
    categories.forEach((predCat, c) => {
      const val = cm[r][c];
      const isDiag = (r === c);
      let cellClass = 'cm-zero';
      if (isDiag && val > 0) cellClass = 'cm-diag';
      else if (!isDiag && val > 0) cellClass = 'cm-offdiag';

      html += `
        <div class="cm-cell ${cellClass}" title="Actual: ${actualCat}, Predicted: ${predCat}">
          <span style="font-size: 1.15rem;">${val}</span>
          <span style="font-size: 0.65rem; opacity: 0.8;">${isDiag ? 'Correct' : val > 0 ? 'Boundary Shift' : 'None'}</span>
        </div>
      `;
    });
  });

  cmGrid.innerHTML = html;
}

/* =========================================================
   8. TEST SET COMPARISON TABLE (24 TEST SAMPLES)
   ========================================================= */
function initTestComparisonTable() {
  if (typeof ROADVISION_DATA === 'undefined') return;

  const tbody = document.getElementById('test-eval-tbody');
  const filterSelect = document.getElementById('test-eval-filter');
  if (!tbody) return;

  const samples = ROADVISION_DATA.test_evaluation_samples;

  function render(filter) {
    let rows = samples;
    if (filter === 'errors') {
      rows = samples.filter(s => !s.is_correct);
    } else if (filter === 'correct') {
      rows = samples.filter(s => s.is_correct);
    }

    if (rows.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:18px; color:var(--text-muted);">No records match filter.</td></tr>`;
      return;
    }

    let html = '';
    rows.forEach(s => {
      const actClass = s.actual_condition.toLowerCase().replace(' ', '-');
      const predClass = s.predicted_condition.toLowerCase().replace(' ', '-');
      const statusIcon = s.is_correct 
        ? '<i class="fas fa-check-circle" style="color:var(--indicator-good);"></i> Match' 
        : '<i class="fas fa-exclamation-triangle" style="color:var(--indicator-fair);"></i> Boundary';

      html += `
        <tr>
          <td><strong>${s.record_id}</strong></td>
          <td>
            <div style="font-weight: 700; color: var(--text-primary); font-size: 0.84rem;">${s.city}</div>
            <div style="font-size: 0.74rem; color: var(--text-secondary);">${s.road_segment}</div>
            <div style="font-size: 0.70rem; color: var(--text-muted);">IRI: ${s.iri_m_per_km} m/km | Cracks: ${s.crack_percentage}% | Potholes: ${s.pothole_count}</div>
          </td>
          <td><span class="table-tag ${actClass}">${s.actual_condition}</span></td>
          <td><span class="table-tag ${predClass}">${s.predicted_condition}</span></td>
          <td>${s.confidence}%</td>
          <td>${statusIcon}</td>
        </tr>
      `;
    });
    tbody.innerHTML = html;
  }

  render('all');

  if (filterSelect) {
    filterSelect.addEventListener('change', (e) => {
      render(e.target.value);
    });
  }
}

/* =========================================================
   9. MODALS (5-MIN VIVA GUIDE & PROJECT REPORT)
   ========================================================= */
function initModals() {
  const openVivaBtn = document.getElementById('btn-open-viva-modal');
  const vivaModal = document.getElementById('vivaModal');
  const closeVivaBtn = document.getElementById('btn-close-viva');

  if (openVivaBtn && vivaModal) {
    openVivaBtn.addEventListener('click', () => vivaModal.classList.add('active'));
  }
  if (closeVivaBtn && vivaModal) {
    closeVivaBtn.addEventListener('click', () => vivaModal.classList.remove('active'));
  }

  const openReportBtn = document.getElementById('btn-open-report-modal');
  const reportModal = document.getElementById('reportModal');
  const closeReportBtn = document.getElementById('btn-close-report');
  const printReportBtn = document.getElementById('btn-print-report');

  if (openReportBtn && reportModal) {
    openReportBtn.addEventListener('click', () => reportModal.classList.add('active'));
  }
  if (closeReportBtn && reportModal) {
    closeReportBtn.addEventListener('click', () => reportModal.classList.remove('active'));
  }
  if (printReportBtn) {
    printReportBtn.addEventListener('click', () => window.print());
  }

  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });

  const downloadNbBtn = document.getElementById('btn-download-notebook');
  if (downloadNbBtn) {
    downloadNbBtn.addEventListener('click', () => {
      const link = document.createElement('a');
      link.href = 'RoadVision_AI_Colab_Notebook.ipynb';
      link.download = 'RoadVision_AI_Indian_Roads_Notebook.ipynb';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }
}

/* =========================================================
   10. STUDENT TEAM LOCAL PERSISTENCE (EDITABLE CREDITS)
   ========================================================= */
function initTeamPersistence() {
  const members = [
    { nameId: 'member-1-name', rollId: 'member-1-roll', defaultName: 'Rohan Sharma', defaultRoll: 'CE-2024-042' },
    { nameId: 'member-2-name', rollId: 'member-2-roll', defaultName: 'Ananya Patel', defaultRoll: 'CE-2024-058' },
    { nameId: 'member-3-name', rollId: 'member-3-roll', defaultName: 'Aditya Deshmukh', defaultRoll: 'CE-2024-071' }
  ];

  members.forEach(m => {
    const nameEl = document.getElementById(m.nameId);
    const rollEl = document.getElementById(m.rollId);

    if (nameEl && rollEl) {
      const savedName = localStorage.getItem(`rv_${m.nameId}`);
      const savedRoll = localStorage.getItem(`rv_${m.rollId}`);

      if (savedName) nameEl.innerText = savedName;
      if (savedRoll) rollEl.innerText = savedRoll;

      nameEl.addEventListener('click', () => {
        const current = nameEl.innerText;
        const updated = prompt('Edit Student Name:', current);
        if (updated && updated.trim()) {
          nameEl.innerText = updated.trim();
          localStorage.setItem(`rv_${m.nameId}`, updated.trim());
        }
      });

      rollEl.addEventListener('click', () => {
        const current = rollEl.innerText;
        const updated = prompt('Edit Roll Number:', current);
        if (updated && updated.trim()) {
          rollEl.innerText = updated.trim();
          localStorage.setItem(`rv_${m.rollId}`, updated.trim());
        }
      });
    }
  });
}
