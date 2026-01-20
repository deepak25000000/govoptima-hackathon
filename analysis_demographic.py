"""
DEMOGRAPHIC DATA ANALYSIS
Comprehensive analysis of Demographic_Data.csv for GovOptima Platform
Focuses on migration patterns and population movement
Author: Senior Data Analyst
Date: January 2026
"""

import pandas as pd
import numpy as np
import os

os.makedirs('analysis_outputs', exist_ok=True)

print("="*80)
print("🌍 DEMOGRAPHIC DATA ANALYSIS")
print("="*80)

# ===== 1. DATA LOADING =====
print("\n1. LOADING DATA...")
df = pd.read_csv('Demographic_Data.csv')
print(f"✓ Loaded {len(df):,} records")

# ===== 2. DATA EXPLORATION =====
print("\n2. DATA EXPLORATION")
print(f"  Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Columns: {list(df.columns)}")
print(f"\n  Sample Records:\n{df.head(10)}")

# ===== 3. DATA CLEANING =====
print("\n3. DATA CLEANING")

df.columns = [c.strip().lower() for c in df.columns]
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
df['district'] = df['district'].astype(str).str.strip().str.title()
df['district'] = df['district'].replace({
    'Mumbai( Sub Urban )': 'Mumbai Suburban',
    'Ahmed Nagar': 'Ahmadnagar',
    'Bid': 'Beed',
    'Buldhana': 'Buldana'
})
df.fillna(0, inplace=True)
print("  ✓ Data cleaned and standardized")

# ===== 4. DEMOGRAPHIC UPDATE ANALYSIS =====
print("\n4. DEMOGRAPHIC UPDATE ANALYSIS")

demo_cols = [c for c in df.columns if c.startswith('demo_')]
df['total_demographic_updates'] = df[demo_cols].sum(axis=1)

print(f"\n  📊 DEMOGRAPHIC UPDATE STATISTICS:")
for col in demo_cols:
    total = df[col].sum()
    print(f"    • {col}: {total:,}")

print(f"    • TOTAL UPDATES: {df['total_demographic_updates'].sum():,}")

# ===== 5. MIGRATION PATTERN DETECTION =====
print("\n5. MIGRATION PATTERN ANALYSIS")

district_demo = df.groupby('district').agg({
    'total_demographic_updates': 'sum'
})

# Calculate migration intensity (high demographic updates = likely migration/address changes)
district_demo['migration_intensity_score'] = (
    district_demo['total_demographic_updates'] / 
    district_demo['total_demographic_updates'].max() * 100
)

district_demo = district_demo.sort_values('migration_intensity_score', ascending=False)

print("\n  🚨 HIGH MIGRATION DISTRICTS (Top 15):")
print(district_demo.head(15))

# ===== 6. URBANIZATION INDICATORS =====
print("\n6. URBANIZATION INDICATORS")

# High demographic updates often indicate urban migration
high_migration = district_demo[district_demo['migration_intensity_score'] > 50]

print(f"\n  🏙️ DISTRICTS WITH HIGH MIGRATION SIGNALS:")
print(f"    • Count: {len(high_migration)} districts")
print(f"    • These districts likely experiencing urban influx or high mobility")

print(f"\n  Top 5 High-Migration Districts:")
for idx, (district, row) in enumerate(high_migration.head(5).iterrows(), 1):
    print(f"    {idx}. {district}: {row['total_demographic_updates']:,} updates (Score: {row['migration_intensity_score']:.1f})")

# ===== 7. TEMPORAL ANALYSIS =====
print("\n7. TEMPORAL MIGRATION PATTERNS")

monthly_demo = df.groupby(df['date'].dt.to_period('M'))['total_demographic_updates'].sum()
print(f"\n  📅 MONTHLY DEMOGRAPHIC UPDATE TRENDS:")
print(monthly_demo.head(12))

# ===== 8. RESOURCE IMPACT ASSESSMENT =====
print("\n8. RESOURCE IMPACT ANALYSIS")

# High demographic updates mean more workload for government offices
district_demo['workload_index'] = district_demo['total_demographic_updates'] / 1000  # Scale to workload units

high_workload = district_demo.nlargest(10, 'workload_index')
print("\n  ⚡ DISTRICTS NEEDING ADDITIONAL RESOURCES:")
print(high_workload[['workload_index', 'total_demographic_updates']])

# ===== 9. KEY INSIGHTS =====
print("\n9. KEY INSIGHTS")

insights = []
insights.append(f"• Total demographic updates: {df['total_demographic_updates'].sum():,}")
insights.append(f"• Highest migration district: {district_demo.index[0]} ({district_demo.iloc[0]['total_demographic_updates']:,} updates)")
insights.append(f"• {len(high_migration)} districts show high migration patterns (Score >50)")
insights.append(f"• Average updates per district: {df['total_demographic_updates'].sum() / df['district'].nunique():,.0f}")

# Seasonal patterns
if len(monthly_demo) > 0:
    peak_month = monthly_demo.idxmax()
    insights.append(f"• Peak migration month: {peak_month}")

for insight in insights:
    print(f"  {insight}")

# ===== 10. SAVE OUTPUTS =====
print("\n10. SAVING OUTPUTS")

df.to_csv('analysis_outputs/demographic_cleaned.csv', index=False)
print("  ✓ Saved: demographic_cleaned.csv")

district_demo.to_csv('analysis_outputs/demographic_district_summary.csv')
print("  ✓ Saved: demographic_district_summary.csv")

with open('analysis_outputs/demographic_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("DEMOGRAPHIC DATA ANALYSIS REPORT\n")
    f.write("Migration Patterns & Resource Impact Assessment\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET OVERVIEW:\n")
    f.write(f"  Records: {len(df):,}\n")
    f.write(f"  Districts: {df['district'].nunique()}\n")
    f.write(f"  Total Demographic Updates: {df['total_demographic_updates'].sum():,}\n\n")
    
    f.write("HIGH MIGRATION DISTRICTS (Top 10):\n")
    for idx, (district, row) in enumerate(district_demo.head(10).iterrows(), 1):
        f.write(f"  {idx}. {district}: {row['total_demographic_updates']:,} (Score: {row['migration_intensity_score']:.1f})\n")
    
    f.write("\nRESOURCE IMPACT:\n")
    for idx, (district, row) in enumerate(high_workload.head(5).iterrows(), 1):
        f.write(f"  {idx}. {district}: Workload Index {row['workload_index']:.1f}\n")
    
    f.write("\nKEY INSIGHTS:\n")
    for insight in insights:
        f.write(f"  {insight}\n")
    
    f.write("\n" + "="*80)

print("  ✓ Saved: demographic_analysis_report.txt")

print("\n" + "="*80)
print("✅ DEMOGRAPHIC ANALYSIS COMPLETE!")
print("="*80)
