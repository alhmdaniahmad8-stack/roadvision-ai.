import os

os.makedirs("assets", exist_ok=True)

# 1. Good Road SVG
svg_good = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%">
  <defs>
    <linearGradient id="skyGood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="60%" stop-color="#bae6fd"/>
      <stop offset="100%" stop-color="#f0f9ff"/>
    </linearGradient>
    <linearGradient id="asphaltGood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2d3748"/>
      <stop offset="100%" stop-color="#1a202c"/>
    </linearGradient>
    <linearGradient id="grassGood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4ade80"/>
      <stop offset="100%" stop-color="#16a34a"/>
    </linearGradient>
  </defs>
  
  <!-- Sky -->
  <rect width="600" height="180" fill="url(#skyGood)"/>
  <circle cx="500" cy="60" r="30" fill="#fef08a" opacity="0.9"/>
  <!-- Distant Hills -->
  <path d="M0,180 Q150,140 300,170 T600,165 L600,180 L0,180 Z" fill="#86efac" opacity="0.7"/>
  <path d="M0,180 Q200,150 420,180 L600,175 L600,180 L0,180 Z" fill="#4ade80" opacity="0.9"/>

  <!-- Roadside Shoulders (Grass/Earth) -->
  <polygon points="0,180 600,180 600,380 0,380" fill="url(#grassGood)"/>

  <!-- Road Pavement (Perspective) -->
  <polygon points="260,180 340,180 580,380 20,380" fill="url(#asphaltGood)"/>
  <!-- Shoulder Paved Edge Lines (Solid White) -->
  <polygon points="262,180 266,180 38,380 26,380" fill="#ffffff" opacity="0.9"/>
  <polygon points="334,180 338,180 574,380 562,380" fill="#ffffff" opacity="0.9"/>

  <!-- Center Lane Markings (Dashed Yellow - IRC Standard) -->
  <polygon points="298,185 302,185 303,205 297,205" fill="#facc15"/>
  <polygon points="297,220 303,220 305,250 295,250" fill="#facc15"/>
  <polygon points="295,268 305,268 308,310 292,310" fill="#facc15"/>
  <polygon points="292,332 308,332 312,380 288,380" fill="#facc15"/>

  <!-- Inspection Quality Badge Overlay -->
  <rect x="25" y="25" width="170" height="42" rx="8" fill="#0f172a" fill-opacity="0.85" stroke="#10b981" stroke-width="1.5"/>
  <circle cx="45" cy="46" r="6" fill="#10b981"/>
  <text x="60" y="44" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold">CATEGORY: GOOD</text>
  <text x="60" y="58" fill="#94a3b8" font-family="monospace" font-size="10">IRI: 1.8 m/km | Cracks: 2%</text>

  <!-- Technical Watermark -->
  <text x="580" y="365" fill="#ffffff" opacity="0.6" font-family="monospace" font-size="11" text-anchor="end">SURFACE PCI: 92/100 (SOUND)</text>
</svg>
"""

# 2. Fair Road SVG
svg_fair = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%">
  <defs>
    <linearGradient id="skyFair" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="70%" stop-color="#cbd5e1"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="asphaltFair" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>

  <rect width="600" height="180" fill="url(#skyFair)"/>
  <path d="M0,180 Q180,155 360,175 T600,170 L600,180 L0,180 Z" fill="#a1a1aa" opacity="0.6"/>

  <!-- Shoulder -->
  <polygon points="0,180 600,180 600,380 0,380" fill="#a3a3a3"/>

  <!-- Road Surface -->
  <polygon points="260,180 340,180 580,380 20,380" fill="url(#asphaltFair)"/>
  
  <!-- Shoulder Lines (Slightly Weathered) -->
  <polygon points="262,180 266,180 38,380 26,380" fill="#e2e8f0" opacity="0.75"/>
  <polygon points="334,180 338,180 574,380 562,380" fill="#e2e8f0" opacity="0.75"/>

  <!-- Center Line Markings -->
  <polygon points="298,185 302,185 303,205 297,205" fill="#facc15" opacity="0.85"/>
  <polygon points="297,220 303,220 305,250 295,250" fill="#facc15" opacity="0.85"/>
  <polygon points="295,268 305,268 308,310 292,310" fill="#facc15" opacity="0.85"/>
  <polygon points="292,332 308,332 312,380 288,380" fill="#facc15" opacity="0.85"/>

  <!-- Visible Hairline Cracks & Slight Wheelpath Rutting -->
  <path d="M160,330 Q175,320 185,325 T210,318 T230,325" fill="none" stroke="#1e293b" stroke-width="1.8" opacity="0.85"/>
  <path d="M190,322 L198,312" fill="none" stroke="#1e293b" stroke-width="1.5" opacity="0.85"/>
  <path d="M420,310 Q410,295 390,298 T360,288" fill="none" stroke="#1e293b" stroke-width="1.6" opacity="0.8"/>
  <path d="M220,260 Q235,255 250,262" fill="none" stroke="#1e293b" stroke-width="1.2" opacity="0.7"/>

  <!-- 1 Small Isolated Pothole / Sealed Patch -->
  <ellipse cx="210" cy="345" rx="14" ry="7" fill="#1e293b" opacity="0.85"/>
  <ellipse cx="210" cy="344" rx="12" ry="5" fill="#0f172a"/>

  <!-- Inspection Quality Badge Overlay -->
  <rect x="25" y="25" width="170" height="42" rx="8" fill="#0f172a" fill-opacity="0.85" stroke="#eab308" stroke-width="1.5"/>
  <circle cx="45" cy="46" r="6" fill="#eab308"/>
  <text x="60" y="44" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold">CATEGORY: FAIR</text>
  <text x="60" y="58" fill="#fef08a" font-family="monospace" font-size="10">IRI: 4.1 m/km | Cracks: 13%</text>

  <text x="580" y="365" fill="#ffffff" opacity="0.7" font-family="monospace" font-size="11" text-anchor="end">SURFACE PCI: 68/100 (PREVENTATIVE)</text>
</svg>
"""

# 3. Poor Road SVG
svg_poor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%">
  <defs>
    <linearGradient id="skyPoor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#94a3b8"/>
    </linearGradient>
    <linearGradient id="asphaltPoor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>

  <rect width="600" height="180" fill="url(#skyPoor)"/>
  
  <!-- Dusty/Eroded Shoulder -->
  <polygon points="0,180 600,180 600,380 0,380" fill="#78716c"/>

  <!-- Road Surface -->
  <polygon points="260,180 340,180 580,380 20,380" fill="url(#asphaltPoor)"/>

  <!-- Degraded Center Line -->
  <polygon points="298,185 302,185 303,205 297,205" fill="#d97706" opacity="0.6"/>
  <polygon points="297,220 303,220 304,242 296,242" fill="#d97706" opacity="0.5"/>
  <polygon points="295,275 305,275 307,305 293,305" fill="#d97706" opacity="0.6"/>

  <!-- Extensive Fatigue / Alligator Cracking Pattern -->
  <g stroke="#090d16" stroke-width="2.2" fill="none" opacity="0.9">
    <path d="M120,340 L150,330 L160,350 L130,360 Z"/>
    <path d="M150,330 L180,325 L190,345 L160,350 Z"/>
    <path d="M130,360 L160,350 L170,375 L140,380 Z"/>
    <path d="M180,325 L215,320 L225,340 L190,345 Z"/>
    <path d="M190,345 L225,340 L235,365 L200,370 Z"/>
    <path d="M370,300 L400,290 L420,310 L380,315 Z"/>
    <path d="M400,290 L430,285 L445,300 L420,310 Z"/>
  </g>

  <!-- Multiple Potholes with Depth Shading -->
  <!-- Pothole 1 -->
  <ellipse cx="230" cy="300" rx="22" ry="11" fill="#090d16"/>
  <ellipse cx="230" cy="302" rx="18" ry="8" fill="#020617"/>
  <path d="M212,298 Q228,304 246,298" stroke="#475569" stroke-width="1.5" fill="none"/>

  <!-- Pothole 2 -->
  <ellipse cx="380" cy="335" rx="28" ry="14" fill="#090d16"/>
  <ellipse cx="380" cy="337" rx="23" ry="10" fill="#020617"/>
  <path d="M360,332 Q380,340 402,332" stroke="#475569" stroke-width="1.8" fill="none"/>

  <!-- Pothole 3 (Smaller) -->
  <ellipse cx="170" cy="270" rx="14" ry="7" fill="#090d16"/>
  <ellipse cx="170" cy="271" rx="11" ry="5" fill="#020617"/>

  <!-- Inspection Quality Badge Overlay -->
  <rect x="25" y="25" width="170" height="42" rx="8" fill="#0f172a" fill-opacity="0.85" stroke="#f97316" stroke-width="1.5"/>
  <circle cx="45" cy="46" r="6" fill="#f97316"/>
  <text x="60" y="44" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold">CATEGORY: POOR</text>
  <text x="60" y="58" fill="#94a3b8" font-family="monospace" font-size="10">IRI: 6.8 m/km | Cracks: 26%</text>

  <text x="580" y="365" fill="#ffffff" opacity="0.8" font-family="monospace" font-size="11" text-anchor="end">SURFACE PCI: 44/100 (REHABILITATION)</text>
</svg>
"""

# 4. Very Poor Road SVG
svg_very_poor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%">
  <defs>
    <linearGradient id="skyVeryPoor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
    <linearGradient id="asphaltVeryPoor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>

  <rect width="600" height="180" fill="url(#skyVeryPoor)"/>

  <!-- Severely damaged eroded muddy edges -->
  <polygon points="0,180 600,180 600,380 0,380" fill="#57534e"/>

  <!-- Broken Road Bed -->
  <polygon points="260,180 340,180 580,380 20,380" fill="url(#asphaltVeryPoor)"/>

  <!-- Disintegrated Lane Marking Fragments -->
  <polygon points="298,185 302,185 303,195 297,195" fill="#b45309" opacity="0.4"/>
  <polygon points="296,280 302,280 303,292 295,292" fill="#b45309" opacity="0.3"/>

  <!-- Heavy Deep Rutting Channels -->
  <path d="M150,380 L230,220" stroke="#050811" stroke-width="12" opacity="0.8" fill="none"/>
  <path d="M430,380 L350,220" stroke="#050811" stroke-width="12" opacity="0.8" fill="none"/>

  <!-- Massive Alligator Cracking Network -->
  <g stroke="#020617" stroke-width="2.5" fill="none" opacity="0.95">
    <path d="M60,360 L95,345 L115,365 L75,375 Z"/>
    <path d="M95,345 L130,340 L145,355 L115,365 Z"/>
    <path d="M130,340 L160,335 L175,350 L145,355 Z"/>
    <path d="M260,330 L300,320 L315,340 L280,350 Z"/>
    <path d="M300,320 L340,315 L355,335 L315,340 Z"/>
    <path d="M440,360 L480,345 L505,370 L465,380 Z"/>
    <path d="M480,345 L520,340 L540,360 L505,370 Z"/>
  </g>

  <!-- Large Hazardous Potholes with Granular Base Exposure (Mud/Gravel) -->
  <!-- Mega Pothole 1 (Center Left) -->
  <ellipse cx="220" cy="340" rx="38" ry="20" fill="#020617"/>
  <ellipse cx="220" cy="342" rx="32" ry="15" fill="#451a03"/>
  <circle cx="215" cy="343" r="4" fill="#78350f"/>
  <circle cx="230" cy="340" r="3" fill="#78350f"/>
  <path d="M190,335 Q220,350 255,335" stroke="#991b1b" stroke-width="2" fill="none"/>

  <!-- Mega Pothole 2 (Right) -->
  <ellipse cx="410" cy="310" rx="32" ry="16" fill="#020617"/>
  <ellipse cx="410" cy="312" rx="27" ry="12" fill="#451a03"/>
  <circle cx="405" cy="313" r="3.5" fill="#78350f"/>

  <!-- Mega Pothole 3 (Near Distance) -->
  <ellipse cx="290" cy="240" rx="18" ry="9" fill="#020617"/>
  <ellipse cx="290" cy="241" rx="14" ry="6" fill="#451a03"/>

  <!-- Road Edge Breakup / Raveling -->
  <polygon points="30,370 70,350 60,380 20,380" fill="#78350f" opacity="0.9"/>
  <polygon points="530,350 575,370 580,380 540,380" fill="#78350f" opacity="0.9"/>

  <!-- Inspection Quality Badge Overlay -->
  <rect x="25" y="25" width="185" height="42" rx="8" fill="#0f172a" fill-opacity="0.85" stroke="#ef4444" stroke-width="1.5"/>
  <circle cx="45" cy="46" r="6" fill="#ef4444"/>
  <text x="60" y="44" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold">CATEGORY: VERY POOR</text>
  <text x="60" y="58" fill="#f87171" font-family="monospace" font-size="10">IRI: 10.2 m/km | Cracks: 45%</text>

  <text x="580" y="365" fill="#ef4444" opacity="0.9" font-family="monospace" font-size="11" text-anchor="end">SURFACE PCI: 18/100 (RECONSTRUCTION REQUIRED)</text>
</svg>
"""

# 5. Hero Banner Background SVG
svg_hero = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 650" width="100%" height="100%">
  <defs>
    <linearGradient id="heroSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070c1a"/>
      <stop offset="40%" stop-color="#0c1730"/>
      <stop offset="100%" stop-color="#142347"/>
    </linearGradient>
    <linearGradient id="roadSurf" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#16223d"/>
      <stop offset="100%" stop-color="#0a101f"/>
    </linearGradient>
    <linearGradient id="glowYellow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.4"/>
    </linearGradient>
    <pattern id="gridPattern" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.7" opacity="0.3"/>
    </pattern>
  </defs>

  <rect width="1200" height="650" fill="url(#heroSky)"/>
  <rect width="1200" height="650" fill="url(#gridPattern)"/>

  <!-- Distant Tech Mountains / Highway Landscape -->
  <path d="M0,340 Q300,280 600,320 T1200,300 L1200,650 L0,650 Z" fill="#0f192e" opacity="0.7"/>

  <!-- Modern Express Highway Perspective -->
  <polygon points="540,320 660,320 1150,650 50,650" fill="url(#roadSurf)"/>

  <!-- Pavement Grid / Laser Inspection Scanning Mesh -->
  <polygon points="540,320 660,320 1150,650 50,650" fill="none" stroke="#38bdf8" stroke-width="0.5" opacity="0.15"/>
  <line x1="560" y1="320" x2="250" y2="650" stroke="#38bdf8" stroke-width="0.8" opacity="0.2"/>
  <line x1="580" y1="320" x2="450" y2="650" stroke="#38bdf8" stroke-width="0.8" opacity="0.2"/>
  <line x1="620" y1="320" x2="750" y2="650" stroke="#38bdf8" stroke-width="0.8" opacity="0.2"/>
  <line x1="640" y1="320" x2="950" y2="650" stroke="#38bdf8" stroke-width="0.8" opacity="0.2"/>

  <!-- Horizontal Laser Scan Line (AI Scanning Simulation) -->
  <line x1="320" y1="460" x2="880" y2="460" stroke="#00f5ff" stroke-width="2.5" opacity="0.85"/>
  <line x1="280" y1="460" x2="920" y2="460" stroke="#38bdf8" stroke-width="6" opacity="0.2" filter="blur(3px)"/>

  <!-- Scanning Target Box / Inspection Node -->
  <rect x="520" y="440" width="160" height="40" rx="4" fill="#0369a1" fill-opacity="0.35" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="600" y="465" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">SCANNING PAVEMENT: IRI 2.4</text>

  <!-- Side Shoulder Markings -->
  <polygon points="542,320 548,320 78,650 62,650" fill="#ffffff" opacity="0.85"/>
  <polygon points="652,320 658,320 1138,650 1122,650" fill="#ffffff" opacity="0.85"/>

  <!-- Glowing Yellow Highway Centerline (Road Inspired) -->
  <polygon points="597,325 603,325 604,355 596,355" fill="url(#glowYellow)"/>
  <polygon points="595,380 605,380 607,430 593,430" fill="url(#glowYellow)"/>
  <polygon points="592,460 608,460 612,530 588,530" fill="url(#glowYellow)"/>
  <polygon points="586,565 614,565 620,650 580,650" fill="url(#glowYellow)"/>

  <!-- HUD Coordinates & Engineering telemetry -->
  <text x="40" y="50" fill="#64748b" font-family="monospace" font-size="12">STATION: CH 14+250m | ROAD ASSET: NH-48 EXP</text>
  <text x="40" y="70" fill="#38bdf8" font-family="monospace" font-size="11">MODEL: RANDOM FOREST CLASSIFIER (100 TREES)</text>
  <text x="1160" y="50" fill="#10b981" font-family="monospace" font-size="12" text-anchor="end">STATUS: REAL-TIME AI ACTIVE</text>
  <text x="1160" y="70" fill="#94a3b8" font-family="monospace" font-size="11" text-anchor="end">IRC:82-2015 COMPLIANT</text>
</svg>
"""

with open("assets/road-good.svg", "w") as f:
    f.write(svg_good)
with open("assets/road-fair.svg", "w") as f:
    f.write(svg_fair)
with open("assets/road-poor.svg", "w") as f:
    f.write(svg_poor)
with open("assets/road-very-poor.svg", "w") as f:
    f.write(svg_very_poor)
with open("assets/hero-road.svg", "w") as f:
    f.write(svg_hero)

print("Created all 5 custom SVG assets in assets/ directory!")
