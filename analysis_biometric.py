"""
BIOMETRIC DATA ANALYSIS
Comprehensive analysis of Biometric_Data.csv for GovOptima Platform
Author: Senior Data Analyst  
Date: January 2026
"""

import pandas as pd
import numpy as np
import os

os.makedirs('analysis_outputs', exist_ok=True)

print("="*80)
print("🔬 BIOMETRIC DATA ANALYSIS")
print("="*80)

# ===== 1. DATA LOADING =====
print("\n1. LOADING DATA...")
df = pd.read_csv('Biometric_Data.csv')
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

# ===== 4. BIOMETRIC METRICS ANALYSIS =====
print("\n4. BIOMETRIC METRICS ANALYSIS")

bio_cols = [c for c in df.columns if c.startswith('bio_')]
df['total_biometric_updates'] = df[bio_cols].sum(axis=1)

print(f"\n  📊 BIOMETRIC UPDATE STATISTICS:")
for col in bio_cols:
    total = df[col].sum()
    print(f"    • {col}: {total:,}")

print(f"    • TOTAL UPDATES: {df['total_biometric_updates'].sum():,}")

# ===== 5. DISTRICT ANALYSIS =====
print("\n5. DISTRICT-WISE BIOMETRIC ANALYSIS")

district_bio = df.groupby('district')[bio_cols + ['total_biometric_updates']].sum()
district_bio = district_bio.sort_values('total_biometric_updates', ascending=False)

print("\n  🏆 TOP 15 DISTRICTS BY BIOMETRIC UPDATES:")
print(district_bio.head(15))

# ===== 6. AGING POPULATION ANALYSIS =====
print("\n6. AGING POPULATION INDICATORS")

# High biometric updates may indicate aging population (fingerprint degradation)
district_bio['aging_score'] = district_bio['total_biometric_updates'] / district_bio['total_biometric_updates'].max() * 100

high_aging = district_bio.nlargest(10, 'aging_score')
print("\n  👴 DISTRICTS WITH HIGHEST AGING INDICATORS:")
print(high_aging[['aging_score', 'total_biometric_updates']])

# ===== 7. TEMPORAL PATTERNS =====
print("\n7. TEMPORAL PATTERNS")

monthly_bio = df.groupby(df['date'].dt.to_period('M'))['total_biometric_updates'].sum()
print(f"\n  📅 MONTHLY BIOMETRIC UPDATE TRENDS:")
print(monthly_bio.head(12))

# ===== 8. KEY INSIGHTS =====
print("\n8. KEY INSIGHTS")

insights = []
insights.append(f"• Total biometric updates across all districts: {df['total_biometric_updates'].sum():,}")
insights.append(f"• Top district for biometric updates: {district_bio.index[0]} ({district_bio.iloc[0]['total_biometric_updates']:,})")
insights.append(f"• Average updates per district: {df['total_biometric_updates'].sum() / df['district'].nunique():,.0f}")

# Identify peak months
if len(monthly_bio) > 0:
    peak_month = monthly_bio.idxmax()
    insights.append(f"• Peak update month: {peak_month} ({monthly_bio.max():,} updates)")

for insight in insights:
    print(f"  {insight}")

# ===== 9. SAVE OUTPUTS =====
print("\n9. SAVING OUTPUTS")

df.to_csv('analysis_outputs/biometric_cleaned.csv', index=False)
print("  ✓ Saved: biometric_cleaned.csv")

district_bio.to_csv('analysis_outputs/biometric_district_summary.csv')
print("  ✓ Saved: biometric_district_summary.csv")

with open('analysis_outputs/biometric_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("BIOMETRIC DATA ANALYSIS REPORT\n")
    f.write("="*80 + "\n\n")
    
    f.write("DATASET OVERVIEW:\n")
    f.write(f"  Records: {len(df):,}\n")
    f.write(f"  Districts: {df['district'].nunique()}\n")
    f.write(f"  Total Biometric Updates: {df['total_biometric_updates'].sum():,}\n\n")
    
    f.write("TOP 10 DISTRICTS:\n")
    for idx, (district, row) in enumerate(district_bio.head(10).iterrows(), 1):
        f.write(f"  {idx}. {district}: {row['total_biometric_updates']:,}\n")
    
    f.write("\nAGING POPULATION INDICATORS:\n")
    for idx, (district, row) in enumerate(high_aging.head(5).iterrows(), 1):
        f.write(f"  {idx}. {district}: Score {row['aging_score']:.1f}/100\n")
    
    f.write("\nKEY INSIGHTS:\n")
    for insight in insights:
        f.write(f"  {insight}\n")
    
    f.write("\n" + "="*80)

print("  ✓ Saved: biometric_analysis_report.txt")

print("\n" + "="*80)
print("✅ BIOMETRIC ANALYSIS COMPLETE!")
print("="*80)
