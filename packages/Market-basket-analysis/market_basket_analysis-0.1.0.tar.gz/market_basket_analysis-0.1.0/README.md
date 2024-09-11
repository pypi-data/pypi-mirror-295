# Market Basket Analysis Package

This package provides tools for performing Market Basket Analysis (MBA), including generating frequent itemsets and association rules using algorithms like Apriori, FPGrowth, and Eclat. It also includes tools to visualize these rules using interactive graphs. This package simplifies tasks related to itemset mining and rule discovery in transactional datasets.

## Features

- Generate frequent itemsets using:
  - Apriori Algorithm
  - FPGrowth Algorithm
  - Eclat Algorithm (custom implementation)
- Create association rules based on various metrics such as support, confidence, and lift.
- Visualize association rules as interactive graphs using Plotly and NetworkX.

## Installation

1. **Install the package**:


2. **Install dependencies**:
    Install the required dependencies via `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install the package**:
    Once dependencies are installed, you can install the package:

    ```bash
    python setup.py install
    ```

## Usage

After installing, you can import the main analysis function using:

```python
from market_basket_analysis.market_basket_analysis import mba
