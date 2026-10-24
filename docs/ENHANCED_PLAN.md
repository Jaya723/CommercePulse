# CommercePulse: Enhanced Project Plan
## Complete Architecture & Implementation Guide

---

## Project Overview

CommercePulse is a **full-stack big data analytics platform** that processes historical Brazilian e-commerce data (Olist dataset) through a 3-layer pipeline and presents insights through a modern React-based dashboard.

**Tech Stack**:
- **Backend**: Python, PySpark, FastAPI
- **Frontend**: React, Recharts, React-Leaflet
- **Data**: Parquet (columnar storage)
- **Pipeline**: Bronze → Silver → Gold (Medallion Architecture)

**Timeline**: 7 days
**Target**: College submission + Software Engineering/Data Engineering interviews

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CommercePulse Architecture                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     Data Pipeline Layer                         │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │                                                                 │   │
│  │  ┌──────────┐      ┌──────────┐      ┌──────────┐             │   │
│  │  │  Bronze  │─────▶│  Silver  │─────▶│   Gold   │             │   │
│  │  │  (Raw)   │      │(Cleaned) │      │(Metrics) │             │   │
│  │  └──────────┘      └──────────┘      └──────────┘             │   │
│  │       │                  │                  │                │   │
│  │       ▼                  ▼                  ▼                │   │
│  │  ┌──────────┐      ┌──────────┐      ┌──────────┐             │   │
│  │  │ Parquet  │      │ Parquet  │      │ Parquet  │             │   │
│  │  │ Validate │      │ Joins    │      │ Aggreg.  │             │   │
│  │  │ Quality  │      │ Clean    │      │ RFM      │             │   │
│  │  └──────────┘      └──────────┘      └──────────┘             │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     API Layer (FastAPI)                          │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │                                                                 │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │  REST API Endpoints                                    │   │   │
│  │  │                                                        │   │   │
│  │  │  GET /api/metrics/overview                            │   │   │
│  │  │  GET /api/metrics/trends                              │   │   │
│  │  │  GET /api/metrics/geospatial                          │   │   │
│  │  │  GET /api/metrics/customers                           │   │   │
│  │  │  GET /api/metrics/products                            │   │   │
│  │  │  GET /api/metrics/delivery                            │   │   │
│  │  │  GET /api/quality/score                               │   │   │
│  │  │  GET /api/performance/benchmark                       │   │   │
│  │  │  GET /api/pipeline/status                             │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  Frontend Layer (React)                         │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │                                                                 │   │
│  │  ┌────────────────────────────────────────────────────────┐   │   │
│  │  │  React SPA (Single Page Application)                   │   │   │
│  │  │                                                        │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │   │
│  │  │  │ Overview │  │  Trends  │  │   Geo    │           │   │   │
│  │  │  │   Page   │  │   Page   │  │   Page   │           │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘           │   │   │
│  │  │                                                        │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │   │
│  │  │  │Customers │  │ Products │  │ Delivery │           │   │   │
│  │  │  │   Page   │  │   Page   │  │   Page   │           │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘           │   │   │
│  │  │                                                        │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │   │
│  │  │  │ Quality  │  │Perform.  │  │   Data   │           │   │   │
│  │  │  │   Page   │  │   Page   │  │ Dictionary│          │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘           │   │   │
│  │  └────────────────────────────────────────────────────────┘   │   │
│  │                                                                 │   │
│  │  Components: Recharts (charts), React-Leaflet (maps),         │   │
│  │              Material-UI (UI), Axios (API calls)               │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Details

### Backend (Python)

| Technology | Purpose | Why This Choice? |
|------------|---------|------------------|
| **PySpark 4.2.0** | Distributed data processing | Industry standard for big data, used by Uber/Netflix |
| **Pandas 3.1.0** | Data exploration & validation | Fast for small data, great for profiling |
| **FastAPI** | REST API server | Modern, fast, automatic docs, type-safe |
| **Pydantic** | Data validation | Works seamlessly with FastAPI |
| **Parquet** | File format | Columnar, compressed, 10x smaller than CSV |
| **Java 17** | PySpark dependency | Required for Spark JVM |

### Frontend (React)

| Technology | Purpose | Why This Choice? |
|------------|---------|------------------|
| **React 18** | Frontend framework | Industry standard, huge ecosystem |
| **Vite** | Build tool | Fast development, modern |
| **Recharts** | Charts library | React-native, declarative, beautiful |
| **React-Leaflet** | Maps | Interactive maps, easy to use |
| **Material-UI (MUI)** | UI components | Professional look, responsive |
| **Axios** | HTTP client | Promise-based, error handling |
| **React Router** | Navigation | SPA routing |
| **Tailwind CSS** | Styling | Utility-first, fast development |

### Why React Over Streamlit?

| Factor | Streamlit | React |
|--------|-----------|-------|
| **Industry Use** | Data science prototypes | Production applications |
| **Customization** | Limited | Full control |
| **Learning Value** | Python-specific | Transferable to any web dev |
| **Career Impact** | Shows data skills | Shows full-stack skills |
| **Portfolio Value** | Good | Better |
| **Interview Impact** | "I used Streamlit" | "I built a full-stack app" |

**React is the better choice for interviews** because it shows full-stack capability, which is highly valued in both software engineering and data engineering roles.

---

## Data Flow Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Raw CSV   │────▶│   Bronze    │────▶│   Silver    │
│   (9 files) │     │   Parquet   │     │   Parquet   │
└─────────────┘     └─────────────┘     └─────────────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │    Gold     │
                                    │   Parquet   │
                                    └─────────────┘
                                           │
                                           ▼
                            ┌────────────────────────┐
                            │   FastAPI Backend     │
                            │   (reads Parquet)     │
                            └────────────────────────┘
                                           │
                                           │ REST API (JSON)
                                           ▼
                            ┌────────────────────────┐
                            │   React Frontend       │
                            │   (displays data)      │
                            └────────────────────────┘
```

---

## Project Structure

```
BDA Project/
├── data/
│   ├── raw/                           # Original CSV files
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│   ├── bronze/                        # Raw Parquet files
│   ├── silver/                        # Cleaned & joined Parquet
│   ├── gold/                          # Aggregated metrics
│   │   ├── overview_metrics.parquet
│   │   ├── monthly_trends.parquet
│   │   ├── category_performance.parquet
│   │   ├── delivery_metrics.parquet
│   │   ├── order_status.parquet
│   │   ├── customer_rfm.parquet
│   │   ├── regional_metrics.parquet
│   │   └── seller_performance.parquet
│   └── quality/                       # Data quality metrics
│       └── quality_report.json
│
├── src/
│   ├── commerce_pulse/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration
│   │   ├── ingestion.py               # Bronze layer
│   │   ├── cleaning.py                # Silver layer
│   │   ├── analytics.py               # Gold layer (basic)
│   │   ├── customer_analytics.py      # RFM analysis
│   │   ├── regional_analytics.py     # Regional analysis
│   │   ├── seller_analytics.py       # Seller analysis
│   │   ├── data_quality.py            # Quality framework
│   │   └── pipeline.py                # Orchestration
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── metrics.py             # Metrics endpoints
│   │   │   ├── quality.py             # Quality endpoints
│   │   │   ├── performance.py         # Benchmark endpoints
│   │   │   └── pipeline.py            # Pipeline status
│   │   └── models/
│   │       ├── __init__.py
│   │       └── schemas.py             # Pydantic models
│   │
│   ├── scripts/
│   │   ├── run_pipeline.py            # Pipeline entry point
│   │   ├── benchmark.py               # Pandas vs PySpark
│   │   └── profile_data.py            # Data profiling
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                 # Utility functions
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx                  # React entry
│   │   ├── App.jsx                   # Main app
│   │   ├── index.css
│   │   │
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   ├── Charts/
│   │   │   │   ├── LineChart.jsx
│   │   │   │   ├── BarChart.jsx
│   │   │   │   ├── PieChart.jsx
│   │   │   │   └── MapChart.jsx
│   │   │   ├── Metrics/
│   │   │   │   ├── MetricCard.jsx
│   │   │   │   └── MetricTable.jsx
│   │   │   └── UI/
│   │   │       ├── Loading.jsx
│   │   │       └── Error.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Overview.jsx
│   │   │   ├── Trends.jsx
│   │   │   ├── Geospatial.jsx
│   │   │   ├── Customers.jsx
│   │   │   ├── Products.jsx
│   │   │   ├── Delivery.jsx
│   │   │   ├── Quality.jsx
│   │   │   ├── Performance.jsx
│   │   │   └── DataDictionary.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js                 # Axios instance
│   │   │
│   │   └── hooks/
│   │       └── useMetrics.js          # Custom hooks
│   │
│   └── public/
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_cleaning.py
│   ├── test_analytics.py
│   └── test_api.py
│
├── docs/
│   ├── PROJECT_PLAN.md               # This file
│   ├── ARCHITECTURE.md               # Detailed architecture
│   ├── DATA_DICTIONARY.md            # Schema documentation
│   ├── API_DOCUMENTATION.md          # API endpoints
│   ├── DEPLOYMENT.md                 # How to run
│   ├── PRESENTATION.md               # Slide outline
│   └── DEMO_SCRIPT.md                # Demo steps
│
├── requirements.txt                   # Python dependencies
├── .gitignore
└── README.md
```

---

## Business Metrics (Complete List)

### Core Metrics (Original 6)

#### 1. Order Volume
- **Total Orders**: Count of unique orders in dataset
- **By Status**: Orders by status (delivered, cancelled, shipped, etc.)
- **Data Source**: `olist_orders_dataset.csv`

#### 2. Monthly Trends
- **Orders per Month**: Time series of order counts
- **Monthly Revenue**: Sum of payment values per month
- **Data Source**: `olist_orders_dataset.csv` + `olist_order_payments_dataset.csv`

#### 3. Category Performance
- **Item Price Totals**: Sum of `price` per product category
- **Average Order Value**: Average price per order per category
- **Data Source**: `olist_order_items_dataset.csv` + `olist_products_dataset.csv`

#### 4. Category Metrics
- **Distinct Orders per Category**: Count of unique orders
- **Total Items per Category**: Sum of `order_item_id`
- **Data Source**: `olist_order_items_dataset.csv` + `olist_products_dataset.csv`

#### 5. Delivery Performance
- **On-Time Delivery Rate**: % of orders delivered on or before estimated date
- **Average Delivery Delay**: Days difference between actual and estimated delivery
- **Data Source**: `olist_orders_dataset.csv` (only `order_status = 'delivered'`)

#### 6. Order Status Distribution
- **Status Breakdown**: Count and percentage per status
- **Delivery Time by Status**: Average delivery time per status
- **Data Source**: `olist_orders_dataset.csv`

### Enhanced Metrics (New)

#### 7. Customer RFM Analysis ⭐
- **Recency**: Days since customer's last order
- **Frequency**: Number of orders per customer
- **Monetary**: Total spend per customer
- **Segments**: High-value, Loyal, At-risk, New, Churned
- **Data Source**: `olist_orders_dataset.csv` + `olist_customers_dataset.csv` + `olist_order_payments_dataset.csv`

#### 8. Regional Performance ⭐
- **Orders by State**: Total orders per Brazilian state
- **Delivery Time by State**: Average delivery days per state
- **Revenue by State**: Total revenue per state
- **Top States**: Top 5 states by order volume
- **Data Source**: `olist_customers_dataset.csv` + `olist_orders_dataset.csv`

#### 9. Seller Performance ⭐
- **Top Sellers by Revenue**: Top 10 sellers by total sales
- **Seller Order Count**: Number of orders per seller
- **Seller Delivery Performance**: Average delivery time per seller
- **Data Source**: `olist_order_items_dataset.csv` + `olist_sellers_dataset.csv`

#### 10. Geospatial Analysis ⭐
- **Order Map**: Map visualization of orders by location
- **Seller Map**: Map visualization of seller locations
- **Heatmap**: Order density heatmap
- **Data Source**: `olist_geolocation_dataset.csv`

---

## Data Quality Framework

### Quality Checks

| Check Type | Description | Threshold |
|------------|-------------|-----------|
| **Null Check** | Percentage of null values per column | < 5% |
| **Duplicate Check** | Number of duplicate rows | 0 |
| **Date Validation** | Invalid date formats | 0 |
| **Referential Integrity** | Foreign key violations | 0 |
| **Value Range** | Values outside expected ranges | 0 |

### Quality Scoring

- **Overall Score**: Weighted average of all checks (0-100)
- **Per-Table Score**: Quality score per dataset
- **Per-Column Score**: Quality score per column

### Quality Dashboard

- Visual quality score with color coding (green/yellow/red)
- Drill-down to see specific issues
- Trend over time (if pipeline runs multiple times)

---

## Performance Benchmarking

### Benchmark Strategy

Compare Pandas vs PySpark on:

1. **Bronze Layer**: Loading 9 CSV files
2. **Silver Layer**: Joining 3 tables
3. **Gold Layer**: Computing aggregations

### Metrics to Track

- **Execution Time**: Wall-clock time
- **Memory Usage**: Peak memory consumption
- **CPU Usage**: Average CPU utilization

### Visualization

- Bar chart comparing execution times
- Speedup ratio (PySpark / Pandas)
- Memory usage comparison

---

## API Architecture (FastAPI)

### Base URL
`http://localhost:8000`

### Endpoints

#### Metrics Endpoints

```
GET /api/metrics/overview
Response: {
  "total_orders": 99441,
  "total_revenue": 15000000.00,
  "avg_order_value": 150.95,
  "top_category": "bed_bath_table"
}

GET /api/metrics/trends?start_date=2017-01-01&end_date=2018-12-31
Response: {
  "monthly_orders": [{"month": "2017-01", "count": 500}, ...],
  "monthly_revenue": [{"month": "2017-01", "revenue": 75000}, ...]
}

GET /api/metrics/geospatial
Response: {
  "orders_by_state": [{"state": "SP", "count": 40000}, ...],
  "delivery_by_state": [{"state": "SP", "avg_days": 5.2}, ...]
}

GET /api/metrics/customers
Response: {
  "rfm_segments": [{"segment": "High-value", "count": 5000}, ...],
  "top_customers": [{"customer_id": "xxx", "total_spend": 5000}, ...]
}

GET /api/metrics/products
Response: {
  "category_performance": [{"category": "bed_bath_table", "total": 1000000}, ...],
  "category_orders": [{"category": "bed_bath_table", "orders": 10000}, ...]
}

GET /api/metrics/delivery
Response: {
  "on_time_rate": 0.95,
  "avg_delay_days": 2.3,
  "status_distribution": [{"status": "delivered", "count": 90000}, ...]
}
```

#### Quality Endpoints

```
GET /api/quality/score
Response: {
  "overall_score": 87,
  "table_scores": [
    {"table": "orders", "score": 92},
    {"table": "customers", "score": 85}
  ],
  "issues": [
    {"table": "orders", "column": "order_approved_at", "null_pct": 3.2}
  ]
}
```

#### Performance Endpoints

```
GET /api/performance/benchmark
Response: {
  "bronze_layer": {
    "pandas_time": 15.2,
    "pyspark_time": 8.5,
    "speedup": 1.79
  },
  "silver_layer": {
    "pandas_time": 25.3,
    "pyspark_time": 8.1,
    "speedup": 3.12
  },
  "gold_layer": {
    "pandas_time": 5.2,
    "pyspark_time": 4.8,
    "speedup": 1.08
  }
}
```

#### Pipeline Endpoints

```
GET /api/pipeline/status
Response: {
  "last_run": "2026-10-24T19:00:00",
  "status": "success",
  "duration_seconds": 120,
  "layer_status": {
    "bronze": "success",
    "silver": "success",
    "gold": "success"
  }
}

POST /api/pipeline/run
Response: {
  "job_id": "pipeline_20261024_190000",
  "status": "started"
}
```

### API Features

- **Automatic Documentation**: Swagger UI at `/docs`
- **Type Validation**: Pydantic models for request/response
- **Error Handling**: Standardized error responses
- **CORS**: Enabled for frontend communication

---

## Frontend Architecture (React)

### Component Hierarchy

```
App
├── Layout
│   ├── Navbar (navigation)
│   └── Sidebar (page links)
├── Pages
│   ├── Overview
│   │   ├── MetricCard (key metrics)
│   │   └── MetricTable (detailed metrics)
│   ├── Trends
│   │   ├── LineChart (monthly trends)
│   │   └── BarChart (revenue trends)
│   ├── Geospatial
│   │   ├── MapChart (order map)
│   │   └── BarChart (state comparison)
│   ├── Customers
│   │   ├── PieChart (RFM segments)
│   │   └── BarChart (top customers)
│   ├── Products
│   │   ├── BarChart (category performance)
│   │   └── Table (category details)
│   ├── Delivery
│   │   ├── MetricCard (on-time rate)
│   │   └── BarChart (status distribution)
│   ├── Quality
│   │   ├── MetricCard (quality score)
│   │   └── Table (quality issues)
│   ├── Performance
│   │   ├── BarChart (benchmark results)
│   │   └── Table (detailed metrics)
│   └── DataDictionary
│       └── Table (schema documentation)
└── UI
    ├── Loading (spinner)
    └── Error (error message)
```

### State Management

- **React Hooks**: useState, useEffect, useContext
- **Custom Hooks**: useMetrics (API calls), useChartData (chart data processing)
- **No Redux**: Not needed for this scale

### API Integration

```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

export const getOverview = () => api.get('/metrics/overview');
export const getTrends = (params) => api.get('/metrics/trends', { params });
export const getGeospatial = () => api.get('/metrics/geospatial');
// ... other endpoints
```

### Chart Libraries

- **Recharts**: Line charts, bar charts, pie charts
- **React-Leaflet**: Interactive maps
- **Material-UI**: Table components

### Responsive Design

- **Desktop**: Full sidebar, grid layouts
- **Tablet**: Collapsible sidebar, stacked layouts
- **Mobile**: Bottom navigation, single column

---

## Implementation Plan (7 Days)

### Day 1: Setup & Data Exploration

**Goals**:
- Fix Java PATH for PySpark
- Explore all 9 CSV files
- Document schemas
- Set up project structure
- Automated data profiling

**Tasks**:
1. Fix Java PATH issue
2. Create project directories
3. Explore each CSV with Pandas
4. Create `docs/DATA_DICTIONARY.md`
5. Install ydata-profiling (optional) or write custom profiler
6. Generate profiling report
7. Set up Python virtual environment
8. Install dependencies (PySpark, FastAPI, etc.)

**Deliverables**:
- Java/PySpark working
- `docs/DATA_DICTIONARY.md`
- `docs/PROFILING_REPORT.html`
- Complete project structure
- `requirements.txt` updated

**Learning Objectives**:
- PySpark setup and Java dependency
- Data profiling techniques
- Writing clear documentation

---

### Day 2: Bronze Layer + Data Quality

**Goals**:
- Implement Bronze layer (CSV → Parquet)
- Add data quality framework
- Create quality dashboard backend

**Tasks**:
1. Create `src/commerce_pulse/config.py`
2. Create `src/commerce_pulse/ingestion.py`:
   - Load CSV to PySpark DataFrame
   - Schema validation
   - Save as Parquet
3. Create `src/commerce_pulse/data_quality.py`:
   - Null checks
   - Duplicate checks
   - Date validation
   - Quality scoring
4. Ingest all 9 tables
5. Run quality checks
6. Save quality metrics to `data/quality/`
7. Create unit tests

**Deliverables**:
- `config.py`, `ingestion.py`, `data_quality.py`
- All 9 tables in `data/bronze/`
- Quality report in `data/quality/quality_report.json`
- Unit tests passing

**Learning Objectives**:
- PySpark DataFrame operations
- Schema validation
- Data quality monitoring
- Parquet file format

---

### Day 3: Silver Layer (Cleaning & Joining)

**Goals**:
- Clean data
- Join related tables
- Handle edge cases

**Tasks**:
1. Create `src/commerce_pulse/cleaning.py`:
   - Handle missing values
   - Remove duplicates
   - Fix date formats
   - Normalize text
2. Implement joins:
   - Orders + Customers
   - Orders + Order Items
   - Products + Category Translation
   - Order Items + Sellers
3. Save joined tables to `data/silver/`
4. Create unit tests
5. Verify referential integrity

**Deliverables**:
- `cleaning.py`
- 3-4 joined tables in `data/silver/`
- Unit tests passing

**Learning Objectives**:
- PySpark joins (inner, left, outer)
- Data cleaning strategies
- Handling missing data
- Referential integrity

---

### Day 4: Gold Layer + Advanced Analytics

**Goals**:
- Compute all business metrics
- Implement RFM analysis
- Add regional and seller analytics

**Tasks**:
1. Create `src/commerce_pulse/analytics.py` (6 core metrics):
   - Order volume
   - Monthly trends
   - Category performance
   - Category metrics
   - Delivery performance
   - Order status distribution
2. Create `src/commerce_pulse/customer_analytics.py` (RFM):
   - Recency calculation
   - Frequency calculation
   - Monetary calculation
   - Customer segmentation
3. Create `src/commerce_pulse/regional_analytics.py`:
   - Orders by state
   - Delivery by state
   - Revenue by state
4. Create `src/commerce_pulse/seller_analytics.py`:
   - Top sellers by revenue
   - Seller order counts
   - Seller delivery performance
5. Save all metrics to `data/gold/`
6. Create unit tests
7. Verify metrics manually

**Deliverables**:
- `analytics.py`, `customer_analytics.py`, `regional_analytics.py`, `seller_analytics.py`
- 10 metric files in `data/gold/`
- Unit tests passing

**Learning Objectives**:
- PySpark aggregations
- Window functions
- Customer segmentation (RFM)
- Geospatial analytics

---

### Day 5: Pipeline Orchestration + Benchmarking + API Setup

**Goals**:
- Create orchestration script
- Add performance benchmarking
- Set up FastAPI backend

**Tasks**:
1. Create `src/scripts/run_pipeline.py`:
   - Initialize Spark session
   - Run Bronze → Silver → Gold
   - Add error handling
   - Add logging
   - Track execution time
2. Create `src/scripts/benchmark.py`:
   - Benchmark Pandas vs PySpark
   - Measure time, memory, CPU
   - Save results to `data/metrics/`
3. Set up FastAPI:
   - Create `src/api/main.py`
   - Create `src/api/routers/metrics.py`
   - Create `src/api/routers/quality.py`
   - Create `src/api/routers/performance.py`
   - Create `src/api/routers/pipeline.py`
   - Create `src/api/models/schemas.py`
4. Test all API endpoints
5. Add CORS for frontend

**Deliverables**:
- `run_pipeline.py`, `benchmark.py`
- FastAPI backend with all endpoints
- API documentation at `/docs`
- Benchmark results

**Learning Objectives**:
- Pipeline orchestration
- Performance benchmarking
- FastAPI framework
- REST API design
- Error handling and logging

---

### Day 6: React Frontend

**Goals**:
- Set up React project
- Build all pages
- Integrate with API
- Add charts and maps

**Tasks**:
1. Set up React with Vite:
   - `npm create vite@latest frontend -- --template react`
   - Install dependencies (Recharts, React-Leaflet, MUI, Axios, Tailwind)
2. Create project structure:
   - Components (Layout, Charts, Metrics, UI)
   - Pages (8 pages)
   - Services (API client)
   - Hooks (custom hooks)
3. Build Layout:
   - Navbar with navigation
   - Sidebar with page links
   - Responsive design
4. Build Overview page:
   - Metric cards
   - Key metrics table
5. Build Trends page:
   - Line chart (monthly orders)
   - Bar chart (monthly revenue)
6. Build Geospatial page:
   - Map chart (orders by state)
   - Bar chart (delivery by state)
7. Build Customers page:
   - Pie chart (RFM segments)
   - Bar chart (top customers)
8. Build Products page:
   - Bar chart (category performance)
   - Table (category details)
9. Build Delivery page:
   - Metric card (on-time rate)
   - Bar chart (status distribution)
10. Build Quality page:
    - Metric card (quality score)
    - Table (quality issues)
11. Build Performance page:
    - Bar chart (benchmark results)
    - Table (detailed metrics)
12. Build Data Dictionary page:
    - Table (schema documentation)
13. Test all pages
14. Fix responsive design issues

**Deliverables**:
- Complete React frontend
- 8 functional pages
- All charts and maps working
- API integration complete
- Responsive design

**Learning Objectives**:
- React framework
- Component-based architecture
- State management with hooks
- API integration with Axios
- Chart libraries (Recharts)
- Map libraries (React-Leaflet)
- Responsive design with Tailwind

---

### Day 7: Documentation & Demo Prep

**Goals**:
- Complete all documentation
- Prepare presentation slides
- Practice demo
- Final testing

**Tasks**:
1. Write `README.md`:
   - Project overview
   - Tech stack
   - Setup instructions
   - How to run pipeline
   - How to run API
   - How to run frontend
2. Write `docs/ARCHITECTURE.md`:
   - Detailed architecture
   - Design decisions
   - Technology choices
3. Write `docs/API_DOCUMENTATION.md`:
   - All endpoints
   - Request/response examples
   - Error codes
4. Write `docs/DEPLOYMENT.md`:
   - Step-by-step run instructions
   - Common issues & solutions
   - Environment setup
5. Write `docs/PRESENTATION.md`:
   - Slide outline
   - Key talking points
   - Demo script
6. Write `docs/DEMO_SCRIPT.md`:
   - Step-by-step demo
   - What to show
   - What to explain
7. Create `.gitignore`
8. Full end-to-end test:
   - Run pipeline
   - Start API
   - Start frontend
   - Test all pages
9. Take screenshots for documentation
10. Practice demo presentation

**Deliverables**:
- Complete documentation
- Presentation outline
- Demo script
- Screenshots
- Ready for submission

**Learning Objectives**:
- Technical writing
- Presentation skills
- Demo preparation
- Documentation best practices

---

## Key Design Decisions

### Why FastAPI Over Flask?

| Factor | FastAPI | Flask |
|--------|---------|-------|
| **Performance** | Faster (async) | Slower (sync) |
| **Type Safety** | Built-in (Pydantic) | Manual |
| **Documentation** | Auto-generated | Manual |
| **Modern** | Yes | Traditional |
| **Learning Curve** | Easy | Easy |

**Decision**: FastAPI for performance and automatic documentation.

### Why React Over Vue/Angular?

| Factor | React | Vue | Angular |
|--------|-------|-----|---------|
| **Industry Use** | Highest | Medium | Medium |
| **Ecosystem** | Largest | Good | Good |
| **Job Market** | Best | Good | Good |
| **Learning Curve** | Medium | Easy | Hard |
| **Flexibility** | High | High | Low |

**Decision**: React for industry adoption and job market.

### Why Parquet Over CSV?

| Factor | Parquet | CSV |
|--------|---------|-----|
| **Size** | 10x smaller | Large |
| **Read Speed** | Faster (columnar) | Slower |
| **Schema** | Preserved | None |
| **Compression** | Built-in | None |

**Decision**: Parquet for efficiency and schema preservation.

### Why Medallion Architecture?

- **Debugging**: Can trace issues back to source
- **Reproducibility**: Immutable bronze layer
- **Performance**: Gold layer pre-computed
- **Industry Standard**: Used by Databricks, Uber, Netflix

---

## Success Criteria

### Must-Have (Tier 1)
1. ✅ Complete pipeline (Bronze → Silver → Gold)
2. ✅ All 10 metrics computed correctly
3. ✅ FastAPI backend with all endpoints
4. ✅ React frontend with 8 pages
5. ✅ Data quality framework
6. ✅ Performance benchmarking
7. ✅ RFM customer segmentation
8. ✅ Geospatial analysis with maps
9. ✅ Complete documentation
10. ✅ Working end-to-end demo

### Nice-to-Have (Tier 2)
11. ✅ Automated profiling report
12. ✅ Pipeline performance monitoring
13. ✅ Regional comparison analysis
14. ✅ Seller performance analytics
15. ✅ Responsive design optimization

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Java/PySpark setup issues | Medium | High | Address Day 1, document fixes |
| React learning curve | Medium | Medium | Use Vite for fast setup, follow tutorials |
| API integration issues | Low | Medium | Test endpoints early, use Postman |
| Time constraints | Medium | High | Prioritize Tier 1 features |
| Data quality issues | Low | Medium | Add quality checks early |
| Chart library complexity | Low | Low | Use Recharts (simple API) |

---

## What Makes This Project Unique?

### For College Presentation
- 🎯 **Full-Stack**: Backend (PySpark + FastAPI) + Frontend (React)
- 🎯 **Modern Tech**: FastAPI, React, Vite, Tailwind
- 🎯 **Advanced Analytics**: RFM segmentation, geospatial analysis
- 🎯 **Production-Ready**: Data quality, benchmarking, monitoring
- 🎯 **Professional**: Complete documentation, API docs, deployment guide

### For Interviews
- 🎯 **Differentiation**: Most candidates don't have full-stack + big data
- 🎯 **Evidence**: Benchmarking proves technical understanding
- 🎯 **Completeness**: End-to-end with quality, not just ETL
- 🎯 **Communication**: Can explain architecture and decisions
- 🎯 **Versatility**: Shows both data engineering and software engineering skills

---

## Next Steps

**Ready to start Day 1?**

Day 1 includes:
1. Fixing Java PATH issue
2. Exploring all 9 CSV files
3. Documenting schemas in DATA_DICTIONARY.md
4. Generating profiling report
5. Setting up complete project structure
6. Installing all dependencies

This will take approximately 4-6 hours.

**Shall we begin?**
