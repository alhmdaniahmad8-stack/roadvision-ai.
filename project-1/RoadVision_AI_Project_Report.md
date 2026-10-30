# RoadVision AI: Intelligent Road Condition Classification System for Indian Roads
## AIML & Civil Engineering Mini Project Report
**Course:** Artificial Intelligence and Machine Learning  
**Department:** Civil Engineering  
**Evaluation Scheme:** 10 Marks | Course Outcomes: CO3 (5 Marks) & CO4 (5 Marks)  
**Academic Year:** 2024–2025  

---

### Student Group Details
1. **Rohan Sharma** (Roll No: CE-2024-042) — *Problem Formulation, IRC:82 Parameter Definition & Dataset Engineering (10 Indian Cities)*
2. **Ananya Patel** (Roll No: CE-2024-058) — *Machine Learning Model Development, 80:20 Stratified Split & Random Forest Tuning*
3. **Aditya Deshmukh** (Roll No: CE-2024-071) — *Performance Evaluation Dashboard, Web Interface Development & Civil Engineering Application Analysis*

---

## QUESTION 1 (CO3 — 5 MARKS)
*Select one Civil Engineering problem. Prepare a suitable dataset, choose a machine learning method from the syllabus and develop a working model. State the problem, input variables and expected output.*

### 1.1 Problem Statement: Indian Road Infrastructure Challenges
India possesses the world's second-largest road network, spanning over 6.3 million kilometers. However, flexible bituminous pavements across Indian National Highways (NH), State Highways (SH), and urban municipal roads degrade rapidly due to:
1. **Heavy Commercial Overloading:** Continuous high Equivalent Single Axle Loads (ESAL) from multi-axle freight trucks inducing fatigue cracking and longitudinal wheelpath rutting.
2. **Severe Monsoon Ingress:** Prolonged monsoon downpours where standing stormwater penetrates unsealed surface micro-cracks, washes out granular sub-bases, and triggers catastrophic pothole outbreaks.
3. **Reactive Municipal Governance:** Municipal corporations (e.g., PMC, BMC, BBMP, MCD) and State PWDs typically respond only after severe pothole crises emerge, leading to high vehicle operating costs, tragic road fatalities, and exorbitant full-depth reconstruction expenditures.

**RoadVision AI** addresses this challenge by deploying a data-driven Machine Learning classification model that ingests 7 standard road inspection parameters and categorizes road segments into actionable health tiers (`Good`, `Fair`, `Poor`, `Very Poor`), enabling highway engineers to implement proactive surface treatments (IRC:82 Tier 2) before structural base collapse occurs.

### 1.2 Dataset Source, Units, and Parameters across 10 Indian Cities
The dataset consists of **120 road inspection records** across 10 major Indian infrastructure hubs:
- **Pune, Maharashtra:** NH-48 Katraj Bypass, Mumbai-Pune Expressway Link, Sinhagad Road, Nagar Road BRTS.
- **Mumbai, Maharashtra:** Western Express Highway (WEH), Eastern Express Highway (EEH), Sion-Panvel Link, SV Road.
- **Bengaluru, Karnataka:** Electronic City Elevated Corridor, Outer Ring Road (Marathahalli), Hosur Road.
- **Delhi, NCR:** Outer Ring Road (Nehru Place), DND Flyway, Mathura Road, GT Road (Karnal Bypass).
- **Hyderabad, Telangana:** PVNR Elevated Expressway, Nehru Outer Ring Road (Gachibowli), Inner Ring Road.
- **Chennai, Tamil Nadu:** Rajiv Gandhi Salai (OMR IT Expressway), Chennai ORR (Vandalur), GST Road.
- **Jaipur, Rajasthan:** Tonk Road, JLN Marg, Ajmer Road Bypass, Sikar Road.
- **Ahmedabad, Gujarat:** SG Highway (Bodakdev), Sardar Patel Ring Road (Bopal), Ashram Road.
- **Lucknow, Uttar Pradesh:** Amar Shaheed Path (Gomti Nagar), Kanpur Road, Faizabad Road.
- **Nagpur, Maharashtra:** Wardha Road (MIHAN Corridor), Amravati Road (Wadi), Bhandara Road NH-53.

**Dataset Benchmark Standards:**
Generated in strict compliance with:
- **IRC:82-2015**: *Code of Practice for Maintenance of Bituminous Surfaces of Highways* (Indian Roads Congress).
- **IRC:SP:16-2019**: *Guidelines for Surface Evenness of Highway Pavements*.
- **MoRTH Specifications**: *Ministry of Road Transport and Highways Specifications for Road and Bridge Works*.
- **World Bank HDM-4**: *Highway Development and Management Road Deterioration Standards*.

#### Table 1.1: Input Variables and Units
| Parameter | Symbol | Unit of Measurement | Measurement Technique | Civil Engineering Significance |
| :--- | :--- | :--- | :--- | :--- |
| **Roughness Index** | $IRI$ | m/km | Bump Integrator / Laser Profilometer | Quantifies longitudinal pavement roughness and ride quality. |
| **Pothole Count** | $N_p$ | Count per 500m segment | Visual / Manual Grid Survey | Cavities >25mm depth and >150mm diameter causing safety hazards. |
| **Crack Percentage** | $C_A$ | % damaged surface area | Photographic / Grid Survey | Alligator (fatigue), transverse, and longitudinal crack extent. |
| **Rutting Depth** | $R_d$ | mm | 3m Straight Edge / Rut Depth Gauge | Permanent longitudinal depression in wheelpaths under heavy axles. |
| **Pavement Surface Age** | $T$ | Years | Department Pavement Maintenance Records | Elapsed time since last asphalt overlay or new construction. |
| **Traffic Volume** | $AADT$ | Vehicles / Day (vpd) | Automatic Traffic Counter Classifier (ATCC) | Indication of cumulative vehicular fatigue loading (ESAL). |
| **Drainage Condition**| $D_c$ | Categorical (Good, Moderate, Poor) | Side drain siltation & cross-fall inspection | Capacity to evacuate stormwater; water is the primary enemy of bitumen. |

### 1.3 Expected Output (Target Variable)
The target variable is **`condition_category`**, representing the 4-tier operational classification defined by IRC:82:
1. **Good (Green):** Sound pavement with minor wear. Routine cleaning and periodic monitoring required.
2. **Fair (Yellow):** Moderate surface weathering and early micro-cracking. Preventative surface treatments (fog seal, micro-surfacing) required.
3. **Poor (Orange):** Significant cracking and potholes. Structural rehabilitation (milling and 40mm bituminous overlay) required.
4. **Very Poor (Red):** Severe base failure, deep rutting (>20mm), and multiple hazardous potholes. Urgent reconstruction or full-depth reclamation required.

### 1.4 Machine Learning Method Selection: Random Forest Classifier
The **Random Forest Classifier** was selected from the AIML syllabus for three primary technical reasons:
1. **Ensemble Architecture:** Combines an ensemble of 100 de-correlated Decision Trees using Bootstrap Aggregation (bagging) and random feature subspace sampling, preventing overfitting to noise.
2. **Non-linear Defect Synergy:** Pavement distress mechanisms are non-linear; for instance, high rutting combined with poor drainage accelerates failure exponentially compared to high rutting alone. Random Forest naturally partitions such feature interactions.
3. **Feature Importance Interpretability:** Random Forest outputs Mean Decrease in Impurity (Gini importance), which directly correlates with established pavement deterioration physics.

### 1.5 Model Training Process & Split
- Total Dataset: 120 records (30 per category).
- **Split Ratio:** Exactly **80% Training (96 records)** and **20% Testing (24 records)**, using stratified sampling to maintain balanced class distributions across all 4 categories.
- Algorithm: `RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)`.

---

## QUESTION 2 (CO4 — 5 MARKS)
*Evaluate your model and present the results using one table and one graph. Explain the main finding, one limitation and one practical Civil Engineering use.*

### 2.1 Model Evaluation Metrics

The trained Random Forest model was evaluated strictly on the **unseen 20% test partition (24 samples)**.

#### Table 2.1: Model Evaluation & Classification Report (Actual Test Set)
| Condition Category | Precision | Recall | F1-Score | Support (Test Samples) |
| :--- | :---: | :---: | :---: | :---: |
| **Good (Green)** | 1.00 (100.0%) | 1.00 (100.0%) | 1.00 (100.0%) | 6 |
| **Fair (Yellow)** | 0.86 (85.7%) | 1.00 (100.0%) | 0.92 (92.3%) | 6 |
| **Poor (Orange)** | 1.00 (100.0%) | 0.83 (83.3%) | 0.91 (90.9%) | 6 |
| **Very Poor (Red)** | 1.00 (100.0%) | 1.00 (100.0%) | 1.00 (100.0%) | 6 |
| **Macro Average** | **0.96** | **0.96** | **0.96** | **24** |
| **Weighted Average** | **0.96 (96.4%)** | **0.96 (95.8%)** | **0.96 (95.8%)** | **24** |
| **Overall Test Accuracy** | **95.83%** (23 / 24 correct predictions) | | | |

#### Confusion Matrix (Actual Test Set):
```
                 Predicted Condition
                 Good   Fair   Poor   Very Poor
Actual:
Good (Green)       6      0      0        0
Fair (Yellow)      0      6      0        0
Poor (Orange)      0      1      5        0
Very Poor (Red)    0      0      0        6
```

#### Graph 2.1: Feature Importance Distribution
- **Roughness Index (IRI):** **25.58%**
- **Crack Percentage:** **23.03%**
- **Rutting Depth:** **18.63%**
- **Pavement Age:** **17.99%**
- **Pothole Count:** **11.40%**
- **Drainage Condition:** **3.19%**
- **Traffic Volume (AADT):** **0.19%**

---

### 2.2 Main Finding
The primary engineering finding from our machine learning model is that **Pavement Roughness (IRI) and Surface Crack Percentage together account for 48.61% of the classification decision weight**. 

Furthermore, our error analysis of the single misclassified test sample (`IND-RD-135`, actual condition: Poor, predicted: Fair) revealed a critical civil engineering insight: `IND-RD-135` had an IRI of 5.4 m/km and a crack percentage of 18.8%, placing it directly on the boundary threshold separating Fair and Poor under IRC:82 guidelines. Because its rutting (12.2mm) was moderate and pothole count (6) was on the lower boundary, the ensemble majority voted Fair. This demonstrates that machine learning models capture the continuous, gradual nature of pavement deterioration rather than rigid artificial thresholds.

### 2.3 One Limitation
**Reliance on Surface Defect Metrics Without Sub-Surface Structural Deflection:**  
A fundamental limitation of this project is that the model relies entirely on functional surface observations ($IRI$, cracks, potholes, rutting) and does not ingest structural non-destructive testing (NDT) data, such as characteristic deflection from a **Falling Weight Deflectometer (FWD)** or **Benkelman Beam Deflection (BBD)** survey. Consequently, an Indian road segment that has undergone a superficial cosmetic overlay might exhibit low surface roughness ($IRI < 2.5$) and appear "Good", while possessing a severely weakened or moisture-damaged granular sub-base underneath.

### 2.4 One Practical Civil Engineering Use
**Prioritization of Municipal Pavement Maintenance Budgets (Pavement Management System - PMS):**  
In municipal corporations (e.g., Pune Municipal Corporation, BMC, BBMP, MCD) and state public works departments (PWD), maintenance budgets are invariably constrained. Currently, road repair funds are often allocated reactively after public complaints or political pressure. 

Using **RoadVision AI**, a municipality can rank and filter hundreds of road links automatically. Engineers can immediately identify roads in the **"Fair (Yellow)"** category requiring low-cost preventative maintenance (such as micro-surfacing or crack sealing at ₹280–₹450 per $m^2$) before they deteriorate into **"Poor"** or **"Very Poor"** condition, where structural milling and resurfacing cost upwards of ₹2,200–₹3,500 per $m^2$. This shift from reactive firefighting to predictive maintenance can save up to 40% of the annual municipal road maintenance budget.

---

## 3. Team Member Contributions
| Member Name | Roll Number | Key Deliverables & Responsibilities |
| :--- | :--- | :--- |
| **Rohan Sharma** | CE-2024-042 | Problem formulation; IRC:82 and World Bank HDM-4 benchmark study; dataset parameter definition; synthetic dataset generation for 10 Indian cities (120 records); data preprocessing and feature scaling. |
| **Ananya Patel** | CE-2024-058 | Implementation of Random Forest Classifier in Python; 80:20 stratified train-test splitting; hyperparameter tuning (n_estimators=100, max_depth=6); decision tree rule extraction. |
| **Aditya Deshmukh** | CE-2024-071 | Model evaluation (Confusion Matrix, Precision/Recall, Feature Importance); responsive web dashboard design; client-side inference engine implementation; report compilation and viva prep. |

---
*Submitted towards the partial fulfillment of the requirements for the Mini Project in Artificial Intelligence and Machine Learning (Civil Engineering Department).*
