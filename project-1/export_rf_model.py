import json
import numpy as np
from generate_and_train import rf, feature_cols, X_test, y_test, y_pred, y_pred_proba

trees_data = []

for estimator in rf.estimators_:
    tree = estimator.tree_
    tree_dict = {
        "left": tree.children_left.tolist(),
        "right": tree.children_right.tolist(),
        "feature": tree.feature.tolist(),
        "threshold": [round(float(t), 4) if t != -2 else -2 for t in tree.threshold],
        "value": [v[0].tolist() for v in tree.value]  # class distribution according to rf.classes_
    }
    trees_data.append(tree_dict)

rf_export = {
    "feature_names": feature_cols,
    "classes": rf.classes_.tolist(), # ['Fair', 'Good', 'Poor', 'Very Poor']
    "n_classes": len(rf.classes_),
    "trees": trees_data
}

js_content = f"""// RoadVision AI - Client-side Random Forest Classifier Runtime
// Auto-generated from Python scikit-learn RandomForestClassifier(n_estimators=100, max_depth=6)
// Trained on 80% split (96 records) of IRC:82 Road Condition Dataset

const ROAD_VISION_RF_MODEL = {json.dumps(rf_export, indent=None)};

function predictRoadCondition(inputFeatures) {{
    // inputFeatures: [iri_m_per_km, pothole_count, crack_percentage, rutting_depth_mm, pavement_age_years, drainage_encoded, traffic_volume_vpd]
    const classes = ROAD_VISION_RF_MODEL.classes;
    const nClasses = classes.length;
    const votes = new Array(nClasses).fill(0);
    
    ROAD_VISION_RF_MODEL.trees.forEach(tree => {{
        let node = 0;
        while (tree.feature[node] !== -2) {{
            const featIdx = tree.feature[node];
            const threshold = tree.threshold[node];
            const val = inputFeatures[featIdx];
            if (val <= threshold) {{
                node = tree.left[node];
            }} else {{
                node = tree.right[node];
            }}
        }}
        // Leaf node reached
        const leafValues = tree.value[node];
        const sumVal = leafValues.reduce((a, b) => a + b, 0);
        if (sumVal > 0) {{
            for (let c = 0; c < nClasses; c++) {{
                votes[c] += leafValues[c] / sumVal;
            }}
        }}
    }});
    
    const totalVotes = votes.reduce((a, b) => a + b, 0);
    const probabilities = {{}};
    let bestClassIndex = 0;
    let maxProb = -1;
    
    classes.forEach((cls, i) => {{
        const prob = totalVotes > 0 ? votes[i] / totalVotes : 0;
        probabilities[cls] = Math.round(prob * 1000) / 10; // percentage
        if (prob > maxProb) {{
            maxProb = prob;
            bestClassIndex = i;
        }}
    }});
    
    return {{
        predicted_condition: classes[bestClassIndex],
        confidence: Math.round(maxProb * 1000) / 10,
        probabilities: probabilities,
        class_index: bestClassIndex
    }};
}}

if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ predictRoadCondition, ROAD_VISION_RF_MODEL }};
}}
"""

with open("rf_model.js", "w") as f:
    f.write(js_content)

print("Updated rf_model.js with exact rf.classes_ alignment.")
