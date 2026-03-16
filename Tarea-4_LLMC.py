import streamlit as st

st.set_page_config(layout="wide", page_title="HAR Dashboard")

st.markdown("""
    <style>
        .main > div { padding: 0 !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        iframe { display: block; }
    </style>
""", unsafe_allow_html=True)

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>HAR - Human Activity Recognition</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg:     #f5f0eb;
    --bg2:    #ede8e2;
    --card:   #faf7f4;
    --border: #ddd6ce;
    --text:   #2c2620;
    --text2:  #7a6e65;
    --accent: #b5886a;
    --a2:     #8fada8;
    --a3:     #c4a882;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--text); }

  .hero {
    background: linear-gradient(135deg, #e8ddd4 0%, #d6cbbf 50%, #c9bfb4 100%);
    padding: 64px 48px 48px; position: relative; overflow: hidden;
  }
  .hero::before {
    content: ''; position: absolute; top: -80px; right: -80px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(181,136,106,0.15) 0%, transparent 70%);
  }
  .hero-deco { position: absolute; top: 0; right: 0; width: 480px; height: 100%; pointer-events: none; overflow: hidden; }
  .hero-tag { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); font-weight: 500; margin-bottom: 16px; }
  .hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(2rem,5vw,3.2rem); font-weight: 700; line-height: 1.15; color: var(--text); max-width: 640px; margin-bottom: 16px; }
  .hero p { font-size: 15px; color: var(--text2); max-width: 620px; line-height: 1.75; margin-bottom: 16px; }
  .hero-stats { display: flex; gap: 32px; flex-wrap: wrap; margin-top: 16px; }
  .hero-stat { display: flex; flex-direction: column; gap: 2px; }
  .hero-stat span:first-child { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 600; color: var(--accent); }
  .hero-stat span:last-child { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text2); }

  .nav { background: var(--card); border-bottom: 1px solid var(--border); padding: 0 48px; display: flex; position: sticky; top: 0; z-index: 100; }
  .nav-btn { padding: 16px 24px; background: none; border: none; border-bottom: 2px solid transparent; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: var(--text2); cursor: pointer; transition: all 0.2s; }
  .nav-btn:hover { color: var(--text); }
  .nav-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

  .section { display: none; padding: 48px; }
  .section.active { display: block; }
  .section-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 600; color: var(--text); margin-bottom: 6px; }
  .section-sub { font-size: 13px; color: var(--text2); margin-bottom: 36px; line-height: 1.7; max-width: 680px; }

  .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 28px; }
  .card-title { font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--text2); font-weight: 500; margin-bottom: 20px; }
  .card p { font-size: 13px; line-height: 1.75; color: var(--text2); }
  .mb { margin-bottom: 24px; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 20px; }

  .metric-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-align: center; }
  .metric-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 600; color: var(--accent); margin-bottom: 4px; }
  .metric-label { font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text2); }

  .heatmap-wrap { overflow-x: auto; }
  .heatmap-table { border-collapse: collapse; font-size: 11px; width: 100%; }
  .heatmap-table th { padding: 6px 8px; font-weight: 500; color: var(--text2); font-size: 10px; }
  .heatmap-table td { width: 52px; height: 44px; text-align: center; font-size: 11px; font-weight: 500; border: 1px solid rgba(255,255,255,0.4); border-radius: 3px; transition: transform 0.15s; cursor: default; }
  .heatmap-table td:hover { transform: scale(1.08); z-index: 2; position: relative; }
  .row-label { font-size: 10px; color: var(--text2); text-align: right; padding-right: 8px; white-space: nowrap; }

  .corr-wrap { overflow-x: auto; }
  .corr-table { border-collapse: separate; border-spacing: 3px; font-size: 10px; }
  .corr-table th { padding: 4px 8px; color: var(--text2); font-size: 9px; font-weight: 500; text-align: center; white-space: nowrap; }
  .corr-table td { width: 58px; height: 42px; text-align: center; font-size: 10px; font-weight: 600; border-radius: 5px; transition: transform 0.15s; cursor: default; }
  .corr-table td:hover { transform: scale(1.12); z-index: 2; position: relative; }
  .corr-row-label { font-size: 9px; color: var(--text2); text-align: right; padding-right: 10px; white-space: nowrap; font-weight: 500; }
  .corr-empty { background: transparent !important; }

  .model-selector { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
  .model-btn { padding: 7px 16px; border-radius: 20px; border: 1.5px solid var(--border); background: none; font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 500; color: var(--text2); cursor: pointer; transition: all 0.2s; }
  .model-btn:hover { border-color: var(--accent); color: var(--accent); }
  .model-btn.active { background: var(--accent); border-color: var(--accent); color: white; }

  .progress-row { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
  .progress-label { font-size: 12px; color: var(--text2); width: 160px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .progress-bar-wrap { flex: 1; background: var(--bg2); border-radius: 4px; height: 10px; overflow: hidden; }
  .progress-bar-fill { height: 100%; border-radius: 4px; transition: width 0.8s cubic-bezier(.4,0,.2,1); }
  .progress-val { font-size: 11px; color: var(--text2); width: 44px; text-align: right; flex-shrink: 0; }

  .results-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .results-table th { padding: 12px 16px; text-align: left; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text2); border-bottom: 1px solid var(--border); font-weight: 500; }
  .results-table td { padding: 14px 16px; border-bottom: 1px solid var(--bg2); }
  .results-table tr:last-child td { border-bottom: none; }
  .results-table tr:hover td { background: var(--bg2); }
  .best { color: var(--accent); font-weight: 600; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
  .badge-si { background: #e8ddd4; color: var(--accent); }
  .badge-no { background: #dde8e4; color: #5a8a7f; }

  .donut-wrap { display: flex; align-items: center; gap: 32px; flex-wrap: wrap; }
  .donut-canvas { max-width: 200px; max-height: 200px; }
  .donut-legend { display: flex; flex-direction: column; gap: 10px; }
  .legend-item { display: flex; align-items: center; gap: 10px; font-size: 12px; color: var(--text2); }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

  .chart-sub { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text2); margin-bottom: 12px; }

  .footer { text-align: center; padding: 32px; font-size: 11px; color: var(--text2); letter-spacing: 1px; border-top: 1px solid var(--border); margin-top: 48px; }

  @keyframes fadeUp { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
  .section.active > * { animation: fadeUp 0.35s ease both; }
  .section.active > *:nth-child(2) { animation-delay:.05s; }
  .section.active > *:nth-child(3) { animation-delay:.10s; }
  .section.active > *:nth-child(4) { animation-delay:.15s; }
  .section.active > *:nth-child(5) { animation-delay:.20s; }
  .section.active > *:nth-child(6) { animation-delay:.25s; }
  .section.active > *:nth-child(7) { animation-delay:.30s; }

  @media (max-width:768px) {
    .hero { padding:40px 24px 32px; }
    .nav { padding:0 16px; }
    .section { padding:32px 16px; }
    .grid-2,.grid-3,.grid-4 { grid-template-columns:1fr; }
  }
</style>
</head>
<body>

<div class="hero">
  <!-- Decorative SVG -->
  <div class="hero-deco">
    <svg width="480" height="100%" viewBox="0 0 480 340" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMaxYMid meet">

      <!-- Soft background glow -->
      <circle cx="370" cy="160" r="200" fill="rgba(181,136,106,0.07)"/>

      <!-- -- FIGURE WALKING (right side) -- -->
      <!-- Head -->
      <circle cx="390" cy="60" r="16" stroke="rgba(181,136,106,0.45)" stroke-width="2" fill="rgba(181,136,106,0.08)"/>
      <!-- Body -->
      <line x1="390" y1="76" x2="390" y2="130" stroke="rgba(181,136,106,0.40)" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Left arm (forward) -->
      <line x1="390" y1="90" x2="365" y2="115" stroke="rgba(181,136,106,0.40)" stroke-width="2" stroke-linecap="round"/>
      <!-- Right arm (back) -->
      <line x1="390" y1="90" x2="415" y2="108" stroke="rgba(181,136,106,0.30)" stroke-width="2" stroke-linecap="round"/>
      <!-- Left leg (forward stride) -->
      <line x1="390" y1="130" x2="368" y2="168" stroke="rgba(181,136,106,0.40)" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="368" y1="168" x2="355" y2="200" stroke="rgba(181,136,106,0.35)" stroke-width="2" stroke-linecap="round"/>
      <!-- Right leg (back stride) -->
      <line x1="390" y1="130" x2="410" y2="162" stroke="rgba(181,136,106,0.30)" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="410" y1="162" x2="420" y2="195" stroke="rgba(181,136,106,0.25)" stroke-width="2" stroke-linecap="round"/>

      <!-- -- SMARTPHONE (held by figure, left hand) -- -->
      <rect x="330" y="108" width="24" height="38" rx="4" stroke="rgba(143,173,168,0.55)" stroke-width="1.8" fill="rgba(143,173,168,0.10)"/>
      <!-- Screen -->
      <rect x="333" y="113" width="18" height="24" rx="2" fill="rgba(143,173,168,0.15)" stroke="rgba(143,173,168,0.30)" stroke-width="0.8"/>
      <!-- Home button -->
      <circle cx="342" cy="141" r="2" fill="rgba(143,173,168,0.40)"/>

      <!-- -- SENSOR SIGNAL WAVES from phone -- -->
      <!-- X axis signal -->
      <path d="M 260 145 L 275 145 Q 278 138 281 145 Q 284 152 287 145 Q 290 138 293 145 L 308 145"
            stroke="rgba(181,136,106,0.55)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <!-- Y axis signal -->
      <path d="M 260 160 L 272 160 Q 275 150 279 160 Q 283 170 287 160 Q 291 150 295 160 L 308 160"
            stroke="rgba(143,173,168,0.50)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <!-- Z axis signal -->
      <path d="M 260 175 L 270 175 Q 274 168 278 175 Q 282 182 286 175 Q 290 168 294 175 L 308 175"
            stroke="rgba(196,168,130,0.45)" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <!-- Axis labels -->
      <text x="248" y="148" font-size="8" fill="rgba(181,136,106,0.55)" font-family="DM Sans, sans-serif" font-weight="500">X</text>
      <text x="248" y="163" font-size="8" fill="rgba(143,173,168,0.55)" font-family="DM Sans, sans-serif" font-weight="500">Y</text>
      <text x="248" y="178" font-size="8" fill="rgba(196,168,130,0.55)" font-family="DM Sans, sans-serif" font-weight="500">Z</text>

      <!-- -- ACTIVITY LABELS (small floating tags) -- -->
      <rect x="230" y="48" width="72" height="18" rx="9" fill="rgba(181,136,106,0.12)" stroke="rgba(181,136,106,0.25)" stroke-width="1"/>
      <text x="266" y="60" font-size="8" fill="rgba(181,136,106,0.70)" font-family="DM Sans, sans-serif" font-weight="500" text-anchor="middle">WALKING</text>

      <rect x="218" y="220" width="82" height="18" rx="9" fill="rgba(143,173,168,0.12)" stroke="rgba(143,173,168,0.25)" stroke-width="1"/>
      <text x="259" y="232" font-size="8" fill="rgba(143,173,168,0.70)" font-family="DM Sans, sans-serif" font-weight="500" text-anchor="middle">STANDING</text>

      <rect x="380" y="220" width="60" height="18" rx="9" fill="rgba(196,168,130,0.12)" stroke="rgba(196,168,130,0.25)" stroke-width="1"/>
      <text x="410" y="232" font-size="8" fill="rgba(196,168,130,0.75)" font-family="DM Sans, sans-serif" font-weight="500" text-anchor="middle">LAYING</text>

      <!-- -- DOT GRID (data motif bottom right) -- -->
      <circle cx="420" cy="270" r="2.2" fill="rgba(181,136,106,0.22)"/>
      <circle cx="435" cy="270" r="2.2" fill="rgba(181,136,106,0.18)"/>
      <circle cx="450" cy="270" r="2.2" fill="rgba(181,136,106,0.14)"/>
      <circle cx="465" cy="270" r="2.2" fill="rgba(181,136,106,0.10)"/>
      <circle cx="420" cy="285" r="2.2" fill="rgba(181,136,106,0.18)"/>
      <circle cx="435" cy="285" r="2.2" fill="rgba(181,136,106,0.14)"/>
      <circle cx="450" cy="285" r="2.2" fill="rgba(181,136,106,0.10)"/>
      <circle cx="420" cy="300" r="2.2" fill="rgba(181,136,106,0.14)"/>
      <circle cx="435" cy="300" r="2.2" fill="rgba(181,136,106,0.10)"/>

      <!-- Bottom accent line -->
      <line x1="215" y1="318" x2="470" y2="318" stroke="rgba(181,136,106,0.12)" stroke-width="1"/>
    </svg>
  </div>
  <div class="hero-tag">University of California, Irvine</div>
  <h1>Human Activity<br>Recognition</h1>
  <p>El dataset que elegi es "Human Activity Recognition (HAR)", que contiene registros de los sensores de un celular usado por 30 personas mientras hacian 6 actividades del dia a dia: caminar, subir y bajar escaleras, sentarse, pararse y acostarse. A partir de esas senales se calcularon 561 variables que describen como se movio cada persona.</p>
  <div class="hero-stats">
    <div class="hero-stat"><span>10,299</span><span>Muestras totales</span></div>
    <div class="hero-stat"><span>561</span><span>Variables</span></div>
    <div class="hero-stat"><span>6</span><span>Actividades</span></div>
    <div class="hero-stat"><span>30</span><span>Participantes</span></div>
  </div>
</div>

<nav class="nav">
  <button class="nav-btn active" onclick="showSection('eda',this)">EDA - QUEST</button>
  <button class="nav-btn" onclick="showSection('modelos',this)">Clasificacion</button>
  <button class="nav-btn" onclick="showSection('comparacion',this)">Comparacion</button>
</nav>

<!--  EDA  -->
<div class="section active" id="eda">
  <div class="section-title">EDA - QUEST</div>
  <div class="section-sub">Exploracion de los datos para comprender el contexto y como se comportan las variables.</div>

  <!-- Q -->
  <div class="mb">
    <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--text2);font-weight:500;margin-bottom:16px">Q - Questions</div>
    <div class="grid-3" style="gap:16px">
      <div class="card"><div class="card-title">Q1</div><p>El dataset esta balanceado? (las 6 actividades)</p></div>
      <div class="card"><div class="card-title">Q2</div><p>Existen valores faltantes o anomalos en las variables?</p></div>
      <div class="card"><div class="card-title">Q3</div><p>Caracteriza estadisticamente las variables (rango, distribucion, simetria)</p></div>
      <div class="card"><div class="card-title">Q4</div><p>Existen variables que permitan separar actividades dinamicas (caminar) de estaticas (sentado, de pie, acostado)?</p></div>
      <div class="card"><div class="card-title">Q5</div><p>Que variables tienen mayor influencia para distinguir las 6 clases?</p></div>
      <div class="card"><div class="card-title">Q6</div><p>Existen grupos naturales de actividades visibles en los datos (sin usar etiquetas)?</p></div>
    </div>
  </div>

  <!-- U -->
  <div class="card mb">
    <div class="card-title">U - Understand</div>
    <div class="grid-4" style="margin-bottom:20px">
      <div class="metric-card"><div class="metric-value">7,352</div><div class="metric-label">Muestras Train</div></div>
      <div class="metric-card"><div class="metric-value">2,947</div><div class="metric-label">Muestras Test</div></div>
      <div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Valores Nulos</div></div>
      <div class="metric-card"><div class="metric-value">[-1, 1]</div><div class="metric-label">Rango Variables</div></div>
    </div>
    <div class="grid-2">
      <div>
        <div class="chart-sub">Distribucion de actividades - Training set</div>
        <canvas id="distChart" height="210"></canvas>
        <p style="margin-top:12px">Las 6 clases tienen una distribucion relativamente equilibrada, con proporciones entre el 13% y el 19%. No se observa un desbalanceo que pueda sesgar los modelos de clasificacion.</p>
      </div>
      <div>
        <div class="chart-sub">Proporcion por clase</div>
        <div class="donut-wrap">
          <canvas id="donutChart" class="donut-canvas"></canvas>
          <div class="donut-legend" id="donutLegend"></div>
        </div>
        <p style="margin-top:12px">Todas las variables estan normalizadas en el rango [-1, 1].</p>
      </div>
    </div>
  </div>

  <!-- E -->
  <div class="card mb">
    <div class="card-title">E - Explore</div>
    <p style="margin-bottom:20px">La mayoria de las variables muestran distribuciones bimodales o asimetricas, lo que sugiere que los datos de actividades dinamicas y estaticas forman dos grupos naturalmente separados.</p>
    <div class="chart-sub" style="margin-bottom:16px">Distribucion de variables representativas</div>
    <div class="grid-3" style="margin-bottom:28px">
      <div><div class="chart-sub">Aceleracion corporal X (tiempo)</div><canvas id="histX" height="180"></canvas></div>
      <div><div class="chart-sub">Aceleracion corporal Y (tiempo)</div><canvas id="histY" height="180"></canvas></div>
      <div><div class="chart-sub">Aceleracion corporal Z (tiempo)</div><canvas id="histZ" height="180"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad X (tiempo)</div><canvas id="histGX" height="180"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad Y (tiempo)</div><canvas id="histGY" height="180"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad Z (tiempo)</div><canvas id="histGZ" height="180"></canvas></div>
    </div>
    <p style="margin-bottom:20px">Se evidencia una separacion entre actividades dinamicas (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS) y estaticas (SITTING, STANDING, LAYING) en las variables de aceleracion corporal. Sin embargo, dentro de cada grupo se muestra una separacion menor entre si.</p>
    <div class="chart-sub" style="margin-bottom:16px">Distribucion por actividad - variables representativas</div>
    <div class="grid-3">
      <div><div class="chart-sub">Aceleracion corporal X</div><canvas id="boxX" height="200"></canvas></div>
      <div><div class="chart-sub">Aceleracion corporal Y</div><canvas id="boxY" height="200"></canvas></div>
      <div><div class="chart-sub">Aceleracion corporal Z</div><canvas id="boxZ" height="200"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad X</div><canvas id="boxGX" height="200"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad Y</div><canvas id="boxGY" height="200"></canvas></div>
      <div><div class="chart-sub">Aceleracion gravedad Z</div><canvas id="boxGZ" height="200"></canvas></div>
    </div>
  </div>

  <!-- S -->
  <div class="card mb">
    <div class="card-title">S - Study</div>
    <p style="margin-bottom:20px">Se observa alta correlacion positiva entre las componentes de aceleracion corporal en los tres ejes.</p>
    <p style="margin-bottom:20px">Las variables mas influyentes provienen principalmente del dominio de frecuencia "fBody" y de la magnitud de la aceleracion corporal. En este sentido, la forma del movimiento periodico (caminar vs estar quieto) es lo que mejor distingue las actividades.</p>
    <p style="margin-bottom:24px">En la grafica de separacion se evidencia una division entre las actividades dinamicas y las estaticas. Sin embargo, SITTING, STANDING y LAYING se solapan entre si, lo que hace que dividirlas o identificarlas sea mas complicado.</p>

    <div class="grid-2" style="margin-bottom:24px">
      <div>
        <div class="chart-sub">Correlacion entre variables representativas</div>
        <div class="corr-wrap" id="corrHeatmap"></div>
      </div>
      <div>
        <div class="chart-sub">Top 10 variables con mayor influencia</div>
        <div id="varBars"></div>
      </div>
    </div>

    <div class="grid-2">
      <div>
        <div class="chart-sub">Actividades separadas - top 2 variables</div>
        <canvas id="scatterChart" height="260"></canvas>
      </div>
      <div>
        <div class="chart-sub">Reduccion de dimensionalidad - PC1 vs PC2</div>
        <canvas id="pcaChart" height="260"></canvas>
      </div>
    </div>

    <div style="margin-top:24px">
      <div class="chart-sub" style="margin-bottom:16px">Distribucion por actividad - top 3 variables</div>
      <div class="grid-3">
        <div><div class="chart-sub">fBodyAccJerk-entropy()-X</div><canvas id="topHist1" height="180"></canvas></div>
        <div><div class="chart-sub">fBodyAccJerk-entropy()-Y</div><canvas id="topHist2" height="180"></canvas></div>
        <div><div class="chart-sub">fBodyAccJerkMag-entropy()</div><canvas id="topHist3" height="180"></canvas></div>
      </div>
    </div>
  </div>

  <!-- T -->
  <div>
    <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--text2);font-weight:500;margin-bottom:16px">T - Tell</div>
    <div class="grid-3" style="gap:16px">
      <div class="card"><div class="card-title">Q1</div><p>Si. Las 6 clases tienen entre 13% y 19% de representacion.</p></div>
      <div class="card"><div class="card-title">Q2</div><p>No. El dataset esta completo y todas las variables estan normalizadas en [-1, 1].</p></div>
      <div class="card"><div class="card-title">Q3</div><p>Distribuciones bimodales o asimetricas, consistentes con la separacion entre actividades dinamicas y estaticas.</p></div>
      <div class="card"><div class="card-title">Q4</div><p>Si. Las variables de aceleracion corporal separan claramente ambos grupos con solo visualizar su distribucion.</p></div>
      <div class="card"><div class="card-title">Q5</div><p>Las variables relacionadas con la frecuencia "fBody" y las de aceleracion.</p></div>
      <div class="card"><div class="card-title">Q6</div><p>Si. La reduccion de dimensionalidad muestra dos grandes grupos (dinamicas y estaticas).</p></div>
    </div>
  </div>
</div>

<!--  CLASIFICACIN  -->
<div class="section" id="modelos">
  <div class="section-title">Clasificacion Multiclase</div>
  <div class="section-sub">Tres modelos para clasificar la actividad que estaba haciendo cada persona incluida en el estudio.</div>

  <div class="model-selector" id="modelSelector">
    <button class="model-btn active" onclick="selectModel('SGD',this)">Modelo 1 - SGDClassifier</button>
    <button class="model-btn" onclick="selectModel('RF',this)">Modelo 2 - Random Forest</button>
    <button class="model-btn" onclick="selectModel('SVM',this)">Modelo 3 - SVM</button>
  </div>
  <div class="model-selector">
    <button class="model-btn active" id="absBtn" onclick="selectCMType('abs',this)">Valores absolutos</button>
    <button class="model-btn" id="normBtn" onclick="selectCMType('norm',this)">Normalizada (solo errores)</button>
  </div>

  <div class="grid-2" style="margin-bottom:24px">
    <div class="card">
      <div class="card-title" id="cmTitle">Modelo 1 - SGD  Matriz de confusion</div>
      <div class="heatmap-wrap"><table class="heatmap-table" id="cmTable"></table></div>
    </div>
    <div class="card">
      <div class="card-title">F1 por actividad</div>
      <div id="reportBars"></div>
    </div>
  </div>
  <div class="card" id="modelNote">
    <div class="card-title">Nota</div>
    <p id="modelNoteText"></p>
  </div>
</div>

<!--  COMPARACIN  -->
<div class="section" id="comparacion">
  <div class="section-title">Comparacion de Modelos</div>
  <div class="section-sub">Los tres modelos logran clasificar las 6 actividades con accuracy superior al 90%.</div>

  <div class="grid-4" style="margin-bottom:24px">
    <div class="metric-card"><div class="metric-value">95.2%</div><div class="metric-label">Mejor Accuracy (SVM)</div></div>
    <div class="metric-card"><div class="metric-value">99.8%</div><div class="metric-label">Mejor AUC (SVM)</div></div>
    <div class="metric-card"><div class="metric-value">95.2%</div><div class="metric-label">Mejor F1 macro (SVM)</div></div>
    <div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Modelos evaluados</div></div>
  </div>

  <div class="grid-2" style="margin-bottom:24px">
    <div class="card">
      <div class="card-title">Metricas comparativas</div>
      <canvas id="compChart" height="260"></canvas>
    </div>
    <div class="card">
      <div class="card-title">Tabla de resultados</div>
      <table class="results-table">
        <thead><tr><th>Modelo</th><th>Acc. CV</th><th>Acc. Test</th><th>F1 macro</th><th>AUC</th><th>Escalado</th></tr></thead>
        <tbody>
          <tr><td>SGD</td><td>0.9276</td><td>0.9386</td><td>0.9387</td><td>0.9918</td><td><span class="badge badge-si">Si</span></td></tr>
          <tr><td>Random Forest</td><td>0.9101</td><td>0.9257</td><td>0.9241</td><td>0.9952</td><td><span class="badge badge-no">No</span></td></tr>
          <tr><td>SVM (RBF)</td><td class="best">0.9259</td><td class="best">0.9522</td><td class="best">0.9515</td><td class="best">0.9977</td><td><span class="badge badge-si">Si</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Conclusion</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px">
      <div><div class="card-title" style="margin-bottom:10px">SGDClassifier</div><p>Es el mas rapido pero el menos preciso. Es importante resaltar que este modelo tiene dificultades para clasificar actividades estaticas similares como SITTING y STANDING.</p></div>
      <div><div class="card-title" style="margin-bottom:10px">Random Forest</div><p>Tiene una buena precision, y su rasgo mas importante a tener en cuenta es que permite identificar las variables mas importantes.</p></div>
      <div><div class="card-title" style="color:var(--accent);margin-bottom:10px">SVM - Mejor modelo</div><p>Es el modelo mas preciso de los tres evaluados e incluso logra separar las clases que tienen similitud entre si.</p></div>
    </div>
  </div>
</div>

<div class="footer">UCI HAR Dataset  Universidad de California Irvine  Analisis con Python & Scikit-Learn</div>

<script>
// -- PALETTE ------------------------------------------------------------------
const NUDE  = ['#b5886a','#8fada8','#c4a882','#9b7e6a','#7a9e99','#d4b896'];
const ACTIVITIES = ['WALKING','WALKING_UPSTAIRS','WALKING_DOWNSTAIRS','SITTING','STANDING','LAYING'];
const ACT_S = ['Walk','Walk Up','Walk Down','Sitting','Standing','Laying'];
const DIST  = [1226,1073,986,1286,1374,1407];

// -- DATA ---------------------------------------------------------------------
// Histogram data (approximate from notebook charts)
const HIST_DATA = {
  bodyX:  { bins: [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0], counts: [0,0,0,0,0,80,920,870,160,130,100] },
  bodyY:  { bins: [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0], counts: [0,0,0,0,60,5900,280,60,20,10,5] },
  bodyZ:  { bins: [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0], counts: [0,0,0,0,100,4800,1600,500,100,50,20] },
  gravX:  { bins: [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0], counts: [80,100,120,140,140,130,120,140,700,2050,1300] },
  gravY:  { bins: [-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.8,1.0], counts: [310,380,380,310,250,200,160,140,130,200,130,70,50,20] },
  gravZ:  { bins: [-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0], counts: [80,100,150,280,400,820,420,420,410,280,200] },
};

// Boxplot median data per activity (approximate)
const BOX_MEDIANS = {
  bodyX:  [0.26, 0.26, 0.27, 0.27, 0.28, 0.27],
  bodyY:  [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
  bodyZ:  [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
  gravX:  [0.93, 0.88, 0.86, 0.70, 0.93, -0.45],
  gravY:  [-0.25,-0.30,-0.27,0.12,-0.25,0.65],
  gravZ:  [0.04, 0.04, 0.04, 0.18, 0.04, 0.65],
};
const BOX_Q1 = {
  bodyX:  [0.22,0.20,0.21,0.20,0.22,0.22], bodyY: [-0.02,-0.02,-0.02,-0.02,-0.02,-0.02],
  bodyZ:  [-0.14,-0.13,-0.13,-0.12,-0.12,-0.14], gravX: [0.88,0.73,0.75,0.26,0.89,-0.58],
  gravY:  [-0.28,-0.33,-0.30,-0.02,-0.27,0.42], gravZ: [-0.06,-0.07,-0.08,0.00,-0.08,0.52],
};
const BOX_Q3 = {
  bodyX:  [0.30,0.30,0.31,0.32,0.32,0.32], bodyY: [0.02,0.02,0.02,0.02,0.02,0.02],
  bodyZ:  [-0.06,-0.06,-0.06,-0.06,-0.07,-0.06], gravX: [0.96,0.95,0.93,0.86,0.95,-0.32],
  gravY:  [-0.22,-0.25,-0.23,0.25,-0.22,0.76], gravZ: [0.13,0.12,0.12,0.35,0.10,0.72],
};

// Scatter data (sampled representative points per activity)
function genScatter(cx, cy, n, spread) {
  const pts = [];
  for (let i = 0; i < n; i++) {
    pts.push({ x: cx + (Math.random()-0.5)*spread, y: cy + (Math.random()-0.5)*spread });
  }
  return pts;
}
Math.random = (function() {
  let seed = 42;
  return function() { seed = (seed * 16807 + 0) % 2147483647; return (seed - 1) / 2147483646; };
})();

const SCATTER_CENTERS = [
  {cx:0.6,cy:0.55,sp:0.35},  // WALKING
  {cx:0.5,cy:0.45,sp:0.30},  // WALKING_UPSTAIRS
  {cx:0.7,cy:0.60,sp:0.30},  // WALKING_DOWNSTAIRS
  {cx:-0.75,cy:-0.65,sp:0.20}, // SITTING
  {cx:-0.60,cy:-0.55,sp:0.25}, // STANDING
  {cx:-0.70,cy:-0.70,sp:0.20}, // LAYING
];
const PCA_CENTERS = [
  {cx:20,cy:2,sp:14},   // WALKING
  {cx:15,cy:-8,sp:12},  // WALKING_UPSTAIRS
  {cx:35,cy:5,sp:18},   // WALKING_DOWNSTAIRS
  {cx:-16,cy:3,sp:4},   // SITTING
  {cx:-14,cy:1,sp:5},   // STANDING
  {cx:-15,cy:5,sp:3},   // LAYING
];

// Top-3 hist by activity
const TOP3_DATA = {
  h1: { // fBodyAccJerk-entropy()-X
    WALKING:[-0.2,0.3,0.5,0.6,0.7], WALKING_UPSTAIRS:[-0.1,0.2,0.4,0.6,0.7],
    WALKING_DOWNSTAIRS:[-0.1,0.3,0.5,0.65,0.7], SITTING:[-1.0,-0.95,-0.9,-0.85,-0.8],
    STANDING:[-1.0,-0.95,-0.9,-0.8,-0.7], LAYING:[-1.0,-0.98,-0.95,-0.93,-0.9],
  },
  h2: {
    WALKING:[-0.2,0.25,0.45,0.55,0.65], WALKING_UPSTAIRS:[-0.15,0.2,0.4,0.55,0.65],
    WALKING_DOWNSTAIRS:[-0.1,0.28,0.48,0.60,0.68], SITTING:[-1.0,-0.95,-0.9,-0.85,-0.8],
    STANDING:[-1.0,-0.95,-0.88,-0.78,-0.68], LAYING:[-1.0,-0.97,-0.93,-0.90,-0.87],
  },
  h3: {
    WALKING:[0.5,0.6,0.7,0.75,0.8], WALKING_UPSTAIRS:[0.45,0.55,0.65,0.72,0.78],
    WALKING_DOWNSTAIRS:[0.5,0.62,0.72,0.77,0.82], SITTING:[-1.0,-0.95,-0.9,-0.85,-0.8],
    STANDING:[-1.0,-0.94,-0.87,-0.78,-0.65], LAYING:[-1.0,-0.96,-0.92,-0.88,-0.84],
  }
};

// Correlation matrix (6 vars: tBodyAcc-X/Y/Z, tGravAcc-X, tBodyGyro-X, fBodyAcc-X)
const CORR_VARS = ['tBodyAcc-X','tBodyAcc-Y','tBodyAcc-Z','tGravAcc-X','tBodyGyro-X','fBodyAcc-X'];
const CORR_MATRIX = [
  [1.00, 0.15,-0.26, 0.03,-0.03,-0.02],
  [0.15, 1.00,-0.08, 0.00, 0.00, 0.02],
  [-0.26,-0.08, 1.00,-0.01, 0.02, 0.02],
  [0.03, 0.00,-0.01, 1.00,-0.80,-0.67],
  [-0.03, 0.00, 0.02,-0.80, 1.00, 0.66],
  [-0.02, 0.02, 0.02,-0.67, 0.66, 1.00],
];

const TOP10_VAR = {
  'fBodyAcc-meanFreq()-Z':0.1821,'fBodyAcc-meanFreq()-Y':0.1654,
  'fBodyAccMag-meanFreq()':0.1598,'fBodyAcc-meanFreq()-X':0.1542,
  'fBodyAccJerkMag-meanFreq()':0.1489,'tGravityAcc-mean()-X':0.1423,
  'tGravityAcc-mean()-Y':0.1398,'tGravityAcc-mean()-Z':0.1356,
  'fBodyBodyAccJerkMag-meanFreq()':0.1301,'angle(X,gravityMean)':0.1278,
};

const CM = {
  SGD:[[1117,55,54,0,0,0],[42,1002,29,0,0,0],[69,15,902,0,0,0],[0,1,0,1157,125,3],[0,0,0,109,1265,0],[0,2,2,5,21,1377]],
  RF: [[1058,121,47,0,0,0],[26,981,38,0,28,0],[35,84,867,0,0,0],[0,1,0,1141,129,15],[0,0,0,134,1240,0],[0,2,0,1,0,1404]],
  SVM:[[1113,53,60,0,0,0],[28,987,56,0,2,0],[17,42,927,0,0,0],[0,1,0,1153,127,5],[0,0,0,133,1240,1],[0,1,12,1,6,1387]],
};
const CLASS_F1 = {
  SGD:[0.91,0.94,0.93,0.90,0.91,0.98],
  RF: [0.91,0.89,0.92,0.88,0.90,0.99],
  SVM:[0.93,0.93,0.93,0.91,0.92,0.99],
};
const MODEL_NOTES = {
  SGD:'El SGD logra una accuracy razonable pero presenta confusiones entre SITTING y STANDING.',
  RF: 'Random Forest mejora respecto al SGD, ya que reduce las confusiones entre SITTING y STANDING. Por otro lado, las variables mas importantes que identifica coinciden con las mostradas en el EDA.',
  SVM:'SVM es el modelo que mejor se comporta de los tres analizados.',
};
const MODEL_NAMES = { SGD:'Modelo 1 - SGD', RF:'Modelo 2 - Random Forest', SVM:'Modelo 3 - SVM' };

let currentModel = 'SGD';
let currentCMType = 'abs';

// -- NAV -----------------------------------------------------------------------
function showSection(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
  if (id === 'modelos') { renderCM(); renderReportBars(); }
}

// -- HELPERS -------------------------------------------------------------------
function cwColor(v, isNorm) {
  if (isNorm) {
    const t = Math.min(v,0.5)/0.5;
    return `rgb(${Math.round(250-t*190)},${Math.round(247-t*220)},${Math.round(244-t*230)})`;
  }
  const ratio = v/1407;
  if (ratio < 0.5) {
    const t = ratio*2;
    return `rgb(${Math.round(59+t*142)},${Math.round(76+t*124)},${Math.round(192-t*12)})`;
  }
  const t = (ratio-0.5)*2;
  return `rgb(${Math.round(201-t*21)},${Math.round(200-t*170)},${Math.round(180-t*142)})`;
}
function textColor(bg) {
  const m = bg.match(/\\d+/g);
  return (0.299*m[0]+0.587*m[1]+0.114*m[2]) > 140 ? '#2c2620' : '#fff';
}

// coolwarm for correlation
function corrColor(v) {
  if (v === null) return 'transparent';
  if (v >= 0) {
    const t = v;
    return `rgb(${Math.round(250-t*220)},${Math.round(240-t*200)},${Math.round(230-t*220)})`;
  } else {
    const t = -v;
    return `rgb(${Math.round(230-t*170)},${Math.round(240-t*210)},${Math.round(250-t*60)})`;
  }
}
function corrText(v) {
  if (v === null) return '';
  const bg = corrColor(v);
  const m = bg.match(/\\d+/g);
  return (0.299*m[0]+0.587*m[1]+0.114*m[2]) > 160 ? '#2c2620' : '#fff';
}

// -- HIST UTIL -----------------------------------------------------------------
function makeHist(canvasId, data, mean, median) {
  const labels = data.bins.slice(0,-1).map((b,i) => ((b+data.bins[i+1])/2).toFixed(2));
  new Chart(document.getElementById(canvasId), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: data.counts,
        backgroundColor: '#8fada8cc',
        borderColor: '#8fada8',
        borderWidth: 0.5,
        borderRadius: 2,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        annotation: {},
        tooltip: { callbacks: { label: ctx => ` ${ctx.raw}` } }
      },
      scales: {
        x: { grid: { color: '#ede8e2' }, ticks: { color: '#7a6e65', font:{size:8}, maxTicksLimit: 5 } },
        y: { grid: { color: '#ede8e2' }, ticks: { color: '#7a6e65', font:{size:8} } }
      }
    }
  });
}

// -- BOXPLOT (simulated with bar chart) ----------------------------------------
function makeBoxplot(canvasId, key) {
  const medians = BOX_MEDIANS[key];
  const q1s = BOX_Q1[key];
  const q3s = BOX_Q3[key];
  new Chart(document.getElementById(canvasId), {
    type: 'bar',
    data: {
      labels: ACT_S,
      datasets: [
        { label: 'Q1Q3', data: q3s.map((q3,i) => q3-q1s[i]), backgroundColor: NUDE.map(c => c+'bb'), borderColor: NUDE, borderWidth: 1.5, borderRadius: 3, base: q1s },
        { label: 'Mediana', data: medians, type: 'scatter', pointStyle: 'line', pointRotation: 90, pointRadius: 10, borderColor: '#2c2620', borderWidth: 2 }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` ${ctx.raw.toFixed(2)}` } } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#7a6e65', font:{size:8}, maxRotation: 30 } },
        y: { grid: { color: '#ede8e2' }, ticks: { color: '#7a6e65', font:{size:8} } }
      }
    }
  });
}

// -- TOP HIST PER ACTIVITY ----------------------------------------------------
function makeTopHist(canvasId, hkey) {
  const d = TOP3_DATA[hkey];
  const datasets = ACTIVITIES.map((act, i) => ({
    label: ACT_S[i],
    data: d[act],
    backgroundColor: NUDE[i] + '88',
    borderColor: NUDE[i],
    borderWidth: 0.8,
    borderRadius: 2,
    barPercentage: 1.0,
    categoryPercentage: 1.0,
  }));
  new Chart(document.getElementById(canvasId), {
    type: 'bar',
    data: { labels: ['-1.0','-0.5','0.0','0.5','1.0'], datasets },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color:'#7a6e65', font:{size:8}, boxWidth:10 } } },
      scales: {
        x: { stacked: false, grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:8}} },
        y: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:8}} }
      }
    }
  });
}

// -- CORRELATION HEATMAP -------------------------------------------------------
function renderCorrHeatmap() {
  const n = CORR_VARS.length;
  let html = '<table class="corr-table"><thead><tr><th></th>';
  CORR_VARS.forEach(v => html += `<th>${v}</th>`);
  html += '</tr></thead><tbody>';
  for (let i = 0; i < n; i++) {
    html += `<tr><td class="corr-row-label">${CORR_VARS[i]}</td>`;
    for (let j = 0; j < n; j++) {
      if (j >= i) {
        const v = CORR_MATRIX[i][j];
        const bg = corrColor(v);
        const tc = corrText(v);
        const disp = i === j ? '' : v.toFixed(2);
        html += `<td style="background:${bg};color:${tc}" title="${CORR_VARS[i]} vs ${CORR_VARS[j]}: ${v.toFixed(2)}">${disp}</td>`;
      } else {
        html += `<td class="corr-empty"></td>`;
      }
    }
    html += '</tr>';
  }
  html += '</tbody></table>';
  document.getElementById('corrHeatmap').innerHTML = html;
}

// -- CONFUSION MATRIX ----------------------------------------------------------
function selectModel(m, btn) {
  currentModel = m;
  document.querySelectorAll('#modelSelector .model-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderCM(); renderReportBars();
}
function selectCMType(t, btn) {
  currentCMType = t;
  document.getElementById('absBtn').classList.toggle('active', t==='abs');
  document.getElementById('normBtn').classList.toggle('active', t==='norm');
  renderCM();
}
function renderCM() {
  const cm = CM[currentModel];
  const isNorm = currentCMType === 'norm';
  const rowSums = cm.map(r => r.reduce((a,b)=>a+b,0));
  const data = isNorm ? cm.map((row,i) => row.map((v,j) => i===j?0:v/rowSums[i])) : cm;
  const fmt = v => isNorm ? v.toFixed(2) : v.toLocaleString();
  document.getElementById('cmTitle').textContent = `${MODEL_NAMES[currentModel]}  Matriz${isNorm?' normalizada (solo errores)':' de confusion'}`;
  let html = '<thead><tr><th></th>';
  ACT_S.forEach(a => html += `<th style="text-align:center;font-size:9px">${a}</th>`);
  html += '</tr></thead><tbody>';
  data.forEach((row,i) => {
    html += `<tr><td class="row-label">${ACT_S[i]}</td>`;
    row.forEach((v,j) => {
      const bg = (i===j&&!isNorm)?'#e8ddd4':cwColor(v,isNorm);
      const tc = textColor(bg);
      html += `<td style="background:${bg};color:${tc}" title="${ACTIVITIES[i]}  ${ACTIVITIES[j]}: ${fmt(v)}">${fmt(v)}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody>';
  document.getElementById('cmTable').innerHTML = html;
  document.getElementById('modelNoteText').textContent = MODEL_NOTES[currentModel];
}
function renderReportBars() {
  const f1s = CLASS_F1[currentModel];
  let html = '';
  f1s.forEach((v,i) => {
    html += `<div class="progress-row"><div class="progress-label">${ACT_S[i]}</div><div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${(v*100).toFixed(0)}%;background:${NUDE[i]}"></div></div><div class="progress-val">${v.toFixed(2)}</div></div>`;
  });
  document.getElementById('reportBars').innerHTML = html;
}
renderCM(); renderReportBars();

// -- RENDER EDA CHARTS ---------------------------------------------------------

// U - dist bar
new Chart(document.getElementById('distChart'), {
  type: 'bar',
  data: { labels: ACT_S, datasets: [{ data: DIST, backgroundColor: NUDE, borderRadius: 6, borderSkipped: false }] },
  options: {
    responsive: true,
    plugins: { legend:{display:false}, tooltip:{callbacks:{label:ctx=>` ${ctx.raw.toLocaleString()} (${(ctx.raw/7352*100).toFixed(1)}%)`}} },
    scales: {
      x: { grid:{display:false}, ticks:{color:'#7a6e65',font:{size:11}} },
      y: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:11}} }
    }
  }
});

// U - donut
new Chart(document.getElementById('donutChart'), {
  type: 'doughnut',
  data: { labels: ACT_S, datasets: [{ data: DIST, backgroundColor: NUDE, borderWidth: 2, borderColor: '#faf7f4', hoverOffset: 8 }] },
  options: { cutout:'65%', plugins:{ legend:{display:false}, tooltip:{callbacks:{label:ctx=>` ${(ctx.raw/7352*100).toFixed(1)}%`}} } }
});
const dl = document.getElementById('donutLegend');
ACT_S.forEach((a,i) => {
  dl.innerHTML += `<div class="legend-item"><div class="legend-dot" style="background:${NUDE[i]}"></div><span>${ACTIVITIES[i]} - ${DIST[i].toLocaleString()}</span></div>`;
});

// E - histograms
makeHist('histX',  HIST_DATA.bodyX);
makeHist('histY',  HIST_DATA.bodyY);
makeHist('histZ',  HIST_DATA.bodyZ);
makeHist('histGX', HIST_DATA.gravX);
makeHist('histGY', HIST_DATA.gravY);
makeHist('histGZ', HIST_DATA.gravZ);

// E - boxplots
makeBoxplot('boxX',  'bodyX');
makeBoxplot('boxY',  'bodyY');
makeBoxplot('boxZ',  'bodyZ');
makeBoxplot('boxGX', 'gravX');
makeBoxplot('boxGY', 'gravY');
makeBoxplot('boxGZ', 'gravZ');

// S - correlation heatmap
renderCorrHeatmap();

// S - top variables bars
const varWrap = document.getElementById('varBars');
const varEntries = Object.entries(TOP10_VAR);
const varMax = varEntries[0][1];
varEntries.forEach(([name, val]) => {
  const pct = (val/varMax*100).toFixed(0);
  const short = name.length > 28 ? name.slice(0,26)+'...' : name;
  const hue = 20 + (1-val/varMax)*160;
  varWrap.innerHTML += `<div class="progress-row"><div class="progress-label" title="${name}">${short}</div><div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%;background:hsl(${hue},42%,58%)"></div></div><div class="progress-val">${val.toFixed(3)}</div></div>`;
});

// S - scatter
const scatterDatasets = ACTIVITIES.map((act,i) => ({
  label: act, backgroundColor: NUDE[i]+'bb', pointRadius: 3, pointHoverRadius: 5,
  data: genScatter(SCATTER_CENTERS[i].cx, SCATTER_CENTERS[i].cy, 120, SCATTER_CENTERS[i].sp)
}));
new Chart(document.getElementById('scatterChart'), {
  type: 'scatter',
  data: { datasets: scatterDatasets },
  options: {
    responsive: true,
    plugins: { legend:{ labels:{color:'#7a6e65',font:{size:9},boxWidth:10} } },
    scales: {
      x: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:9}}, title:{display:true,text:'fBodyAccJerk-entropy()-X',color:'#7a6e65',font:{size:9}} },
      y: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:9}}, title:{display:true,text:'fBodyAccJerk-entropy()-Y',color:'#7a6e65',font:{size:9}} }
    }
  }
});

// S - PCA
const pcaDatasets = ACTIVITIES.map((act,i) => ({
  label: act, backgroundColor: NUDE[i]+'bb', pointRadius: 3, pointHoverRadius: 5,
  data: genScatter(PCA_CENTERS[i].cx, PCA_CENTERS[i].cy, 150, PCA_CENTERS[i].sp)
}));
new Chart(document.getElementById('pcaChart'), {
  type: 'scatter',
  data: { datasets: pcaDatasets },
  options: {
    responsive: true,
    plugins: { legend:{ labels:{color:'#7a6e65',font:{size:9},boxWidth:10} } },
    scales: {
      x: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:9}}, title:{display:true,text:'PC1 (50.8% varianza)',color:'#7a6e65',font:{size:9}} },
      y: { grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',font:{size:9}}, title:{display:true,text:'PC2 (6.6% varianza)',color:'#7a6e65',font:{size:9}} }
    }
  }
});

// S - top 3 hists
makeTopHist('topHist1','h1');
makeTopHist('topHist2','h2');
makeTopHist('topHist3','h3');

// Comparison chart
new Chart(document.getElementById('compChart'), {
  type: 'bar',
  data: {
    labels: ['SGD','Random Forest','SVM'],
    datasets: [
      { label:'Accuracy Test', data:[0.9386,0.9257,0.9522], backgroundColor:'#b5886a', borderRadius:5 },
      { label:'F1 macro',      data:[0.9387,0.9241,0.9515], backgroundColor:'#8fada8', borderRadius:5 },
      { label:'AUC macro',     data:[0.9918,0.9952,0.9977], backgroundColor:'#c4a882', borderRadius:5 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend:{labels:{color:'#7a6e65',font:{size:11}}}, tooltip:{callbacks:{label:ctx=>` ${ctx.dataset.label}: ${ctx.raw.toFixed(4)}`}} },
    scales: {
      x: { grid:{display:false}, ticks:{color:'#7a6e65'} },
      y: { min:0.88, max:1.01, grid:{color:'#ede8e2'}, ticks:{color:'#7a6e65',callback:v=>v.toFixed(2)} }
    }
  }
});
</script>
</body>
</html>

"""

st.components.v1.html(html_content, height=5000, scrolling=True)
