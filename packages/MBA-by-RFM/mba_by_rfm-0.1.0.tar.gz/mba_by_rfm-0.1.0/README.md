# RFM Market Basket Analysis

## Overview

The `MBA-by-RFM` package provides comprehensive tools for performing **RFM analysis** and generating **market basket analysis** using Apriori, FP-Growth, and ECLAT algorithms. It also includes powerful data visualizations such as network graphs, heatmaps, and RFM segment distribution charts.

## Features

- **RFM Analysis**: Segment customers based on Recency, Frequency, and Monetary values.
- **Market Basket Analysis**: Generate association rules using Apriori, FP-Growth, and ECLAT algorithms.
- **Data Visualization**: Plot association rules as heatmaps, network diagrams, and RFM segments charts.

## Installation

You can install the package directly from PyPI using `pip`:

## Usage
Import the Main Function:
The main analysis workflow can be executed by importing the main function:
```bash
from rfm_market_basket_analysis.main import main
import pandas as pd

# Load your transactional dataset
df = pd.read_csv('transactions.csv')

# Run the main analysis
main(df)
```
