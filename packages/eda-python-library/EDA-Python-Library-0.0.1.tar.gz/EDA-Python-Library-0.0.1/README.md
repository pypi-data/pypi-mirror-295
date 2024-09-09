# Preprocessing Pipeline

## Overview

The **Preprocessing Pipeline** is a comprehensive Python-based tool designed to facilitate the preprocessing of data by performing initial data inspection, handling missing values, converting data types, managing outliers, scaling data, and transforming variables. This tool is modular, customizable, and suited for various data cleaning and preprocessing tasks essential for machine learning and data analysis.

## Table of Contents

- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Initial Data Inspection](#initial-data-inspection)
  - [Handling Missing Values](#handling-missing-values)
  - [Data Type Conversion](#data-type-conversion)
  - [Outlier Handling](#outlier-handling)
  - [Scaling Data](#scaling-data)
  - [Variable Transformation](#variable-transformation)
- [Classes and Methods](#classes-and-methods)
- [Report Generation](#report-generation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Data preprocessing is a crucial step in any data analysis or machine learning pipeline. This preprocessing tool provides a systematic approach to cleaning and preparing data by offering modules for inspecting data, handling missing values, managing outliers, scaling numerical features, and transforming variables to improve data quality and model performance.

## Problem Statement

Handling raw data can be challenging due to missing values, inconsistent data types, outliers, and other issues that can degrade the performance of predictive models. This tool/library/package aims to streamline the preprocessing workflow, making it easier to clean and prepare data for further analysis.

## Features

- **Initial Inspection**: Provides insights into the dataset, including shape, size, summary statistics, and detailed analysis of missing and duplicated values.
- **Data Type Conversion**: Converts data types like objects to strings, integers, floats, and datetime, ensuring data consistency.
- **Missing Value Handling**: Offers multiple strategies to fill or remove missing values, including mean, median, mode, bfill, linear, and polynomial interpolation.
- **Outlier Handling**: Detects and caps outliers using IQR and Z-score methods.
- **Scaling**: Standardizes numerical data using Standard Scaler, Robust Scaler, and Normalizer techniques.
- **Variable Transformation**: Provides transformations like binning, log transformation, square root transformation, label encoding, and one-hot encoding.

## Installation

Clone this repository to your local machine and ensure you have Python installed along with the required dependencies:

```bash
git clone https://github.com/KaRtHiK-56/EDA_python_package_library
cd preprocessing-pipeline
pip install -r requirements.txt
```

## Usage

### Initial Data Inspection

The inspection methods provide a detailed overview of your dataset to identify data quality issues upfront.

```python
# Import the InitialInspection class and create an instance with your DataFrame
from preprocessing import InitialInspection

# Sample DataFrame
import pandas as pd

data = {
    'col1': [1, 2, np.nan, 4],
    'col2': ['A', 'B', 'A', 'B'],
    'col3': [pd.Timestamp('20220101'), pd.Timestamp('20220102'), pd.Timestamp('20220103'), pd.Timestamp('20220104')]
}

df = pd.DataFrame(data)

# Create an instance of Inspection
Inspection.inspect()
```

### Handling Missing Values

Handle missing values using different strategies like mean, median, mode, bfill, etc.

```python
# Import and use the MissingValueHandler class
from preprocessing import MissingValueHandler

MissingValueHandler.mean('col1')
MissingValueHandler.bfill('col3')
```

### Data Type Conversion

Convert data types using the `DataTypeConverter` class, which supports conversions between object, string, integer, float, and datetime.

```python
# Import and use the DataTypeConverter class
from preprocessing import DataTypeConverter

converter = DataTypeConverter(df)
converter.to_string('col2')
converter.to_datetime('col3')
```

### Outlier Handling

Handle outliers using IQR and Z-score methods.

```python
# Import and use the OutlierHandler class
from preprocessing import OutlierHandler

OutlierHandler.iqr_capping('col1')
```

### Scaling Data

Scale numerical data using Standard Scaler, Robust Scaler, or Normalizer.

```python
# Import and use the ScalingHandler class
from preprocessing import NumericalScaler

NumericalScaler.standard_scaler('col1')
```

### Variable Transformation

Transform variables using binning, log transformation, and encoding methods.

```python
# Import and use the VariableTransformation class
from preprocessing import VariableTransformation

VariableTransformation.binner('col1', bins=[0, 1, 2, 3, 4])
VariableTransformation.label_encoding('col2')
```

## Classes and Methods

### 1. `InitialInspection`
- **Methods**: 
  - `inspect()`: Generates a comprehensive inspection report on dataset shape, size, dimensions, summary, missing values, duplicates, numerical and categorical columns, skewness, and kurtosis.

### 2. `MissingValueHandler`
- **Methods**:
  - `mean()`, `median()`, `mode()`, `bfill()`, `ffill()` ,`linear()`, `polynomial()`, `drop()`: Various techniques to handle missing values in the dataset.

### 3. `DataTypeConverter`
- **Methods**:
  - `to_string()`, `to_int()`, `to_float()`, `to_datetime()`: Convert data types of specific columns.

### 4. `OutlierHandler`
- **Methods**:
  - `iqr_capping()`, `zscore_capping()`: Detect and handle outliers using IQR and Z-score methods.

### 5. `ScalingHandler`
- **Methods**:
  - `standardscaler()`, `robustscaler()`: Scale numerical data using different scaling techniques.

### 6. `VariableTransformation`
- **Methods**:
  - `binning()`, `log_transformer()`, `sqrt_transformer()`, `label_encoding()`, `one_hot_encoding()`: Various transformations for numerical and categorical data.

## Report Generation

The `Inspection` class provides a detailed report summarizing the data, including counts and percentages of missing and duplicated values, column types, and descriptive statistics.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
