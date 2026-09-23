"""
Global Demurrage & Detention Control Center: Synthetic Data Engine
Author: Senior SCM & Logistics Data Architecture Portfolio
Scale: 1,500 Heavy-Haul Rake Operations (Last 12 Months)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set deterministic seed for reproducibility
np.random.seed(42)
TOTAL_ROWS = 1500
END_DATE = datetime(2026, 9, 1, 0, 0, 0)
START_DATE = END_DATE - timedelta(days=365)

# ---------------------------------------------------------
# 1. Master Configuration & Reference Data
# ---------------------------------------------------------
PORTS = ["Port A", "Port B", "Port C", "Port D"]

PORT_METRICS = {
    "Port A": {"Hourly_Penalty_Rate_INR": 18000, "Grace_Period_Hours": 2.0},
    "Port B": {"Hourly_Penalty_Rate_INR": 15000, "Grace_Period_Hours": 2.0},
    "Port C": {"Hourly_Penalty_Rate_INR": 16500, "Grace_Period_Hours": 1.5},
    "Port D": {"Hourly_Penalty_Rate_INR": 14000, "Grace_Period_Hours": 2.5},
}

SECTOR_MAPPING = {
    "Steel": {
        "Destinations": ["Plant A1", "Plant A2", "Plant A3"],
        "Commodities": ["Iron Ore", "Coal", "Limestone"],
    },
    "Power": {
        "Destinations": ["Plant B1", "Plant B2", "Plant B3"],
        "Commodities": ["Coal"],
    },
    "Mining": {
        "Destinations": ["Plant C1", "Plant C2", "Plant C3"],
        "Commodities": ["Bauxite", "Iron Ore"],
    },
}

DELAY_CAUSES = [
    "Yard Congestion",
    "Equipment Breakdown",
    "Railway Traffic",
    "Weather Disruption",
    "Shift Handover Delay",
    "None (Nominal Operations)",
]

# ---------------------------------------------------------
# 2. Table B: Demurrage_Cost_Rules (Lookup Table)
# ---------------------------------------------------------
demurrage_rules_df = pd.DataFrame([
    {
        "Port_Origin": port,
        "Hourly_Penalty_Rate_INR": data["Hourly_Penalty_Rate_INR"],
        "Grace_Period_Hours": data["Grace_Period_Hours"],
    }
    for port, data in PORT_METRICS.items()
])
# ---------------------------------------------------------
# 3. Table A & C: Master_Rake_Log & Operational_Bottlenecks_Log
# ---------------------------------------------------------
rake_ids = [f"RAKE-{20250000 + i}" for i in range(1, TOTAL_ROWS + 1)]
sectors = np.random.choice(["Steel", "Power", "Mining"], size=TOTAL_ROWS, p=[0.45, 0.35, 0.20])
ports = np.random.choice(PORTS, size=TOTAL_ROWS, p=[0.30, 0.25, 0.25, 0.20])

rake_master_records = []
bottleneck_records = []

# Enforce realistic delay dynamics: ~32% target breach rate (> 25% requirement)
is_breached = np.random.binomial(1, 0.32, size=TOTAL_ROWS)

for i in range(TOTAL_ROWS):
    r_id = rake_ids[i]
    sec = sectors[i]
    port = ports[i]

# Destination & Commodity logic
    dest = np.random.choice(SECTOR_MAPPING[sec]["Destinations"])
    commodity = np.random.choice(SECTOR_MAPPING[sec]["Commodities"])
    wagons = int(np.random.randint(45, 60))  # 45 to 59 wagons (standard BOXN/BOBRN rakes)

# Free Time Logic
    free_time = 10.0 if commodity in ["Coal", "Iron Ore"] else 15.0
    grace_time = PORT_METRICS[port]["Grace_Period_Hours"]

# Operational Delay Modeling
    breach = is_breached[i]
    if breach == 1:
        # High impact causes correlated with severe delays
        cause = np.random.choice(
            ["Yard Congestion", "Equipment Breakdown", "Railway Traffic", "Weather Disruption"],
            p=[0.40, 0.30, 0.20, 0.10]
        )
        if cause == "Yard Congestion":
            turnaround_hours = free_time + grace_time + np.random.uniform(3.0, 18.0)
            eff_score = np.round(np.random.uniform(0.10, 0.45), 2)
        elif cause == "Equipment Breakdown":
            turnaround_hours = free_time + grace_time + np.random.uniform(2.0, 12.0)
            eff_score = np.round(np.random.uniform(0.20, 0.50), 2)
        elif cause == "Railway Traffic":
            turnaround_hours = free_time + grace_time + np.random.uniform(1.0, 8.0)
            eff_score = np.round(np.random.uniform(0.35, 0.65), 2)
        else:  # Weather
            turnaround_hours = free_time + grace_time + np.random.uniform(4.0, 24.0)
            eff_score = np.round(np.random.uniform(0.10, 0.30), 2)
    else:
        # Compliant / nominal loading operations
        cause = np.random.choice(["None (Nominal Operations)", "Shift Handover Delay"], p=[0.85, 0.15])
        turnaround_hours = np.random.uniform(5.5, free_time - 0.5)
        eff_score = np.round(np.random.uniform(0.70, 0.98), 2)
        
    turnaround_hours = round(float(turnaround_hours), 2)
    
    # Timestamp Sequencing
    random_days_offset = np.random.uniform(0, 360)
    indent_dt = START_DATE + timedelta(days=random_days_offset, hours=np.random.uniform(0, 23))
    allocation_dt = indent_dt + timedelta(days=int(np.random.randint(1, 4)), hours=np.random.uniform(1, 12))
    placement_dt = allocation_dt + timedelta(hours=np.random.uniform(12.0, 24.0))
    release_dt = placement_dt + timedelta(hours=turnaround_hours)
    
    # Append Fact Record
    rake_master_records.append({
        "Rake_ID": r_id,
        "Sector": sec,
        "Port_Origin": port,
        "Plant_Destination": dest,
        "Commodity_Type": commodity,
        "Total_Wagons": wagons,
        "Indent_Date": indent_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "Allocation_Date": allocation_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "Placement_Timestamp": placement_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "Release_Timestamp": release_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "Allowed_Free_Time_Hours": free_time,
        "Actual_Turnaround_Time_Hours": turnaround_hours
    })
    
    # Append Dimension Record
    bottleneck_records.append({
        "Rake_ID": r_id,
        "Delay_Root_Cause": cause,
        "Terminal_Efficiency_Score": eff_score
    })

master_rake_df = pd.DataFrame(rake_master_records)
bottlenecks_df = pd.DataFrame(bottleneck_records)

# ---------------------------------------------------------
# 4. Export Datasets to CSV
# ---------------------------------------------------------
master_rake_df.to_csv("Master_Rake_Log.csv", index=False)
demurrage_rules_df.to_csv("Demurrage_Cost_Rules.csv", index=False)
bottlenecks_df.to_csv("Operational_Bottlenecks_Log.csv", index=False)

print("Dataset generation complete:")
print(f" - Master_Rake_Log: {len(master_rake_df)} rows")
print(f" - Demurrage_Cost_Rules: {len(demurrage_rules_df)} rows")
print(f" - Operational_Bottlenecks_Log: {len(bottlenecks_df)} rows")
print(f" - Breach Percentage: {np.round((master_rake_df['Actual_Turnaround_Time_Hours'] > master_rake_df['Allowed_Free_Time_Hours']).mean() * 100, 2)}%")
