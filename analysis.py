import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import os

class GovernanceAnalyst:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.biometric_df = None
        self.demographic_df = None
        self.enrollment_df = None
        self.combined_df = None
        
    def load_data(self):
        """Loads data from CSV files."""
        try:
            bio_path = os.path.join(self.data_dir, "Biometric_Data.csv")
            demo_path = os.path.join(self.data_dir, "Demographic_Data.csv")
            enroll_path = os.path.join(self.data_dir, "Enrollment_Data.csv")
            
            self.biometric_df = pd.read_csv(bio_path)
            self.demographic_df = pd.read_csv(demo_path)
            self.enrollment_df = pd.read_csv(enroll_path)
            
            # Normalize column names & Clean District Names (Deduplication)
            for df in [self.biometric_df, self.demographic_df, self.enrollment_df]:
                df.columns = [c.strip().lower() for c in df.columns]
                # Standardize district names: Title Case, Strip Whitespace, handle variations
                df['district'] = df['district'].astype(str).str.strip().str.title()
                # Fix specific known typos/variations if any (example logic)
                df['district'] = df['district'].replace({
                    'Mumbai( Sub Urban )': 'Mumbai Suburban',
                    'Ahmed Nagar': 'Ahmadnagar',
                    'Bid': 'Beed',
                    'Buldhana': 'Buldana' # Standardize spelling
                })
                
            # Date parsing
            for df in [self.biometric_df, self.demographic_df, self.enrollment_df]:
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
                
            # Fill missing numeric values with 0
            self.biometric_df.fillna(0, inplace=True)
            self.demographic_df.fillna(0, inplace=True)
            self.enrollment_df.fillna(0, inplace=True)
            
            return True
        except Exception as e:
            print(f"CRITICAL ERROR loading data: {e}")
            # Fallback: Create empty DFs so the app doesn't crash
            cols_bio = ['date', 'district', 'bio_age_5_17', 'bio_age_17_']
            cols_demo = ['date', 'district', 'demo_age_5_17', 'demo_age_17_']
            cols_enroll = ['date', 'district', 'age_0_5', 'age_5_17', 'age_18_greater']
            
            self.biometric_df = pd.DataFrame(columns=cols_bio)
            self.demographic_df = pd.DataFrame(columns=cols_demo)
            self.enrollment_df = pd.DataFrame(columns=cols_enroll)
            return False

    def process_data(self):
        """Aggregates data and calculates stress index."""
        if self.biometric_df is None:
            if not self.load_data():
                 print("Using empty dataframes due to load failure.")
        
        # Ensure we have dataframes even if they are empty
        if self.biometric_df is None: self.biometric_df = pd.DataFrame()
        if self.demographic_df is None: self.demographic_df = pd.DataFrame()
        if self.enrollment_df is None: self.enrollment_df = pd.DataFrame()

        # Handle Empty Data Case Gracefully
        if self.biometric_df.empty:
            self.combined_df = pd.DataFrame(columns=['date', 'district', 'stress_index', 'migration_intensity', 
                                                     'total_enrollment', 'total_biometric', 'total_demographic',
                                                     'age_0_5', 'age_5_17', 'age_18_greater',
                                                     'ivi', 'bsr', 'api'])
            return self.combined_df

        # Group by Date and District (Ensuring no duplicates for same day/district)
        bio_grouped = self.biometric_df.groupby(['date', 'district']).sum(numeric_only=True).reset_index()
        demo_grouped = self.demographic_df.groupby(['date', 'district']).sum(numeric_only=True).reset_index()
        enroll_grouped = self.enrollment_df.groupby(['date', 'district']).sum(numeric_only=True).reset_index()
        
        # Merge dataframes
        merged = pd.merge(enroll_grouped, bio_grouped, on=['date', 'district'], how='outer', suffixes=('_enroll', '_bio'))
        merged = pd.merge(merged, demo_grouped, on=['date', 'district'], how='outer', suffixes=('', '_demo'))
        
        merged.fillna(0, inplace=True)
        
        # Calculate Totals
        merged['total_enrollment'] = merged['age_0_5'] + merged['age_5_17'] + merged['age_18_greater']
        
        bio_cols = [c for c in merged.columns if c.startswith('bio_')]
        merged['total_biometric'] = merged[bio_cols].sum(axis=1)
        
        demo_cols = [c for c in merged.columns if c.startswith('demo_')]
        merged['total_demographic'] = merged[demo_cols].sum(axis=1)
        
        # --- Advanced Metrics & Indices (Normalized) ---
        
        # Calculate Total Activity (Transactions)
        merged['total_activity'] = merged['total_enrollment'] + merged['total_biometric'] + merged['total_demographic']
        
        # Avoid division by zero
        merged['total_activity'] = merged['total_activity'].replace(0, 1)

        # 1. Identity Volatility Index (IVI)
        # Represents the % of system activity that is "Churn" (Updates) vs "Growth" (Enrollment).
        # Formula: ((Biometric + Demographic) / Total Activity) * 100
        # Range: 0 to 100. High IVI means the system is in "Maintenance Mode" rather than "Growth Mode".
        merged['ivi'] = ((merged['total_demographic'] + merged['total_biometric']) / merged['total_activity']) * 100

        # 2. Biometric Stress Ratio (BSR)
        # Represents the share of biometric updates in total operations.
        # Formula: (Biometric / Total Activity) * 100
        # High BSR (>30%) indicates aging population updates or potential sensor/auth failures causing re-updates.
        merged['bsr'] = (merged['total_biometric'] / merged['total_activity']) * 100

        # 3. Aadhaar Pressure Index (API)
        # Composite Operational Load (Work Units).
        # Weighted based on resource intensity: Enrollment (High effort), Bio (Med), Demo (Low).
        # Formula: (Enrollment * 1.0) + (Biometric * 0.5) + (Demographic * 0.2)
        # This is an absolute number representing "Work Load".
        merged['api'] = (
            (merged['total_enrollment'] * 1.0) + 
            (merged['total_biometric'] * 0.5) + 
            (merged['total_demographic'] * 0.2)
        )
        
        # 4. Migration Intensity Score
        # Proxy: High demographic updates usually imply address/details changes (Migration).
        # Formula: (Demographic Updates / Total Activity) * 10
        # Range: 0 to 10.
        # 10/10 means 100% of the district's activity is demographic updates (High Migration/Correction).
        merged['migration_intensity'] = (merged['total_demographic'] / merged['total_activity']) * 10
        
        # Legacy support
        merged['stress_index'] = merged['api']
        
        # Replace Infinity or NaN with 0 for clean JSON serialization
        merged.replace([np.inf, -np.inf], 0, inplace=True)
        merged.fillna(0, inplace=True)
        
        self.combined_df = merged
        return self.combined_df

    def get_district_stats(self, district: str = None):
        """Returns aggregated stats."""
        df = self.combined_df
        if district:
            df = df[df['district'].str.lower() == district.lower()]
            
        if df.empty:
            return {
                "total_enrollment": 0, "total_biometric": 0, "total_demographic": 0,
                "avg_stress_index": 0.0, "avg_migration_score": 0.0
            }
            
        stats = {
            "total_enrollment": int(df['total_enrollment'].sum()),
            "total_biometric": int(df['total_biometric'].sum()),
            "total_demographic": int(df['total_demographic'].sum()),
            "avg_stress_index": float(df['stress_index'].mean()),
            "avg_migration_score": float(df['migration_intensity'].mean())
        }
        return stats

    def get_stress_heatmap(self):
        """Returns aggregated stress index by district."""
        # Aggregating over the entire period to get a stable "Hotspot" view
        agg_df = self.combined_df.groupby('district')[['stress_index', 'migration_intensity']].mean().reset_index()
        return agg_df.to_dict(orient='records')

    def get_district_deep_dive(self, district: str):
        """Detailed breakdown for a specific district."""
        df = self.combined_df[self.combined_df['district'].str.lower() == district.lower()].sort_values('date')
        
        if df.empty:
            return {
                "age_demographics": {"0-5":0, "5-17":0, "18+":0},
                "kits_recommended": 0,
                "status": "No Data",
                "migration_flag": "Unknown"
            }
            
        # Age-wise totals (sum over time)
        age_stats = {
            "0-5": int(df['age_0_5'].sum()),
            "5-17": int(df['age_5_17'].sum()),
            "18+": int(df['age_18_greater'].sum())
        }
        
        # Resource Recommendation Logic
        avg_daily_ops = df['stress_index'].mean()
        # Assume 1 kit can handle 50 ops/day
        kits_needed = int(np.ceil(avg_daily_ops / 50))
        # Anomaly status
        is_high_load = avg_daily_ops > 200 # Threshold
        
        return {
            "age_demographics": age_stats,
            "kits_recommended": kits_needed,
            "status": "Critical" if is_high_load else "Normal",
            "migration_flag": "High In-Migration" if df['migration_intensity'].mean() > 5 else "Stable"
        }

    def get_forecast(self, district: str, months: int = 3):
        """Linear forecast."""
        df = self.combined_df[self.combined_df['district'].str.lower() == district.lower()].sort_values('date')
        if len(df) < 2:
            return []
            
        last_val = df['stress_index'].mean() # Using mean for stability
        trend = 1.05 # Assume 5% growth
        
        forecast = []
        for i in range(months):
            val = last_val * (trend ** (i+1))
            forecast.append({
                "month": f"M+{i+1}",
                "predicted_stress": float(val),
                "required_kits": int(np.ceil(val / 50))
            })
        return forecast
