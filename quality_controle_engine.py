import numpy as np
import pandas as pd

# 1. Simulate 500 manufactured parts (e.g., fastener/component dimensions in mm)
# Specification Limits: Target = 50.0 mm, Upper Spec (USL) = 50.8 mm, Lower Spec (LSL) = 49.2 mm
np.random.seed(101)
n_samples = 500
target = 50.0
usl = 50.8
lsl = 49.2

# Simulate production measurements with a slight natural variation
measurements = np.random.normal(loc=50.04, scale=0.18, size=n_samples)

df = pd.DataFrame(
    {
        "Part_ID": [f"PART-{i:03d}" for i in range(1, n_samples + 1)],
        "Dimension_mm": np.round(measurements, 3),
    }
)

# 2. Calculate Statistical Process Control (SPC) Metrics
mean_val = df["Dimension_mm"].mean()
std_val = df["Dimension_mm"].std(ddof=1)

# Process Capability Ratio (Cp) and Index (Cpk)
cp = (usl - lsl) / (6 * std_val)
cpk = min(
    (usl - mean_val) / (3 * std_val), (mean_val - lsl) / (3 * std_val)
)

# 3. Quality Verification (Pass/Fail against tolerances)
df["Spec_Status"] = np.where(
    (df["Dimension_mm"] >= lsl) & (df["Dimension_mm"] <= usl), "PASS", "FAIL"
)

# Calculate defect rate in PPM (Parts Per Million)
fail_count = (df["Spec_Status"] == "FAIL").sum()
ppm_defective = (fail_count / n_samples) * 1_000_000

print("--- QUALITY CONTROL ENGINE REPORT ---")
print(f"Total Parts Inspected: {n_samples}")
print(f"Process Mean: {mean_val:.3f} mm (Target: {target} mm)")
print(f"Process Capability (Cp): {cp:.2f}")
print(f"Process Capability Index (Cpk): {cpk:.2f}")
print(f"Defect Rate: {ppm_defective:.0f} PPM")

# 4. Export Inspection Data to Excel
output_file = "Quality_Control_Inspection_Report.xlsx"
df.to_excel(output_file, index=False)
print(f"Success: Quality report saved to '{output_file}'!")

