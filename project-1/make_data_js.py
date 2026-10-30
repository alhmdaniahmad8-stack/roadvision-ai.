import json

with open("model_evaluation_data.json", "r") as f:
    data = json.load(f)

js_content = f"""// RoadVision AI - Dataset and Model Evaluation Data
// Generated from Python scikit-learn Random Forest model training

const ROADVISION_DATA = {json.dumps(data, indent=2)};
"""

with open("data.js", "w") as f:
    f.write(js_content)

print("Generated data.js successfully!")
