
Global Demurrage & Detention Control Center
1. Synthetic Data Generator
File: generate_data.py
"""
Global Demurrage & Detention Control Center: Synthetic Data Engine
Author: Senior SCM & Logistics Data Architecture Portfolio
Scale: 1,500 Heavy-Haul Rake Operations (Last 12 Months)
"""
The generator creates a reproducible synthetic dataset of 1,500 heavy-haul rake operations covering 12 months.
Key characteristics:
•	Deterministic random seed: 42 
•	Four anonymized port categories in the final portfolio version: 
o	Port A 
o	Port B 
o	Port C 
o	Port D 
•	Three sectors: 
o	Steel 
o	Power 
o	Mining 
•	Multiple commodity types 
•	Port-specific: 
o	Hourly penalty rate 
o	Grace period 
•	Operational delay modelling 
•	Terminal efficiency scoring 
•	Sequential operational timestamps: 
o	Indent 
o	Allocation 
o	Placement 
o	Release 
Generated files
Master_Rake_Log.csv
Demurrage_Cost_Rules.csv
Operational_Bottlenecks_Log.csv
The dataset intentionally contains a realistic level of demurrage exposure for analytical purposes.
________________________________________
2. Power BI Semantic Model
Model Structure
Fact Table
Master_Rake_Log
Contains the primary operational transaction/rake-level records.
Supporting Tables
Operational_Bottlenecks_Log
Contains:
•	Rake ID 
•	Delay Root Cause 
•	Terminal Efficiency Score 
Demurrage_Cost_Rules
Contains:
•	Port Origin 
•	Hourly Penalty Rate 
•	Grace Period 
Dim_Calendar
Provides time-based analysis.
________________________________________
3. Implemented Relationships
Relationship 1
Operational_Bottlenecks_Log[Rake_ID]
        ↕
Master_Rake_Log[Rake_ID]
•	Cardinality: 1:1 
•	Cross-filter direction: Both 
•	Active: Yes 
Reason: Power BI requires bidirectional filtering for this 1:1 configuration in the implemented model.
Relationship 2
Master_Rake_Log[Port_Origin]
        →
Demurrage_Cost_Rules[Port_Origin]
•	Cardinality: Many-to-1 
•	Cross-filter direction: Single 
•	Active: Yes 
Relationship 3
Dim_Calendar[Date]
        →
Master_Rake_Log[Placement_Date]
•	Cardinality: *1: ** 
•	Cross-filter direction: Single 
•	Active: Yes 
Placement_Date is a date-only column derived from Placement_Timestamp.
________________________________________
4. Calendar Intelligence
The model contains:
Dim_Calendar
with:
Date
Year_Month
Year_Month_Sort
Year_Month is sorted using Year_Month_Sort to ensure chronological monthly reporting.
________________________________________
5. Core DAX Measures
Measure 1 — Total Demurrage Incurred
Total Demurrage Incurred = 
SUMX(
    'Master_Rake_Log',
    VAR _Port = 'Master_Rake_Log'[Port_Origin]
    VAR _ActualHours = 'Master_Rake_Log'[Actual_Turnaround_Time_Hours]
    VAR _FreeHours = 'Master_Rake_Log'[Allowed_Free_Time_Hours]
    VAR _GraceHours = RELATED('Demurrage_Cost_Rules'[Grace_Period_Hours])
    VAR _HourlyRate = RELATED('Demurrage_Cost_Rules'[Hourly_Penalty_Rate_INR])
    VAR _BillableHours = 
        IF(
            _ActualHours > (_FreeHours + _GraceHours),
            _ActualHours - _FreeHours,
            0
        )
    RETURN
        _BillableHours * _HourlyRate
)
Purpose
Calculates the aggregate demurrage exposure based on:
Actual turnaround → contractual free time → grace-period breach → applicable hourly penalty rate.
________________________________________
6. Average Turnaround Deviation
Average Turnaround Deviation = 
AVERAGEX(
    'Master_Rake_Log',
    'Master_Rake_Log'[Actual_Turnaround_Time_Hours] - 'Master_Rake_Log'[Allowed_Free_Time_Hours]
)
Purpose
Measures the average deviation between actual turnaround and the allowed free-time baseline.
Positive values indicate turnaround above the contractual free-time baseline.
________________________________________
7. Financial Risk Horizon
Financial Risk Horizon = 
CALCULATE(
    [Total Demurrage Incurred],
    KEEPFILTERS('Operational_Bottlenecks_Log'[Terminal_Efficiency_Score] < 0.40),
    KEEPFILTERS('Operational_Bottlenecks_Log'[Delay_Root_Cause] <> "None (Nominal Operations)")
)
Purpose
Identifies the portion of demurrage exposure associated with low-efficiency operational conditions, defined in this case as:
Terminal Efficiency Score < 0.40
and excluding nominal operations.
________________________________________
8. Executive Control Tower
The Power BI dashboard provides:
KPI Cards
•	Total Demurrage Incurred 
•	Financial Risk Horizon 
•	Average Turnaround Deviation 
Analytical Views
•	Demurrage by Port 
•	Demurrage by Delay Root Cause 
•	Monthly Demurrage Trend 
•	Average Turnaround Deviation by Port 
•	Demurrage by Sector 
Interactive Slicers
•	Port 
•	Sector 
•	Commodity 
•	Delay Root Cause 
•	Year-Month 
________________________________________
9. Management Analysis Framework
The dashboard is designed to answer five management questions:
1. Financial
How much demurrage exposure exists?
2. Operational
Where is turnaround performance deteriorating?
3. Root Cause
What operational factors are creating the exposure?
4. Segmentation
Which ports, sectors and commodities contribute most to the exposure?
5. Intervention
Where should management focus operational improvement efforts?
________________________________________
10. Intervention Framework
The analytical workflow is:
Demurrage Exposure
        ↓
Identify High-Exposure Port
        ↓
Identify Delay Root Cause
        ↓
Assess Terminal Efficiency
        ↓
Identify Operational Bottleneck
        ↓
Define Corrective Intervention
        ↓
Track Financial Impact
Example intervention categories:
•	Yard congestion reduction 
•	Equipment reliability improvement 
•	Railway coordination 
•	Shift-handover improvement 
•	Weather contingency planning 
•	Terminal process optimisation 
________________________________________
11. Implemented vs Future State
Implemented
Synthetic Data
      ↓
Python Data Generation
      ↓
CSV Dataset
      ↓
Power BI Semantic Model
      ↓
DAX Measures
      ↓
Interactive Control Tower
      ↓
Management Analysis
Future Enhancement
Historical Operational Data
          ↓
Predictive Analytics
          ↓
Demurrage Risk Prediction
          ↓
Early Warning
          ↓
Recommended Intervention
          ↓
Agentic AI
          ↓
Semi-Autonomous Decision Support
The predictive and agentic components are future roadmap items, not implemented functionality in this project.
________________________________________
12. Technology Stack
Python
Pandas
NumPy
Power BI
DAX
Git
GitHub
Future technology extensions may include:
Machine Learning
Predictive Analytics
LLMs
RAG
AI Agents
Agentic Workflows
These should be presented as future architecture, not current implementation.
________________________________________
13. Portfolio Positioning
Project Title
Global Demurrage & Detention Control Center
Positioning
A synthetic enterprise analytics case study demonstrating how operational transaction data can be transformed into a management control tower for:
•	Demurrage exposure 
•	Operational bottlenecks 
•	Root-cause analysis 
•	Financial risk visibility 
•	Performance intervention 
The project demonstrates the integration of:
Supply Chain + Rail Operations + Asset/Terminal Operations + Financial Analytics + Business Intelligence.
________________________________________
14. GitHub Structure
Use the actual repository structure:
global-demurrage-detention-control-center/
│
├── .gitignore
├── generate_data.py
│
├── Master_Rake_Log.csv
├── Demurrage_Cost_Rules.csv
├── Operational_Bottlenecks_Log.csv
│
├── powerbi/
│   └── Global_Demurrage_Detention_Control_Center.pbix
│
└── screenshots/
    ├── 01_Executive_Control_Tower.png
    ├── 02_Financial_Exposure_Analysis.png
    ├── 03_Operational_Root_Cause_Analysis.png
    ├── 04_Port_A_Analysis.png
    ├── 05_Steel_Sector_Analysis.png
    ├── 06_Iron_Ore_Commodity_Analysis.png
    └── 07_Yard_Congestion_Root_Cause_Analysis.png
________________________________________
15. Data Disclaimer
Use this prominently in the documentation:
Synthetic data | Illustrative enterprise business scenario | No real company, customer, port or operational data used.
This is important because the project uses realistic-looking operational terminology and financial values.
________________________________________
16. Final Portfolio Statement
Global Demurrage & Detention Control Center is a synthetic enterprise analytics project that demonstrates how rail and terminal operational data can be transformed into an interactive financial and operational control tower using Python, Power BI and DAX.

