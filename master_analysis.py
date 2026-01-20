"""
MASTER DATA ANALYSIS - GovOptima Platform
Generates comprehensive analysis outputs for all 3 datasets
Run this to generate all analysis files and insights
"""

from analysis import GovernanceAnalyst
import pandas as pd
import numpy as np
import json
import os

# Create output directory
os.makedirs('analysis_outputs', exist_ok=True)

print("\n" + "="*90)
print(" "*30 + "GOVOPTIMA PLATFORM")
print(" "*25 + "Master Data Analysis System")
print("="*90 + "\n")

# Initialize analyst
analyst = GovernanceAnalyst(os.getcwd())
analyst.load_data()
analyst.process_data()

df = analyst.combined_df

print(f"✅ LOADED & PROCESSED {len(df):,} RECORDS")
print(f"📊 Districts: {df['district'].nunique()}")
print(f"📅 Date Range: {df['date'].min()} to {df['date'].max()}\n")

# =====  COMPREHENSIVE ANALYSIS =====

print("="*90)
print("SECTION 1: ENROLLMENT ANALYSIS")
print("="*90)

enrollment_total = df['total_enrollment'].sum()
enrollment_by_age = {
    'Age 0-5': df['age_0_5'].sum(),
    'Age 5-17': df['age_5_17'].sum(),
    'Age 18+': df['age_18_greater'].sum()
}

print(f"\n📈 TOTAL ENROLLMENTS: {enrollment_total:,}")
for age, count in enrollment_by_age.items():
    pct = (count / enrollment_total * 100) if enrollment_total > 0 else 0
    print(f"  • {age}: {count:,} ({pct:.1f}%)")

# Top enrollment districts
enroll_districts = df.groupby('district')['total_enrollment'].sum().sort_values(ascending=False)
print(f"\n🏆 TOP 10 ENROLLMENT DISTRICTS:")
for idx, (district, val) in enumerate(enroll_districts.head(10).items(), 1):
    print(f"  {idx}. {district}: {val:,}")

# Save enrollment analysis
with open('analysis_outputs/01_enrollment_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("ENROLLMENT DATA ANALYSIS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Enrollments: {enrollment_total:,}\n\n")
    f.write("Age Distribution:\n")
    for age, count in enrollment_by_age.items():
        pct = (count / enrollment_total * 100) if enrollment_total > 0 else 0
        f.write(f"  {age}: {count:,} ({pct:.1f}%)\n")
    f.write("\nTop 15 Districts:\n")
    for idx, (district, val) in enumerate(enroll_districts.head(15).items(), 1):
        f.write(f"  {idx}. {district}: {val:,}\n")

print(f"\n✅ Saved: analysis_outputs/01_enrollment_analysis.txt\n")

# =====  BIOMETRIC ANALYSIS =====

print("="*90)
print("SECTION 2: BIOMETRIC UPDATE ANALYSIS")  
print("="*90)

biometric_total = df['total_biometric'].sum()
print(f"\n🔬 TOTAL BIOMETRIC UPDATES: {biometric_total:,}")

bio_districts = df.groupby('district')['total_biometric'].sum().sort_values(ascending=False)
print(f"\n🏆 TOP 10 BIOMETRIC UPDATE DISTRICTS:")
for idx, (district, val) in enumerate(bio_districts.head(10).items(), 1):
    print(f"  {idx}. {district}: {val:,}")

# Aging population indicators (high biometric updates)
bio_districts_normalized = (bio_districts / bio_districts.max() * 100).round(1)
high_aging = bio_districts_normalized[bio_districts_normalized > 70]
print(f"\n👴 AGING POPULATION INDICATORS ({len(high_aging)} districts):")
for district in high_aging.head(5).index:
    print(f"  • {district}: Score {bio_districts_normalized[district]}/100")

# Save biometric analysis
with open('analysis_outputs/02_biometric_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("BIOMETRIC UPDATE ANALYSIS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Biometric Updates: {biometric_total:,}\n\n")
    f.write("Top 15 Districts:\n")
    for idx, (district, val) in enumerate(bio_districts.head(15).items(), 1):
        f.write(f"  {idx}. {district}: {val:,}\n")
    f.write("\nAging Population Indicators:\n")
    for district in high_aging.head(10).index:
        f.write(f"  • {district}: Score {bio_districts_normalized[district]}/100\n")

print(f"\n✅ Saved: analysis_outputs/02_biometric_analysis.txt\n")

# ===== DEMOGRAPHIC & MIGRATION ANALYSIS =====

print("="*90)
print("SECTION 3: DEMOGRAPHIC UPDATE & MIGRATION ANALYSIS")
print("="*90)

demographic_total = df['total_demographic'].sum()
print(f"\n🌍 TOTAL DEMOGRAPHIC UPDATES: {demographic_total:,}")

# Migration intensity analysis
migration_scores = df.groupby('district')['migration_intensity'].mean().sort_values(ascending=False)
high_migration = migration_scores[migration_scores > 5]

print(f"\n🚨 HIGH MIGRATION DISTRICTS ({len(high_migration)} districts with score >5):")
for idx, (district, score) in enumerate(high_migration.head(10).items(), 1):
    updates = df[df['district'] == district]['total_demographic'].sum()
    print(f"  {idx}. {district}: Score {score:.2f}/10 ({updates:,} updates)")

# Save demographic analysis
with open('analysis_outputs/03_demographic_migration_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("DEMOGRAPHIC UPDATE & MIGRATION ANALYSIS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Demographic Updates: {demographic_total:,}\n\n")
    f.write(f"High Migration Districts (Score >5): {len(high_migration)}\n\n")
    for idx, (district, score) in enumerate(high_migration.head(15).items(), 1):
        updates = df[df['district'] == district]['total_demographic'].sum()
        f.write(f"  {idx}. {district}: Score {score:.2f}/10 ({updates:,} updates)\n")

print(f"\n✅ Saved: analysis_outputs/03_demographic_migration_analysis.txt\n")

# ===== RESOURCE ALLOCATION ANALYSIS =====

print("="*90)
print("SECTION 4: RESOURCE ALLOCATION & OPTIMIZATION")
print("="*90)

# Calculate resource needs by district
district_metrics = df.groupby('district').agg({
    'stress_index': 'mean',
    'migration_intensity': 'mean',
    'total_enrollment': 'sum',
    'total_biometric': 'sum',
    'total_demographic': 'sum'
}).round(2)

district_metrics['total_operations'] = (
    district_metrics['total_enrollment'] +
    district_metrics['total_biometric'] +
    district_metrics['total_demographic']
)

# Resource recommendations (1 kit per 50 daily operations)
district_metrics['recommended_kits'] = np.ceil(district_metrics['stress_index'] / 50).astype(int)
district_metrics['recommended_staff'] = np.ceil(district_metrics['total_operations'] / 10000).astype(int)

# Priority classification
district_metrics['priority'] = pd.cut(
    district_metrics['stress_index'],
    bins=[0, 100, 200, float('inf')],
    labels=['Low', 'Medium', 'High']
)

high_priority = district_metrics[district_metrics['priority'] == 'High'].sort_values('stress_index', ascending=False)

print(f"\n⚡ HIGH PRIORITY DISTRICTS ({len(high_priority)} districts):")
for idx, (district, row) in enumerate(high_priority.head(10).iterrows(), 1):
    print(f"  {idx}. {district}:")
    print(f"      Stress Index: {row['stress_index']:.1f}")
    print(f"      Recommended Kits: {row['recommended_kits']}")
    print(f"      Recommended Staff: {row['recommended_staff']}")

# Save resource analysis
district_metrics.to_csv('analysis_outputs/04_district_resource_recommendations.csv')
print(f"\n✅ Saved: analysis_outputs/04_district_resource_recommendations.csv")

with open('analysis_outputs/04_resource_allocation.txt', 'w', encoding='utf-8') as f:
    f.write("RESOURCE ALLOCATION & OPTIMIZATION ANALYSIS\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Districts Analyzed: {len(district_metrics)}\n")
    f.write(f"High Priority Districts: {len(high_priority)}\n\n")
    f.write("Top 15 High-Priority Districts:\n\n")
    for idx, (district, row) in enumerate(high_priority.head(15).iterrows(), 1):
        f.write(f"{idx}. {district}\n")
        f.write(f"   Stress Index: {row['stress_index']:.1f}\n")
        f.write(f"   Recommended Kits: {row['recommended_kits']}\n")
        f.write(f"   Recommended Staff: {row['recommended_staff']}\n")
        f.write(f"   Migration Score: {row['migration_intensity']:.2f}\n\n")

print(f"✅ Saved: analysis_outputs/04_resource_allocation.txt\n")

# ===== COST ANALYSIS =====

print("="*90)
print("SECTION 5: COST ANALYSIS & SAVINGS ESTIMATION")
print("="*90)

# Cost assumptions
COST_PER_ENROLLMENT = 150  # INR
COST_PER_BIOMETRIC = 75    # INR
COST_PER_DEMOGRAPHIC = 50  # INR
COST_PER_KIT = 500000      # INR (5 lakhs)
COST_PER_STAFF_ANNUAL = 600000  # INR (6 lakhs)

total_cost = (
    enrollment_total * COST_PER_ENROLLMENT +
    biometric_total * COST_PER_BIOMETRIC +
    demographic_total * COST_PER_DEMOGRAPHIC
)

kit_cost = district_metrics['recommended_kits'].sum() * COST_PER_KIT
staff_cost = district_metrics['recommended_staff'].sum() * COST_PER_STAFF_ANNUAL

# Optimization savings (10% efficiency gain)
potential_savings = total_cost * 0.10

print(f"\n💰 COST ANALYSIS:")
print(f"  • Total Operational Cost: ₹{total_cost:,.0f} ({total_cost/10_000_000:.1f} Crore)")
print(f"  • Infrastructure Cost (Kits): ₹{kit_cost:,.0f} ({kit_cost/10_000_000:.1f} Crore)")
print(f"  • Annual Staff Cost: ₹{staff_cost:,.0f} ({staff_cost/10_000_000:.1f} Crore)")
print(f"  • Potential Savings (10% efficiency): ₹{potential_savings:,.0f} ({potential_savings/10_000_000:.1f} Crore)")

cost_analysis = {
    "total_operational_cost_inr": total_cost,
    "total_operational_cost_crore": round(total_cost /10_000_000, 2),
    "kit_infrastructure_cost_inr": kit_cost,
    "staff_annual_cost_inr": staff_cost,
    "potential_savings_inr": potential_savings,
    "potential_savings_crore": round(potential_savings / 10_000_000, 2),
    "total_kits_recommended": int(district_metrics['recommended_kits'].sum()),
    "total_staff_recommended": int(district_metrics['recommended_staff'].sum())
}

with open('analysis_outputs/05_cost_analysis.json', 'w') as f:
    json.dump(cost_analysis, f, indent=2)

print(f"\n✅ Saved: analysis_outputs/05_cost_analysis.json\n")

# ===== MASTER INSIGHTS =====

print("="*90)
print("SECTION 6: KEY INSIGHTS & RECOMMENDATIONS")
print("="*90)

insights = {
    "summary": {
        "total_records": len(df),
        "districts_covered": df['district'].nunique(),
        "date_range": f"{df['date'].min()} to {df['date'].max()}",
        "total_enrollments": int(enrollment_total),
        "total_biometric_updates": int(biometric_total),
        "total_demographic_updates": int(demographic_total),
        "total_government_operations": int(enrollment_total + biometric_total + demographic_total)
    },
    "top_districts": {
        "highest_enrollment": enroll_districts.index[0],
        "highest_biometric": bio_districts.index[0],
        "highest_migration": migration_scores.index[0],
        "highest_stress": district_metrics.sort_values('stress_index', ascending=False).index[0]
    },
    "alerts": {
        "high_migration_districts": len(high_migration),
        "high_priority_districts": len(high_priority),
        "aging_population_districts": len(high_aging)
    },
    "recommendations": [
        f"Deploy {cost_analysis['total_kits_recommended']} additional enrollment kits",
        f"Hire {cost_analysis['total_staff_recommended']} additional staff members",
        f"Focus migration response on {len(high_migration)} high-movement districts",
        f"Priority resource allocation to {len(high_priority)} high-stress districts",
        f"Potential cost savings: ₹{potential_savings/10_000_000:.1f} Crore through optimization"
    ]
}

with open('analysis_outputs/06_master_insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("\n🎯 KEY INSIGHTS:")
print(f"  • Total Government Operations: {insights['summary']['total_government_operations']:,}")
print(f"  • High-Priority Districts: {insights['alerts']['high_priority_districts']}")
print(f"  • High-Migration Districts: {insights['alerts']['high_migration_districts']}")
print(f"  • Recommended Kits: {cost_analysis['total_kits_recommended']}")
print(f"  • Potential Savings: ₹{cost_analysis['potential_savings_crore']} Crore")

print(f"\n✅ Saved: analysis_outputs/06_master_insights.json\n")

# ===== FINAL SUMMARY =====

df.to_csv('analysis_outputs/00_combined_clean_data.csv', index=False)

print("="*90)
print("✅ ANALYSIS COMPLETE!")
print("="*90)

print("\n📁 GENERATED FILES:")
print("  1. 00_combined_clean_data.csv")
print("  2. 01_enrollment_analysis.txt")
print("  3. 02_biometric_analysis.txt")
print("  4. 03_demographic_migration_analysis.txt")
print("  5. 04_district_resource_recommendations.csv")
print("  6. 04_resource_allocation.txt")
print("  7. 05_cost_analysis.json")
print("  8. 06_master_insights.json")

print("\n🎉 All analysis outputs ready for dashboard integration!")
print("="*90 + "\n")
