# Google Colab Execution Guide

## Overview

CommercePulse is designed to run in Google Colab to leverage PySpark's distributed processing capabilities in a cloud environment. This avoids Windows Hadoop compatibility issues and provides access to free GPU resources.

## Prerequisites

- Google account
- Web browser
- Project files from the repository

## Step-by-Step Setup

### 1. Open Google Colab

1. Go to [colab.research.google.com](https://colab.research.google.com/)
2. Click "New Notebook"
3. Name it: `CommercePulse_Pipeline.ipynb`

### 2. Upload Project Files

You have two options:

#### Option A: Upload to Google Drive (Recommended)

1. Upload the entire project folder to your Google Drive
2. Mount your Drive in Colab (see Step 3)

#### Option B: Upload Directly to Colab

1. In Colab, click the folder icon in the left sidebar
2. Click "Upload to session storage"
3. Upload the following:
   - `src/` folder (complete)
   - `data/raw/` folder (with all CSV files)
   - `requirements.txt`

### 3. Mount Google Drive (if using Option A)

Add this cell to your Colab notebook:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Run the cell and follow the authentication prompts.

### 4. Set Up Project Path

Add this cell to your Colab notebook:

```python
import os
import sys
from pathlib import Path

# If using Google Drive
PROJECT_ROOT = Path('/content/drive/MyDrive/BDA Project')

# If using direct upload
# PROJECT_ROOT = Path('/content')

# Set environment variable for config
os.environ['COMMERCE_PULSE_ROOT'] = str(PROJECT_ROOT)

# Add src to Python path
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

print(f"Project root: {PROJECT_ROOT}")
print(f"Data exists: {(PROJECT_ROOT / 'data' / 'raw').exists()}")
```

### 5. Install Dependencies

Add this cell:

```python
!pip install -q pyspark pandas pyarrow
```

### 6. Run Bronze Layer Ingestion

Add this cell:

```python
from commerce_pulse.ingestion import main

# Run the bronze layer ingestion
main()
```

This will:
- Read all CSV files from `data/raw/`
- Convert them to Parquet in `data/bronze/`
- Generate quality reports in `data/quality/`
- Track metadata in `data/bronze/metadata.json`

### 7. Verify Results

Add this cell:

```python
import json
from pathlib import Path

# Check bronze data
bronze_dir = PROJECT_ROOT / 'data' / 'bronze'
print(f"Bronze files: {list(bronze_dir.glob('*.parquet'))}")

# Check quality report
quality_file = PROJECT_ROOT / 'data' / 'quality' / 'quality_report.json'
with open(quality_file, 'r') as f:
    quality_report = json.load(f)

print(f"\nAverage quality score: {quality_report['average_quality_score']}")
print(f"Tables processed: {quality_report['total_tables']}")
```

## Running Silver and Gold Layers

Once Bronze layer is complete, you can proceed with Silver and Gold layers (to be implemented):

```python
# Silver layer (will be implemented)
# from commerce_pulse.cleaning import main as silver_main
# silver_main()

# Gold layer (will be implemented)
# from commerce_pulse.analytics import main as gold_main
# gold_main()
```

## Colab-Specific Tips

### Enable GPU

1. Click "Runtime" in the menu
2. Click "Change runtime type"
3. Select "GPU" under "Hardware accelerator"
4. Click "Save"

### Check Resources

```python
# Check GPU availability
import torch
print(f"GPU available: {torch.cuda.is_available()}")

# Check memory
!df -h
```

### Save Results to Drive

After processing, you can save results back to Drive:

```python
# Copy results to Drive (if not already there)
import shutil
shutil.copytree(PROJECT_ROOT / 'data', '/content/drive/MyDrive/CommercePulse_Results')
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Make sure you've added the `src` directory to Python path (Step 4)

### Issue: File not found

**Solution**: Verify `PROJECT_ROOT` is set correctly and files exist

```python
# Verify paths
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"Raw data exists: {(PROJECT_ROOT / 'data' / 'raw').exists()}")
print(f"CSV files: {list((PROJECT_ROOT / 'data' / 'raw').glob('*.csv'))}")
```

### Issue: Out of memory

**Solution**:
1. Reduce Spark memory in `config.py`
2. Process tables one at a time instead of all at once
3. Use Colab's High-RAM runtime (if available)

## Next Steps

After Bronze layer is complete:
1. Implement Silver layer (cleaning and joining)
2. Implement Gold layer (analytics and metrics)
3. Create Streamlit dashboard
4. Run performance benchmarks

## Advantages of Colab Execution

- ✅ No Windows Hadoop compatibility issues
- ✅ Free GPU access
- ✅ Cloud-based (industry standard)
- ✅ Easy sharing and collaboration
- ✅ Pre-installed Python environment
- ✅ Professional demo capability

## Portability

The codebase is designed to work in multiple environments:
- Google Colab (cloud)
- Databricks (cloud)
- Local Linux/WSL2
- Local Mac (with proper Hadoop setup)

Only the `PROJECT_ROOT` path needs to be configured via environment variable.
