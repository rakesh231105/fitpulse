# ===============================
# MILESTONE 3: ANOMALY DETECTION
# ===============================

import pandas as pd
import os

# ===============================
# LOAD DATA (FROM MODULE 2)
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "outputs", "features.csv")

df = pd.read_csv(file_path)

# ===============================
# PREPROCESS
# ===============================

# Convert timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Convert numeric columns
cols = ['heart_rate_bpm', 'steps', 'spo2_pct']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ===============================
# RULE-BASED ANOMALY DETECTION
# ===============================

# Rules
df['rule_tachycardia'] = df['heart_rate_bpm'] > 120
df['rule_bradycardia'] = df['heart_rate_bpm'] < 45
df['rule_low_spo2'] = df['spo2_pct'] < 94
df['rule_sleep_steps'] = (df['steps'] > 50) & (df['sleeping'] > 0)

# ===============================
# ANOMALY SCORE
# ===============================

df['anomaly_score'] = (
    df['rule_tachycardia'].astype(int) +
    df['rule_bradycardia'].astype(int) +
    df['rule_low_spo2'].astype(int) +
    df['rule_sleep_steps'].astype(int)
)

# ===============================
# SEVERITY CLASSIFICATION
# ===============================

def get_severity(score):
    if score >= 3:
        return "high"
    elif score == 2:
        return "medium"
    elif score == 1:
        return "low"
    else:
        return "normal"

df['severity'] = df['anomaly_score'].apply(get_severity)

# ===============================
# SUMMARY PRINT
# ===============================

print("========== MODULE 3 SUMMARY ==========")
print("Total Records:", len(df))
print("Anomalies:", len(df[df['severity'] != "normal"]))
print("\nSeverity Breakdown:")
print(df['severity'].value_counts())

# ===============================
# SAVE OUTPUT (IMPORTANT)
# ===============================

output_path = os.path.join(BASE_DIR, "outputs", "anomaly_results.csv")

df.to_csv(output_path, index=False)


print("\n✅ anomaly_results.csv saved in outputs folder")

import os
print("Saving at:", output_path)