from fastapi import FastAPI, Query, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from analysis import GovernanceAnalyst
import os
import json
import sys
import sqlite3
import subprocess

# Force UTF-8 for Windows Console to prevent crashes
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

app = FastAPI(title="Governance Stress Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_path = os.getcwd() # Use current working directory
analyst = GovernanceAnalyst(data_path)
analyst.load_data()
analyst.process_data()

# Initialize vulnerable SQLite database for comments
def init_db():
    conn = sqlite3.connect('vulnerable_comments.db')
    c = conn.cursor()
    # Vulnerable: No input sanitization
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  comment TEXT, 
                  district TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT,
                  role TEXT)''')
    # Add some default users
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        c.execute("INSERT INTO users (username, password, role) VALUES ('analyst', 'pass123', 'user')")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # Explicitly use utf-8 to handle emojis/special chars on Windows
        with open(os.path.join(data_path, "templates", "index.html"), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading dashboard: {e}</h1>"

@app.get("/api/districts")
def get_districts():
    districts = analyst.combined_df['district'].unique().tolist()
    return {"districts": sorted(districts)}

@app.get("/api/stats")
def get_stats(district: str = Query(None)):
    try:
        stats = analyst.get_district_stats(district)
        return stats
    except Exception as e:
        print(f"Error in /api/stats: {e}")
        return {"error": str(e), "total_enrollment": 0, "avg_stress_index": 0}

@app.get("/api/stress_heatmap")
def get_heatmap():
    try:
        return analyst.get_stress_heatmap()
    except Exception as e:
        print(f"Error in /api/stress_heatmap: {e}")
        return []

@app.get("/api/deep_dive")
def get_deep_dive(district: str):
    try:
        return analyst.get_district_deep_dive(district)
    except Exception as e:
        print(f"Error in /api/deep_dive: {e}")
        return {"status": "Error", "message": str(e)}

@app.get("/api/forecast")
def get_forecast(district: str):
    try:
        return analyst.get_forecast(district)
    except Exception as e:
        print(f"Error in /api/forecast: {e}")
        return []

@app.get("/api/trends")
def get_trends(district: str = Query(None)):
    try:
        df = analyst.combined_df
        if df is None or df.empty:
            return []
            
        if district:
            df = df[df['district'].str.lower() == district.lower()]
        
        # Aggregate by date
        trend_df = df.groupby('date')[['total_enrollment', 'stress_index', 'migration_intensity']].mean().reset_index()
        return trend_df.to_dict(orient='records')
    except Exception as e:
        print(f"Error in /api/trends: {e}")
        return []

# === GOVOPTIMA ANALYTICS ENDPOINTS ===

@app.get("/api/resource_recommendations")
def get_resource_recommendations():
    """Get resource allocation recommendations for districts"""
    try:
        df = analyst.combined_df
        
        district_metrics = df.groupby('district').agg({
            'stress_index': 'mean',
            'migration_intensity': 'mean',
            'total_enrollment': 'sum',
            'total_biometric': 'sum',
            'total_demographic': 'sum'
        }).round(2)
        
        district_metrics['recommended_kits'] = (district_metrics['stress_index'] / 50).apply(lambda x: int(max(1, x)))
        district_metrics['recommended_staff'] = ((district_metrics['total_enrollment'] + 
                                                   district_metrics['total_biometric'] +
                                                   district_metrics['total_demographic']) / 10000).apply(lambda x: int(max(1, x)))
        
        # Priority classification
        district_metrics['priority'] = district_metrics['stress_index'].apply(
            lambda x: 'High' if x > 200 else ('Medium' if x > 100 else 'Low')
        )
        
        results = district_metrics.sort_values('stress_index', ascending=False).head(20).to_dict(orient='index')
        
        return {
            "recommendations": results,
            "total_kits_needed": int(district_metrics['recommended_kits'].sum()),
            "total_staff_needed": int(district_metrics['recommended_staff'].sum())
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/migration_alerts")
def get_migration_alerts():
    """Get high-migration district alerts with detailed classification"""
    try:
        df = analyst.combined_df
        
        migration_scores = df.groupby('district').agg({
            'migration_intensity': 'mean',
            'total_demographic': 'sum'
        }).round(2)
        
        # Classify all districts
        migration_scores['alert_level'] = migration_scores['migration_intensity'].apply(
            lambda x: 'Very High' if x > 7 else (
                'High' if x > 5 else (
                    'Normal' if x > 3 else (
                        'Low' if x > 1 else 'Very Low'
                    )
                )
            )
        )
        
        # Sort by migration intensity
        migration_scores = migration_scores.sort_values('migration_intensity', ascending=False)
        
        # Categorize counts
        alert_counts = {
            'very_high': int((migration_scores['migration_intensity'] > 7).sum()),
            'high': int(((migration_scores['migration_intensity'] > 5) & (migration_scores['migration_intensity'] <= 7)).sum()),
            'normal': int(((migration_scores['migration_intensity'] > 3) & (migration_scores['migration_intensity'] <= 5)).sum()),
            'low': int(((migration_scores['migration_intensity'] > 1) & (migration_scores['migration_intensity'] <= 3)).sum()),
            'very_low': int((migration_scores['migration_intensity'] <= 1).sum())
        }
        
        # Build alerts list
        alerts = []
        for district, row in migration_scores.iterrows():
            alerts.append({
                "district": district,
                "migration_score": float(row['migration_intensity']),
                "total_updates": int(row['total_demographic']),
                "alert_level": row['alert_level']
            })
        
        return {
            "alerts": alerts[:20],  # Top 20 for display
            "total_high_migration_districts": alert_counts['very_high'] + alert_counts['high'],
            "alert_breakdown": alert_counts,
            "all_alerts": alerts  # Full list
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/cost_analysis")
def get_cost_analysis():
    """Get detailed cost analysis with accurate rupee calculations"""
    try:
        df = analyst.combined_df
        
        # Accurate cost assumptions (in INR)
        COST_PER_ENROLLMENT = 150  # Per enrollment processing
        COST_PER_BIOMETRIC = 75    # Per biometric update
        COST_PER_DEMOGRAPHIC = 50  # Per demographic update
        COST_PER_KIT = 500000      # 5 lakhs per enrollment kit
        COST_PER_STAFF_ANNUAL = 600000  # 6 lakhs per staff member annually
        
        # Calculate totals
        total_enrollments = int(df['total_enrollment'].sum())
        total_biometric = int(df['total_biometric'].sum())
        total_demographic = int(df['total_demographic'].sum())
        
        # Operational costs
        operational_cost = (
            total_enrollments * COST_PER_ENROLLMENT +
            total_biometric * COST_PER_BIOMETRIC +
            total_demographic * COST_PER_DEMOGRAPHIC
        )
        
        # Resource requirements
        district_metrics = df.groupby('district').agg({'stress_index': 'mean'})
        total_kits = int((district_metrics['stress_index'] / 50).apply(lambda x: max(1, x)).sum())
        total_staff = int(((total_enrollments + total_biometric + total_demographic) / 10000))
        
        # Infrastructure costs
        kit_cost = total_kits * COST_PER_KIT
        staff_cost = total_staff * COST_PER_STAFF_ANNUAL
        total_infrastructure = kit_cost + staff_cost
        
        # Optimization savings (10% efficiency gain through better resource allocation)
        potential_savings = operational_cost * 0.10
        
        # ROI calculation
        roi_percentage = round((potential_savings / total_infrastructure) * 100, 1) if total_infrastructure > 0 else 0
        
        return {
            # Operational costs
            "operational_cost_inr": int(operational_cost),
            "operational_cost_crore": round(operational_cost / 10_000_000, 2),
            "operational_cost_formatted": f"₹{operational_cost:,.0f}",
            
            # Infrastructure costs
            "kit_investment_inr": int(kit_cost),
            "kit_investment_crore": round(kit_cost / 10_000_000, 2),
            "kit_investment_formatted": f"₹{kit_cost:,.0f}",
            
            "staff_cost_annual_inr": int(staff_cost),
            "staff_cost_crore": round(staff_cost / 10_000_000, 2),
            "staff_cost_formatted": f"₹{staff_cost:,.0f}",
            
            "total_infrastructure_inr": int(total_infrastructure),
            "total_infrastructure_crore": round(total_infrastructure / 10_000_000, 2),
            "total_infrastructure_formatted": f"₹{total_infrastructure:,.0f}",
            
            # Savings
            "potential_savings_inr": int(potential_savings),
            "potential_savings_crore": round(potential_savings / 10_000_000, 2),
            "potential_savings_formatted": f"₹{potential_savings:,.0f}",
            
            # ROI
            "roi_percentage": roi_percentage,
            
            # Resource counts
            "total_kits_needed": total_kits,
            "total_staff_needed": total_staff,
            
            # Transaction counts
            "total_enrollments": total_enrollments,
            "total_biometric_updates": total_biometric,
            "total_demographic_updates": total_demographic
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/efficiency_metrics")
def get_efficiency_metrics():
    """Get efficiency and performance metrics with district breakdown"""
    try:
        df = analyst.combined_df
        
        total_operations = df['total_enrollment'].sum() + df['total_biometric'].sum() + df['total_demographic'].sum()
        
        # District-level metrics
        district_performance = df.groupby('district').agg({
            'total_enrollment': 'sum',
            'total_biometric': 'sum',
            'total_demographic': 'sum',
            'stress_index': 'mean',
            'migration_intensity': 'mean'
        }).round(2)
        
        district_performance['total_ops'] = (district_performance['total_enrollment'] + 
                                             district_performance['total_biometric'] + 
                                             district_performance['total_demographic'])
        
        # Overall metrics
        metrics = {
            "total_operations": int(total_operations), 
            "total_districts": int(df['district'].nunique()),
            "avg_operations_per_district": int(total_operations / df['district'].nunique()),
            "avg_stress_index": round(df['stress_index'].mean(), 2),
            "avg_migration_score": round(df['migration_intensity'].mean(), 2),
            "high_stress_districts": int((district_performance['stress_index'] > 200).sum()),
            "high_migration_districts": int((district_performance['migration_intensity'] > 5).sum()),
            "district_breakdown": district_performance.sort_values('total_ops', ascending=False).head(10).to_dict(orient='index')
        }
        
        return metrics
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/export_report")
def export_report():
    """Generate comprehensive analytics report as CSV"""
    try:
        df = analyst.combined_df
        
        # Create summary report
        district_summary = df.groupby('district').agg({
            'total_enrollment': 'sum',
            'total_biometric': 'sum',
            'total_demographic': 'sum',
            'stress_index': 'mean',
            'migration_intensity': 'mean'
        }).round(2)
        
        district_summary['total_operations'] = (district_summary['total_enrollment'] + 
                                                 district_summary['total_biometric'] + 
                                                 district_summary['total_demographic'])
        
        # Calculate resource needs
        district_summary['recommended_kits'] = (district_summary['stress_index'] / 50).apply(lambda x: int(max(1, x)))
        district_summary['recommended_staff'] = (district_summary['total_operations'] / 10000).apply(lambda x: int(max(1, x)))
        
        # Priority classification
        district_summary['priority'] = district_summary['stress_index'].apply(
            lambda x: 'High' if x > 200 else ('Medium' if x > 100 else 'Low')
        )
        
        # Migration classification
        district_summary['migration_level'] = district_summary['migration_intensity'].apply(
            lambda x: 'Very High' if x > 7 else ('High' if x > 5 else ('Normal' if x > 3 else 'Low'))
        )
        
        # Save to CSV
        import io
        output = io.StringIO()
        district_summary.to_csv(output)
        csv_data = output.getvalue()
        
        return JSONResponse(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=govoptima_analytics_report.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable for Cloud Deployment (Render/Heroku), default to 8000 for local
    port = int(os.environ.get("PORT", 8000))
    
    # Disable colors to prevents Windows encoding errors
    uvicorn.run(app, host="0.0.0.0", port=port, use_colors=False)
