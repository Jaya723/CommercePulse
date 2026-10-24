# CommercePulse Project Plan
## A Big Data Analytics Pipeline for E-commerce Insights

---

## Executive Summary

CommercePulse is a **batch data analytics platform** that processes historical Brazilian e-commerce data (Olist dataset). It demonstrates real-world data engineering concepts: data ingestion, validation, cleaning, transformation, analytics, and visualization.

**Timeline:** 1 week
**Difficulty:** Beginner-to-Intermediate
**Interview Value:** High - demonstrates PySpark, data engineering patterns, and end-to-end pipeline

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CommercePulse Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Bronze    │    │   Silver    │    │    Gold     │         │
│  │   (Raw)     │───▶│  (Cleaned)  │───▶│ (Analytics) │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│        │                  │                  │                 │
│        ▼                  ▼                  ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Parquet    │    │  Parquet    │    │  Parquet    │         │
│  │  Validation │    │  Joins      │    │  Metrics    │         │
│  │  Quality    │    │  Cleaning   │    │  Aggregation│         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │  Streamlit        │
                    │  Dashboard        │
                    │  (Visualization)  │
                    └───────────────────┘
```

### Why This Architecture?

1. **Bronze Layer**: Raw data with minimal processing. Acts as immutable source of truth.
2. **Silver Layer**: Cleaned, joined, and validated data. Business-ready but not aggregated.
3. **Gold Layer**: Pre-computed analytics metrics. Optimized for dashboard queries.

This is the **Medallion Architecture** - a real-world pattern used by companies like Databricks, Netflix, and Uber.

---

## Business Questions to Answer

### 1. Order Volume
- **Question**: How many orders are in the dataset?
- **Metric**: Total count of unique orders
- **Nuance**: Include all statuses (delivered, cancelled, shipped, etc.)

### 2. Monthly Trends
- **Question**: What are the monthly order trends?
- **Metric**: Orders per month over time
- **Nuance**: Use `order_purchase_timestamp`, handle timezone correctly

### 3. Category Performance
- **Question**: Which product categories generate the highest item-price totals?
- **Metric**: Sum of `price` per category (NOT revenue)
- **Important**: This is item price only, not including freight or payment value

### 4. Category Metrics
- **Question**: How many distinct orders and items per category?
- **Metrics**:
  - Unique orders per category
  - Total items sold per category

### 5. Delivery Performance
- **Question**: What is the delivery performance of delivered orders?
- **Metrics**:
  - Percentage of orders delivered on time
  - Average delivery delay (days)
- **Nuance**: Only include `order_status = 'delivered'` with valid timestamps

### 6. Order Status Distribution
- **Question**: How do order statuses and delivery times vary?
- **Metrics**:
  - Distribution of order statuses
  - Average delivery time by status

---

## Technology Stack & Why

| Technology | Version | Purpose | Why Real-World? |
|------------|---------|---------|-----------------|
| **Python** | 3.x | Core language | Industry standard for data engineering |
| **PySpark** | 4.2.0 | Distributed processing | Used for big data (TB/PB scale) |
| **Pandas** | 3.1.0 | Small data/validation | Data exploration and testing |
| **Parquet** | - | File format | Columnar, compressed, efficient |
| **Streamlit** | - | Dashboard | Rapid prototyping, deployable |

### Why PySpark Instead of Pandas?

- **Scalability**: PySpark can process data that doesn't fit in memory
- **Distributed**: Runs on clusters for parallel processing
- **Production**: Used in companies like Uber, Netflix, Airbnb
- **Interview Talking Point**: Shows you understand big data concepts

---

## Project Structure

```
BDA Project/
├── data/
│   ├── raw/                    # Original CSV files (downloaded)
│   ├── bronze/                 # Raw Parquet files (PySpark ingested)
│   ├── silver/                 # Cleaned & joined Parquet files
│   └── gold/                   # Aggregated analytics metrics
├── src/
│   ├── commerce_pulse/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration & paths
│   │   ├── ingestion.py        # Bronze layer: CSV → Parquet
│   │   ├── cleaning.py         # Silver layer: Join & clean
│   │   ├── analytics.py        # Gold layer: Compute metrics
│   │   └── pipeline.py         # Main orchestration script
│   └── scripts/
│       ├── run_pipeline.py     # Entry point to run entire pipeline
│       └── utils.py            # Helper functions
├── dashboards/
│   └── app.py                  # Streamlit dashboard
├── tests/
│   ├── test_ingestion.py       # Unit tests for ingestion
│   ├── test_cleaning.py        # Unit tests for cleaning
│   └── test_analytics.py       # Unit tests for analytics
├── docs/
│   ├── PROJECT_PLAN.md         # This file
│   ├── ARCHITECTURE.md         # Detailed architecture explanation
│   ├── DATA_DICTIONARY.md      # Schema documentation
│   └── DEPLOYMENT.md           # How to run & demo
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project overview

```

---

## Implementation Plan (7 Days)

### Day 1: Setup & Data Exploration
**Goal**: Understand the data and set up the project structure

**Tasks**:
1. Fix Java PATH issue (PySpark requires Java)
2. Create project structure (add missing directories)
3. Explore all 9 CSV files using Pandas
4. Document schemas in `DATA_DICTIONARY.md`
5. Identify data quality issues (nulls, duplicates, invalid dates)

**Learning Objectives**:
- Understanding PySpark's Java dependency
- Data profiling techniques
- Writing clear documentation

**Deliverables**:
- `docs/DATA_DICTIONARY.md`
- Project structure complete
- Java/PySpark working

---

### Day 2: Bronze Layer (Ingestion)
**Goal**: Load raw CSVs into Parquet format with validation

**Tasks**:
1. Create `src/commerce_pulse/config.py` (paths, Spark config)
2. Create `src/commerce_pulse/ingestion.py`:
   - Function to load CSV to PySpark DataFrame
   - Schema validation (check column names and types)
   - Data quality checks (null counts, duplicate checks)
   - Save as Parquet in `data/bronze/`
3. Create tests for ingestion
4. Run ingestion for all 9 tables

**Learning Objectives**:
- PySpark DataFrame operations
- Schema validation
- Data quality monitoring
- Parquet file format benefits

**Deliverables**:
- `config.py` and `ingestion.py`
- All 9 tables in `data/bronze/`
- Unit tests passing

---

### Day 3: Silver Layer (Cleaning & Joining)
**Goal**: Clean data and join related tables

**Tasks**:
1. Create `src/commerce_pulse/cleaning.py`:
   - Handle missing values (nulls)
   - Remove duplicates
   - Fix date formats
   - Join related tables:
     - Orders + Customers (customer details)
     - Orders + Order Items (product details)
     - Products + Category Translation (English names)
     - Order Items + Sellers (seller details)
2. Create tests for cleaning
3. Save cleaned data to `data/silver/`

**Learning Objectives**:
- PySpark joins (inner, left, outer)
- Data cleaning strategies
- Handling referential integrity
- When to use different join types

**Deliverables**:
- `cleaning.py`
- 2-3 joined tables in `data/silver/`
- Unit tests passing

---

### Day 4: Gold Layer (Analytics)
**Goal**: Compute business metrics for the 6 questions

**Tasks**:
1. Create `src/commerce_pulse/analytics.py`:
   - **Metric 1**: Total order count
   - **Metric 2**: Monthly order trends
   - **Metric 3**: Category item-price totals
   - **Metric 4**: Category order & item counts
   - **Metric 5**: Delivery performance (on-time %, avg delay)
   - **Metric 6**: Order status distribution
2. Save each metric as a separate Parquet file in `data/gold/`
3. Create tests for analytics
4. Verify metrics with manual calculations

**Learning Objectives**:
- PySpark aggregations (group by, sum, count, avg)
- Window functions (if needed)
- Date/time operations in PySpark
- Defining metrics precisely

**Deliverables**:
- `analytics.py`
- 6 metric files in `data/gold/`
- Unit tests passing

---

### Day 5: Pipeline Orchestration
**Goal**: Create a single script to run the entire pipeline

**Tasks**:
1. Create `src/scripts/run_pipeline.py`:
   - Initialize Spark session
   - Run Bronze → Silver → Gold in sequence
   - Add error handling
   - Add logging (progress tracking)
2. Test the full pipeline end-to-end
3. Add idempotency (can run multiple times safely)

**Learning Objectives**:
- Pipeline orchestration
- Error handling patterns
- Logging best practices
- Idempotent design

**Deliverables**:
- `run_pipeline.py`
- Full pipeline running successfully
- Log file showing progress

---

### Day 6: Streamlit Dashboard
**Goal**: Create an interactive dashboard to visualize metrics

**Tasks**:
1. Install Streamlit: `pip install streamlit`
2. Create `dashboards/app.py`:
   - Load Gold layer Parquet files
   - Create 6 pages/tabs for each metric
   - Add charts (line charts, bar charts, pie charts)
   - Add explanations for each metric
3. Test dashboard locally

**Learning Objectives**:
- Streamlit basics
- Data visualization
- Creating user-friendly dashboards
- Business storytelling with data

**Deliverables**:
- `dashboards/app.py`
- Working dashboard
- Screenshots for documentation

---

### Day 7: Documentation & Demo Prep
**Goal**: Prepare for interview presentation

**Tasks**:
1. Write `README.md`:
   - Project overview
   - Setup instructions
   - How to run pipeline
   - How to run dashboard
2. Write `docs/ARCHITECTURE.md`:
   - Detailed architecture explanation
   - Technology choices
   - Design decisions
3. Write `docs/DEPLOYMENT.md`:
   - Step-by-step run instructions
   - Common issues & solutions
4. Practice demo:
   - Run pipeline
   - Show dashboard
   - Explain each metric
5. Add `.gitignore` to exclude sensitive/large files

**Learning Objectives**:
- Technical writing
- Presentation skills
- Explaining technical concepts clearly

**Deliverables**:
- Complete documentation
- Demo script
- Ready for interviews

---

## Real-World Concepts You'll Learn

### 1. Medallion Architecture
- Bronze (raw) → Silver (cleaned) → Gold (aggregated)
- Used by Databricks, Uber, Netflix
- Benefits: Debugging, reproducibility, performance

### 2. Data Quality Monitoring
- Schema validation
- Null checks
- Duplicate detection
- Important in production pipelines

### 3. Idempotency
- Running pipeline multiple times produces same result
- Prevents double-counting
- Critical for production systems

### 4. Columnar Storage (Parquet)
- Efficient compression
- Fast queries on specific columns
- Industry standard for big data

### 5. Error Handling
- Try-except blocks
- Logging
- Graceful failures
- Professional code quality

### 6. Testing
- Unit tests for each layer
- Verify logic correctness
- Catch regressions
- Industry best practice

---

## Interview Talking Points

### Technical
- "I used PySpark for distributed processing because it scales to big data"
- "I implemented the Medallion Architecture for data quality and debuggability"
- "I used Parquet for efficient columnar storage"
- "I added data quality checks at the Bronze layer to catch issues early"
- "I made the pipeline idempotent so it can be re-run safely"

### Business
- "I calculated 6 key business metrics for e-commerce analytics"
- "I handled edge cases like cancelled orders and missing delivery dates"
- "I defined metrics precisely (e.g., item price vs revenue)"
- "I built an interactive dashboard for business stakeholders"

### Process
- "I broke the project into modular layers for maintainability"
- "I wrote unit tests to ensure correctness"
- "I documented the architecture and data dictionary"
- "I used logging for pipeline monitoring"

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Java/PySpark setup issues | Address on Day 1, document fixes |
| Data too large for local machine | Use PySpark sampling for testing |
| Time constraints | Focus on core functionality first |
| Complex joins | Start with simple joins, add complexity gradually |
| PySpark learning curve | Use Pandas for exploration, PySpark for production |

---

## Success Criteria

1. ✅ Pipeline runs end-to-end without errors
2. ✅ All 6 metrics computed correctly
3. ✅ Dashboard displays all metrics clearly
4. ✅ Code is well-documented and tested
5. ✅ Can explain architecture and decisions
6. ✅ Can run and demo independently

---

## Next Steps

Ready to start? Begin with **Day 1: Setup & Data Exploration**:

1. Fix Java PATH issue
2. Explore the 9 CSV files
3. Document schemas
4. Set up project structure

I'll guide you through each day with clear instructions and explanations.

---

## Questions Before We Start?

Do you have any questions about:
- The architecture?
- The timeline?
- The technologies?
- The metrics?
