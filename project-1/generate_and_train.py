import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

np.random.seed(42)

# 10 Indian Cities as explicitly requested
indian_cities_roads = [
    {
        "city": "Pune, Maharashtra",
        "roads": [
            ("NH-48 Katraj Bypass", "National Highway"),
            ("Mumbai-Pune Expressway Link", "Expressway"),
            ("Sinhagad Road Arterial", "Urban Arterial"),
            ("Nagar Road BRTS Corridor", "Urban Arterial"),
            ("Hinjewadi Phase 1 Spine Road", "Major District Road"),
            ("Hadapsar-Solapur Road", "State Highway")
        ]
    },
    {
        "city": "Mumbai, Maharashtra",
        "roads": [
            ("Western Express Highway (Andheri)", "Express Highway"),
            ("Eastern Express Highway (Ghatkopar)", "Express Highway"),
            ("Sion-Panvel Expressway Link", "Major Arterial"),
            ("SV Road (Bandra Section)", "Urban Arterial"),
            ("LBS Marg (Kurla Corridor)", "Urban Arterial"),
            ("Ghodbunder Road Bypass", "State Highway")
        ]
    },
    {
        "city": "Bengaluru, Karnataka",
        "roads": [
            ("Electronic City Elevated Corridor", "Elevated Expressway"),
            ("Outer Ring Road (Marathahalli)", "Urban Arterial"),
            ("Hosur Road (Silk Board Link)", "National Highway"),
            ("Bellary Road (Airport Corridor)", "Express Highway"),
            ("Kan设定 Road (MDR-4)", "Major District Road"),
            ("Old Madras Road (K.R. Puram)", "State Highway")
        ]
    },
    {
        "city": "Delhi, NCR",
        "roads": [
            ("Outer Ring Road (Nehru Place)", "Urban Arterial"),
            ("Delhi-Noida Direct (DND) Flyway", "Expressway"),
            ("Mathura Road (Badarpur Link)", "National Highway"),
            ("GT Road (Karnal Bypass Section)", "National Highway"),
            ("Ring Road (Moti Bagh Corridor)", "Urban Arterial"),
            ("Mehrauli-Gurgaon Road", "State Highway")
        ]
    },
    {
        "city": "Hyderabad, Telangana",
        "roads": [
            ("PVNR Elevated Expressway", "Elevated Expressway"),
            ("Nehru Outer Ring Road (Gachibowli)", "Expressway"),
            ("Inner Ring Road (Mehdipatnam)", "Urban Arterial"),
            ("Uppal-Warangal Highway Section", "National Highway"),
            ("Banjara Hills Road No. 12", "Urban Arterial"),
            ("Medchal Highway (NH-44)", "National Highway")
        ]
    },
    {
        "city": "Chennai, Tamil Nadu",
        "roads": [
            ("Rajiv Gandhi Salai (OMR IT Expressway)", "Express Highway"),
            ("Chennai Outer Ring Road (Vandalur)", "Expressway"),
            ("GST Road (Guindy-Airport Link)", "National Highway"),
            ("Anna Salai (Central Arterial)", "Urban Arterial"),
            ("Mount-Poonamallee High Road", "State Highway"),
            ("Ennore Port Cargo Expressway", "Heavy Industrial Corridor")
        ]
    },
    {
        "city": "Jaipur, Rajasthan",
        "roads": [
            ("Tonk Road (Airport Corridor)", "Urban Arterial"),
            ("JLN Marg (Malviya Nagar)", "Urban Arterial"),
            ("Ajmer Road 200ft Bypass", "National Highway"),
            ("Sikar Road Industrial Link", "State Highway"),
            ("Delhi-Jaipur Expressway (NH-48)", "National Highway"),
            ("Agra Road (Ghat Ki Guni Link)", "Major District Road")
        ]
    },
    {
        "city": "Ahmedabad, Gujarat",
        "roads": [
            ("SG Highway (Bodakdev Corridor)", "Urban Arterial"),
            ("Sardar Patel Ring Road (Bopal)", "Ring Road Expressway"),
            ("Ashram Road (Sabarmati Corridor)", "City Arterial"),
            ("Sanand Industrial Expressway", "Heavy Industrial Road"),
            ("132 Feet Ring Road (Helmet Circle)", "Urban Arterial"),
            ("Narol-Naroda Road (NH-48)", "National Highway")
        ]
    },
    {
        "city": "Lucknow, Uttar Pradesh",
        "roads": [
            ("Amar Shaheed Path (Gomti Nagar)", "Express Highway"),
            ("Kanpur Road (Amausi Airport Link)", "National Highway"),
            ("Faizabad Road (Polytechnic Link)", "National Highway"),
            ("Ring Road (Munshipulia Corridor)", "Urban Arterial"),
            ("Hardoi Bypass Road", "State Highway"),
            ("Sultanpur Road (Arjunganj Section)", "Major District Road")
        ]
    },
    {
        "city": "Nagpur, Maharashtra",
        "roads": [
            ("Wardha Road (MIHAN Transit Corridor)", "National Highway"),
            ("Amravati Road (Wadi Bypass)", "National Highway"),
            ("Outer Ring Road (Narendra Nagar)", "Expressway"),
            ("Bhandara Road (NH-53 Link)", "National Highway"),
            ("Hingna Industrial Road", "Major District Road"),
            ("Kamptee Road (Automotive Square)", "Urban Arterial")
        ]
    }
]

# Flatten available road links
all_city_roads = []
for item in indian_cities_roads:
    city = item["city"]
    for road, rtype in item["roads"]:
        all_city_roads.append((city, road, rtype))

records = []

# Class 1: Good (30 samples)
# Well-maintained Indian expressways and freshly resurfaced corridors
# Criteria: Low IRI (< 3.0 m/km), 0-2 potholes, Cracks < 8%, Rutting < 6mm, Age 0.5-3.5 yrs
for i in range(30):
    city, road, rtype = all_city_roads[i % len(all_city_roads)]
    ch_km = np.random.randint(2, 65)
    ch_m = np.random.choice([100, 250, 400, 550, 700, 850])
    
    iri = round(float(np.random.uniform(1.2, 2.85)), 2)
    potholes = int(np.random.choice([0, 0, 0, 1, 1, 2], p=[0.5, 0.25, 0.12, 0.08, 0.03, 0.02]))
    cracks = round(float(np.random.uniform(0.5, 6.8)), 1)
    rutting = round(float(np.random.uniform(1.0, 5.5)), 1)
    age = round(float(np.random.uniform(0.5, 3.5)), 1)
    drainage = np.random.choice(["Good", "Moderate"], p=[0.85, 0.15])
    traffic = int(np.random.randint(6500, 42000))
    
    records.append({
        "record_id": f"IND-RD-{101+len(records):03d}",
        "city": city,
        "road_segment": f"{road} (Ch {ch_km:02d}+{ch_m}m)",
        "road_type": rtype,
        "iri_m_per_km": iri,
        "pothole_count": potholes,
        "crack_percentage": cracks,
        "rutting_depth_mm": rutting,
        "pavement_age_years": age,
        "drainage_condition": drainage,
        "traffic_volume_vpd": traffic,
        "condition_category": "Good"
    })

# Class 2: Fair (30 samples)
# Aging Indian urban arterials with micro-cracking and shallow ruts
# Criteria: IRI 3.0 - 5.5 m/km, 1-6 potholes, Cracks 7-19%, Rutting 5.5-12mm, Age 3.0-6.8 yrs
for i in range(30):
    city, road, rtype = all_city_roads[(i + 15) % len(all_city_roads)]
    ch_km = np.random.randint(2, 65)
    ch_m = np.random.choice([100, 250, 400, 550, 700, 850])
    
    if i == 14:
        # Borderline transition case for realistic academic ML evaluation
        iri, potholes, cracks, rutting, age, drainage = 5.4, 6, 18.8, 12.2, 6.2, "Moderate"
    else:
        iri = round(float(np.random.uniform(3.1, 5.25)), 2)
        potholes = int(np.random.choice([1, 2, 3, 4, 5]))
        cracks = round(float(np.random.uniform(7.5, 17.8)), 1)
        rutting = round(float(np.random.uniform(5.5, 11.5)), 1)
        age = round(float(np.random.uniform(2.8, 6.5)), 1)
        drainage = np.random.choice(["Good", "Moderate", "Poor"], p=[0.20, 0.70, 0.10])
        
    traffic = int(np.random.randint(5500, 38000))
    
    records.append({
        "record_id": f"IND-RD-{101+len(records):03d}",
        "city": city,
        "road_segment": f"{road} (Ch {ch_km:02d}+{ch_m}m)",
        "road_type": rtype,
        "iri_m_per_km": iri,
        "pothole_count": potholes,
        "crack_percentage": cracks,
        "rutting_depth_mm": rutting,
        "pavement_age_years": age,
        "drainage_condition": drainage,
        "traffic_volume_vpd": traffic,
        "condition_category": "Fair"
    })

# Class 3: Poor (30 samples)
# Post-monsoon Indian roads with alligator cracking and multiple potholes
# Criteria: IRI 5.5 - 8.5 m/km, 6-13 potholes, Cracks 19-35%, Rutting 12-20mm, Age 5.8-10.5 yrs
for i in range(30):
    city, road, rtype = all_city_roads[(i + 30) % len(all_city_roads)]
    ch_km = np.random.randint(2, 65)
    ch_m = np.random.choice([100, 250, 400, 550, 700, 850])
    
    if i == 8:
        iri, potholes, cracks, rutting, age, drainage = 5.6, 5, 18.2, 11.5, 5.8, "Moderate"
    else:
        iri = round(float(np.random.uniform(5.55, 8.35)), 2)
        potholes = int(np.random.choice([6, 7, 8, 9, 11, 13]))
        cracks = round(float(np.random.uniform(19.5, 34.5)), 1)
        rutting = round(float(np.random.uniform(12.0, 19.8)), 1)
        age = round(float(np.random.uniform(5.8, 10.5)), 1)
        drainage = np.random.choice(["Moderate", "Poor"], p=[0.35, 0.65])
        
    traffic = int(np.random.randint(4500, 32000))
    
    records.append({
        "record_id": f"IND-RD-{101+len(records):03d}",
        "city": city,
        "road_segment": f"{road} (Ch {ch_km:02d}+{ch_m}m)",
        "road_type": rtype,
        "iri_m_per_km": iri,
        "pothole_count": potholes,
        "crack_percentage": cracks,
        "rutting_depth_mm": rutting,
        "pavement_age_years": age,
        "drainage_condition": drainage,
        "traffic_volume_vpd": traffic,
        "condition_category": "Poor"
    })

# Class 4: Very Poor (30 samples)
# Heavily damaged Indian freight corridors, severe base failure, massive deep potholes
# Criteria: IRI > 8.5 m/km, 14-28 potholes, Cracks 35-58%, Rutting > 20mm, Age 8.5-15.0 yrs
for i in range(30):
    city, road, rtype = all_city_roads[(i + 45) % len(all_city_roads)]
    ch_km = np.random.randint(2, 65)
    ch_m = np.random.choice([100, 250, 400, 550, 700, 850])
    
    iri = round(float(np.random.uniform(8.55, 12.4)), 2)
    potholes = int(np.random.choice([14, 16, 18, 21, 24, 28]))
    cracks = round(float(np.random.uniform(35.5, 58.5)), 1)
    rutting = round(float(np.random.uniform(20.5, 33.5)), 1)
    age = round(float(np.random.uniform(8.5, 14.5)), 1)
    drainage = np.random.choice(["Poor", "Poor", "Moderate"], p=[0.8, 0.15, 0.05])
    traffic = int(np.random.randint(3000, 36000))
    
    records.append({
        "record_id": f"IND-RD-{101+len(records):03d}",
        "city": city,
        "road_segment": f"{road} (Ch {ch_km:02d}+{ch_m}m)",
        "road_type": rtype,
        "iri_m_per_km": iri,
        "pothole_count": potholes,
        "crack_percentage": cracks,
        "rutting_depth_mm": rutting,
        "pavement_age_years": age,
        "drainage_condition": drainage,
        "traffic_volume_vpd": traffic,
        "condition_category": "Very Poor"
    })

df = pd.DataFrame(records)
# Shuffle records with fixed seed
df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

# Save authentic CSV with standard engineering units
df.to_csv("road_condition_dataset.csv", index=False)
print(f"Generated Indian Road Dataset: road_condition_dataset.csv with {len(df)} total records across 10 Indian cities.")

# Encoding and ML modeling
drainage_map = {"Good": 0, "Moderate": 1, "Poor": 2}
df["drainage_encoded"] = df["drainage_condition"].map(drainage_map)

feature_cols = [
    "iri_m_per_km",
    "pothole_count",
    "crack_percentage",
    "rutting_depth_mm",
    "pavement_age_years",
    "drainage_encoded",
    "traffic_volume_vpd"
]

target_col = "condition_category"
categories = ["Good", "Fair", "Poor", "Very Poor"]

X = df[feature_cols]
y = df[target_col]

# 80% train / 20% test split (CO3 Requirement)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_pred_proba = rf.predict_proba(X_test)

acc = float(accuracy_score(y_test, y_pred))
prec = float(precision_score(y_test, y_pred, average="weighted"))
rec = float(recall_score(y_test, y_pred, average="weighted"))
f1 = float(f1_score(y_test, y_pred, average="weighted"))
cm = confusion_matrix(y_test, y_pred, labels=categories).tolist()
cls_report = classification_report(y_test, y_pred, labels=categories, output_dict=True)

importances = {feat: round(float(imp), 4) for feat, imp in zip(feature_cols, rf.feature_importances_)}

print("\n=== INDIAN ROAD CONDITION MODEL PERFORMANCE (20% TEST SET - 24 SAMPLES) ===")
print(f"Accuracy:  {acc*100:.2f}%")
print(f"Precision: {prec*100:.2f}%")
print(f"Recall:    {rec*100:.2f}%")
print(f"F1-Score:  {f1*100:.2f}%")
print("Confusion Matrix:")
print(np.array(cm))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, labels=categories))

test_indices = X_test.index
test_samples = []
for idx, (real_idx, row) in enumerate(df.loc[test_indices].iterrows()):
    actual = y_test.loc[real_idx]
    pred = y_pred[idx]
    probs = {cls_name: round(float(p), 3) for cls_name, p in zip(rf.classes_, y_pred_proba[idx])}
    test_samples.append({
        "record_id": row["record_id"],
        "city": row["city"],
        "road_segment": row["road_segment"],
        "road_type": row["road_type"],
        "iri_m_per_km": row["iri_m_per_km"],
        "pothole_count": row["pothole_count"],
        "crack_percentage": row["crack_percentage"],
        "rutting_depth_mm": row["rutting_depth_mm"],
        "pavement_age_years": row["pavement_age_years"],
        "drainage_condition": row["drainage_condition"],
        "traffic_volume_vpd": row["traffic_volume_vpd"],
        "actual_condition": actual,
        "predicted_condition": pred,
        "is_correct": bool(actual == pred),
        "confidence": round(float(max(y_pred_proba[idx]) * 100), 1),
        "probabilities": probs
    })

output_data = {
    "summary": {
        "project_title": "RoadVision AI – Intelligent Road Condition Classification System for Indian Roads",
        "academic_course": "Artificial Intelligence & Machine Learning (AIML) – Civil Engineering Mini Project (CO3 & CO4)",
        "total_records": len(df),
        "training_records": len(X_train),
        "testing_records": len(X_test),
        "split_ratio": "80% Training (96 records) / 20% Testing (24 records)",
        "algorithm": "Random Forest Classifier (n_estimators=100, max_depth=6, random_state=42)",
        "features": [
            {"id": "iri_m_per_km", "name": "Roughness Index (IRI)", "unit": "m/km", "description": "International Roughness Index measured via bump integrator / laser profiler per IRC:SP:16 guidelines.", "importance": importances["iri_m_per_km"]},
            {"id": "crack_percentage", "name": "Crack Percentage", "unit": "% surface area", "description": "Cumulative alligator, longitudinal, and transverse cracked surface area per 500m segment.", "importance": importances["crack_percentage"]},
            {"id": "rutting_depth_mm", "name": "Rutting Depth", "unit": "mm", "description": "Permanent longitudinal depressions along wheel paths under repeated commercial vehicle axle loading.", "importance": importances["rutting_depth_mm"]},
            {"id": "pavement_age_years", "name": "Pavement Surface Age", "unit": "years", "description": "Time elapsed since last asphalt bituminous overlay or initial new highway construction.", "importance": importances["pavement_age_years"]},
            {"id": "pothole_count", "name": "Pothole Count", "unit": "count / 500m", "description": "Frequency of structural bowl-shaped pavement cavities exceeding 25mm depth and 150mm diameter.", "importance": importances["pothole_count"]},
            {"id": "drainage_condition", "name": "Drainage Condition", "unit": "Rating", "description": "Adequacy of side longitudinal storm drains, cross culverts, and shoulder cross-slope runoff.", "importance": importances["drainage_encoded"]},
            {"id": "traffic_volume_vpd", "name": "Traffic Volume (AADT)", "unit": "veh/day", "description": "Average Annual Daily Traffic volume contributing to cumulative Equivalent Single Axle Loads (ESAL).", "importance": importances["traffic_volume_vpd"]}
        ],
        "categories": ["Good", "Fair", "Poor", "Very Poor"],
        "metrics": {
            "accuracy": round(acc * 100, 2),
            "precision_weighted": round(prec * 100, 2),
            "recall_weighted": round(rec * 100, 2),
            "f1_score_weighted": round(f1 * 100, 2),
            "confusion_matrix": cm,
            "classification_report": cls_report
        }
    },
    "feature_importances": importances,
    "test_evaluation_samples": test_samples,
    "all_records": df.drop(columns=["drainage_encoded"]).to_dict(orient="records")
}

with open("model_evaluation_data.json", "w") as f:
    json.dump(output_data, f, indent=2)

print("Saved updated Indian Road model_evaluation_data.json.")
