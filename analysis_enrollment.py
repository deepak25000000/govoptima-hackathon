"""
ENROLLMENT DATA ANALYSIS
Comprehensive analysis of Enrollment_Data.csv for GovOptima Platform
Author: Senior Data Analyst
Date: January 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# Create output directory
os.makedirs('analysis_outputs', exist_ok=True)

print("="*80)
print("📊 ENROLLMENT DATA ANALYSIS")
print("="*80)

# ===== 1. DATA LOADING =====
print("\n1. LOADING DATA...")
df = pd.read_csv('Enrollment_Data.csv')
print(f"✓ Loaded {len(df):,} records")

# ===== 2. DATA EXPLORATION =====
print("\n2. DATA EXPLORATION")
print(f"  Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Columns: {list(df.columns)}")
print(f"\n  Column Data Types:\n{df.dtypes}")
print(f"\n  First 10 Records:\n{df.head(10)}")

# ===== 3. DATA QUALITY ASSESSMENT =====
print("\n3. DATA QUALITY ASSESSMENT")
null_counts = df.isnull().sum()
print(f"  Missing Values:\n{null_counts}")
print(f"  Total Missing: {null_counts.sum()}")
print(f"  Duplicate Rows: {df.duplicated().sum()}")

# ===== 4. DATA CLEANING =====
print("\n4. DATA CLEANING")

# Normalize column names
df.columns = [c.strip().lower() for c in df.columns]
print(f"  ✓ Normalized column names: {list(df.columns)}")

# Parse dates
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
print(f"  ✓ Parsed dates")

# Standardize district names
df['district'] = df['district'].astype(str).str.strip().str.title()
df['district'] = df['district'].replace({
    'Mumbai( Sub Urban )': 'Mumbai Suburban',
    'Ahmed Nagar': 'Ahmadnagar',
    'Bid': 'Beed',
    'Buldhana': 'Buldana'
})
print(f"  ✓ Standardized {df['district'].nunique()} district names")

# Fill missing values
df.fillna(0, inplace=True)
print(f"  ✓ Filled missing values with 0")

# ===== 5. STATISTICAL ANALYSIS =====
print("\n5. STATISTICAL ANALYSIS")

# Age group analysis
df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
age_stats = {
    'Age 0-5': df['age_0_5'].sum(),
    'Age 5-17': df['age_5_17'].sum(),
    'Age 18+': df['age_18_greater'].sum(),
    'Total': df['total_enrollments'].sum()
}

print("\n  📈 ENROLLMENT STATISTICS:")
for key, val in age_stats.items():
    pct = (val / age_stats['Total'] * 100) if age_stats['Total'] > 0 else 0
    print(f"    • {key}: {val:,} ({pct:.1f}%)")

print(f"\n  📅 TIME PERIOD:")
print(f"    • Start Date: {df['date'].min()}")
print(f"    • End Date: {df['date'].max()}")
print(f"    • Duration: {(df['date'].max() - df['date'].min()).days} days")

print(f"\n  🏛️ GEOGRAPHIC COVERAGE:")
print(f"    • Total Districts: {df['district'].nunique()}")
print(f"    • Total Records: {len(df):,}")

# ===== 6. DISTRICT-WISE ANALYSIS =====
print("\n6. DISTRICT-WISE ANALYSIS")

district_summary = df.groupby('district').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'total_enrollments': 'sum'
}).sort_values('total_enrollments', ascending=False)

print("\n  🏆 TOP 15 DISTRICTS BY ENROLLMENT:")
print(district_summary.head(15))

print("\n  📉 BOTTOM 10 DISTRICTS BY ENROLLMENT:")
print(district_summary.tail(10))

# ===== 7. TEMPORAL ANALYSIS =====
print("\n7. TEMPORAL ANALYSIS")

monthly_enrollments = df.groupby(df['date'].dt.to_period('M'))['total_enrollments'].sum()
print(f"\n  📆 MONTHLY ENROLLMENT TRENDS:")
print(monthly_enrollments.head(12))

# ===== 8. KEY INSIGHTS =====
print("\n8. KEY INSIGHTS")

insights = []

# Insight 1: Dominant age group
dominant_age = max(age_stats, key=lambda k: age_stats[k] if k != 'Total' else 0)
insights.append(f"• {dominant_age} group has highest enrollments ({age_stats[dominant_age]:,})")

# Insight 2: Top district
top_district = district_summary.index[0]
insights.append(f"• {top_district} leads with {district_summary.iloc[0]['total_enrollments']:,} enrollments")

# Insight 3: Average per district
avg_per_district = df['total_enrollments'].sum() / df['district'].nunique()
insights.append(f"• Average enrollments per district: {avg_per_district:,.0f}")

# Insight 4: Growth trend
if len(monthly_enrollments) > 1:
    growth_rate = ((monthly_enrollments.iloc[-1] - monthly_enrollments.iloc[0]) / monthly_enrollments.iloc[0]) * 100
    insights.append(f"• Overall growth rate: {growth_rate:+.1f}%")

for insight in insights:
    print(f"  {insight}")

# ===== 9. SAVE OUTPUTS =====
print("\n9. SAVING OUTPUTS")

# Save cleaned data
df.to_csv('analysis_outputs/enrollment_cleaned.csv', index=False)
print("  ✓ Saved: enrollment_cleaned.csv")

# Save district summary
district_summary.to_csv('analysis_outputs/enrollment_district_summary.csv')
print("  ✓ Saved: enrollment_district_summary.csv")

# Save analysis report
with open('analysis_outputs/enrollment_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("ENROLLMENT DATA ANALYSIS REPORT\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET OVERVIEW:\n")
    f.write(f"  Records: {len(df):,}\n")
    f.write(f"  Districts: {df['district'].nunique()}\n")
    f.write(f"  Date Range: {df['date'].min()} to {df['date'].max()}\n\n")
    
    f.write("ENROLLMENT STATISTICS:\n")
    for key, val in age_stats.items():
        pct = (val / age_stats['Total'] * 100) if age_stats['Total'] > 0 else 0
        f.write(f"  {key}: {val:,} ({pct:.1f}%)\n")
    
    f.write("\nTOP 10 DISTRICTS:\n")
    for idx, (district, row) in enumerate(district_summary.head(10).iterrows(), 1):
        f.write(f"  {idx}. {district}: {row['total_enrollments']:,}\n")
    
    f.write("\nKEY INSIGHTS:\n")
    for insight in insights:
        f.write(f"  {insight}\n")
    
    f.write("\n" + "="*80)

print("  ✓ Saved: enrollment_analysis_report.txt")

print("\n" + "="*80)
print("✅ ENROLLMENT ANALYSIS COMPLETE!")
print("="*80)
