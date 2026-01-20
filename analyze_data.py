"""
COMPREHENSIVE DATA ANALYSIS SCRIPT
Analyzes all 3 government datasets for hackathon project
Generates insights, statistics, and recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

print("="*80)
print("MAHARASHTRA AADHAAR DATA - COMPREHENSIVE ANALYSIS")
print("Senior Data Analyst Report")
print("="*80)

# ===== ENROLLMENT DATA ANALYSIS =====
print("\n\n📊 1. ENROLLMENT DATA ANALYSIS")
print("-"*80)

enroll_df = pd.read_csv('Enrollment_Data.csv')
print(f"Dataset Shape: {enroll_df.shape[0]:,} rows × {enroll_df.shape[1]} columns")
print(f"\nColumns: {list(enroll_df.columns)}")
print(f"\nSample Data:\n{enroll_df.head(10)}")
print(f"\nData Types:\n{enroll_df.dtypes}")
print(f"\nMissing Values:\n{enroll_df.isnull().sum()}")
print(f"\nBasic Statistics:\n{enroll_df.describe()}")

# Clean and analyze
enroll_df.columns = [c.strip().lower() for c in enroll_df.columns]
enroll_df['date'] = pd.to_datetime(enroll_df['date'], format='%d-%m-%Y', errors='coerce')
enroll_df['district'] = enroll_df['district'].str.strip(). str.title()

print(f"\n📈 KEY INSIGHTS - ENROLLMENTS:")
print(f"  • Total Enrollments: {enroll_df[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum():,}")
print(f"  • Districts Covered: {enroll_df['district'].nunique()}")
print(f"  • Date Range: {enroll_df['date'].min()} to {enroll_df['date'].max()}")
print(f"  • Age 0-5: {enroll_df['age_0_5'].sum():,}")
print(f"  • Age 5-17: {enroll_df['age_5_17'].sum():,}")
print(f"  • Age 18+: {enroll_df['age_18_greater'].sum():,}")

# Top districts
total_enroll = enroll_df.groupby('district')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
total_enroll['total'] = total_enroll.sum(axis=1)
print(f"\n🏆 TOP 10 DISTRICTS BY ENROLLMENT:")
print(total_enroll.nlargest(10, 'total'))

# ===== BIOMETRIC DATA ANALYSIS =====
print("\n\n📊 2. BIOMETRIC DATA ANALYSIS")
print("-"*80)

bio_df = pd.read_csv('Biometric_Data.csv')
print(f"Dataset Shape: {bio_df.shape[0]:,} rows × {bio_df.shape[1]} columns")
print(f"\nColumns: {list(bio_df.columns)}")
print(f"\nSample Data:\n{bio_df.head(10)}")
print(f"\nData Types:\n{bio_df.dtypes}")
print(f"\nMissing Values:\n{bio_df.isnull().sum()}")

# Clean
bio_df.columns = [c.strip().lower() for c in bio_df.columns]
bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y', errors='coerce')
bio_df['district'] = bio_df['district'].str.strip().str.title()

bio_cols = [c for c in bio_df.columns if c.startswith('bio_')]
print(f"\n📈 KEY INSIGHTS - BIOMETRIC UPDATES:")
print(f"  • Total Biometric Updates: {bio_df[bio_cols].sum().sum():,}")
print(f"  • Districts Covered: {bio_df['district'].nunique()}")
print(f"  • Date Range: {bio_df['date'].min()} to {bio_df['date'].max()}")

for col in bio_cols:
    print(f"  • {col}: {bio_df[col].sum():,}")

# ===== DEMOGRAPHIC DATA ANALYSIS =====
print("\n\n📊 3. DEMOGRAPHIC DATA ANALYSIS")
print("-"*80)

demo_df = pd.read_csv('Demographic_Data.csv')
print(f"Dataset Shape: {demo_df.shape[0]:,} rows × {demo_df.shape[1]} columns")
print(f"\nColumns: {list(demo_df.columns)}")
print(f"\nSample Data:\n{demo_df.head(10)}")
print(f"\nData Types:\n{demo_df.dtypes}")
print(f"\nMissing Values:\n{demo_df.isnull().sum()}")

# Clean
demo_df.columns = [c.strip().lower() for c in demo_df.columns]
demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y', errors='coerce')
demo_df['district'] = demo_df['district'].str.strip().str.title()

demo_cols = [c for c in demo_df.columns if c.startswith('demo_')]
print(f"\n📈 KEY INSIGHTS - DEMOGRAPHIC UPDATES:")
print(f"  • Total Demographic Updates: {demo_df[demo_cols].sum().sum():,}")
print(f"  • Districts Covered: {demo_df['district'].nunique()}")
print(f"  • Date Range: {demo_df['date'].min()} to {demo_df['date'].max()}")

for col in demo_cols:
    print(f"  • {col}: {demo_df[col].sum():,}")

# ===== COMBINED ANALYSIS =====
print("\n\n🔍 4. COMBINED ANALYSIS & INSIGHTS")
print("-"*80)

# Merge all datasets
merged = pd.merge(enroll_df, bio_df, on=['date', 'district'], how='outer')
merged = pd.merge(merged, demo_df, on=['date', 'district'], how='outer')
merged.fillna(0, inplace=True)

# Calculate advanced metrics
merged['total_enrollment'] = merged['age_0_5'] + merged['age_5_17'] + merged['age_18_greater']
merged['total_biometric'] = merged[[c for c in merged.columns if 'bio_' in c]].sum(axis=1)
merged['total_demographic'] = merged[[c for c in merged.columns if 'demo_' in c]].sum(axis=1)

merged['total_activity'] = merged['total_enrollment'] + merged['total_biometric'] + merged['total_demographic']
merged['total_activity'] = merged['total_activity'].replace(0, 1)

# Migration Intensity (Demographic updates as % of total)
merged['migration_intensity'] = (merged['total_demographic'] / merged['total_activity']) * 10

# Pressure Index (Weighted load)
merged['pressure_index'] = (
    merged['total_enrollment'] * 1.0 +
    merged['total_biometric'] * 0.5 +
    merged['total_demographic'] * 0.2
)

print(f"📊 COMBINED DATASET:")
print(f"  • Total Records: {len(merged):,}")
print(f"  • Total Enrollments: {merged['total_enrollment'].sum():,}")
print(f"  • Total Biometric Updates: {merged['total_biometric'].sum():,}")
print(f"  • Total Demographic Updates: {merged['total_demographic'].sum():,}")
print(f"  • Total Government Operations: {merged['total_activity'].sum():,}")

# District-wise aggregation
district_summary = merged.groupby('district').agg({
    'total_enrollment': 'sum',
    'total_biometric': 'sum',
    'total_demographic': 'sum',
    'migration_intensity': 'mean',
    'pressure_index': 'mean'
}).round(2)

district_summary['total_ops'] = (district_summary['total_enrollment'] + 
                                  district_summary['total_biometric'] + 
                                  district_summary['total_demographic'])

print(f"\n🏆 TOP 15 HIGH-PRESSURE DISTRICTS:")
print(district_summary.nlargest(15, 'pressure_index'))

print(f"\n🚨 TOP 10 HIGH-MIGRATION DISTRICTS:")
print(district_summary.nlargest(10, 'migration_intensity')[['migration_intensity', 'total_demographic']])

# Save analysis outputs
print("\n\n💾 SAVING ANALYSIS OUTPUTS...")
district_summary.to_csv('district_analysis_output.csv')
merged.to_csv('combined_clean_data.csv', index=False)

# Generate insights JSON
insights = {
    "total_enrollments": int(merged['total_enrollment'].sum()),
    "total_biometric": int(merged['total_biometric'].sum()),
    "total_demographic": int(merged['total_demographic'].sum()),
    "unique_districts": int(merged['district'].nunique()),
    "high_pressure_districts": district_summary.nlargest(10, 'pressure_index').index.tolist(),
    "high_migration_districts": district_summary.nlargest(10, 'migration_intensity').index.tolist(),
    "avg_migration_intensity": float(merged['migration_intensity'].mean()),
    "avg_pressure_index": float(merged['pressure_index'].mean())
}

with open('analysis_insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("✅ Created: district_analysis_output.csv")
print("✅ Created: combined_clean_data.csv")
print("✅ Created: analysis_insights.json")

print("\n\n" + "="*80)
print("✅ ANALYSIS COMPLETE!")
print("="*80)
