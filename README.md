# Sales Data Analysis

An end-to-end analysis of a synthetic retail dataset using pandas and Matplotlib.

## Questions explored
- Which products generate the most revenue?
- How much revenue is recorded overall?
- What is the average transaction value?
- How does revenue change over time?

## Features
- Loads and validates a CSV file.
- Handles missing and invalid rows.
- Calculates key business metrics.
- Produces product and monthly summaries.
- Exports clean summary tables and a chart.

## Requirements
Python 3.10+.

## Setup and run
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
python analysis.py
```

## Tests
```bash
python -m unittest discover -s tests -v
```

## Outputs
The `output/` directory contains summary CSV files and a revenue chart.

## Data note
`data/sales.csv` is synthetic sample data created for this educational project. It does not represent a real company or customer dataset.

## Learning outcomes
Data cleaning, pandas, grouping and aggregation, date handling, descriptive statistics, charting, and communicating findings.
