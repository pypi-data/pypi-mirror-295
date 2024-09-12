# FeatureRefiner
# <img src="FeatureRefiner/scripts/logo.jpeg" alt="FeatureRefiner logo" width="200"/>

![PyPI](https://img.shields.io/pypi/v/FeatureRefiner?color=blue&label=pypi&logo=pypi)
![License](https://img.shields.io/github/license/ambilynanjilath/FeatureRefiner)
![Python Versions](https://img.shields.io/pypi/pyversions/FeatureRefiner)

FeatureRefiner is a Python package for feature engineering that provides a set of tools for data transformation, imputation, encoding, scaling, and feature creation. This package comes with an interactive Streamlit interface that allows users to easily apply these transformations to their datasets.

## Features

- Create polynomial features
- Handle and extract date-time features
- Encode categorical data using various encoding techniques
- Impute missing values with different strategies
- Normalize and scale data using multiple scaling methods
- Interactive Streamlit interface for easy usage

## Installation

It's recommended to install `FeatureRefiner` in a virtual environment to manage dependencies effectively and avoid conflicts with other projects.

### 1. Set Up a Virtual Environment

**For Python 3.3 and above:**

1. **Create a Virtual Environment:**

    ```bash
    python -m venv env
    ```

    Replace `env` with your preferred name for the virtual environment.

2. **Activate the Virtual Environment:**

    - **On Windows:**
      ```bash
      env\Scripts\activate
      ```

    - **On macOS/Linux:**
      ```bash
      source env/bin/activate
      ```

### 2. Install FeatureRefiner

Once the virtual environment is activated, you can install `FeatureRefiner` using `pip`:

```bash
pip install FeatureRefiner
```

## Quick Start
After installing the package, run the FeatureRefiner interface using:

```bash
run-FeatureRefiner
```
This will open a Streamlit app where you can upload your dataset and start applying transformations.

## Usage

### Command-Line Interface
To launch the Streamlit app, simply use the command:
```bash
run-FeatureRefiner
```
### Importing Modules in Python
You can also use FeatureRefiner modules directly in your Python scripts:
```bash
from FeatureRefiner.imputation import MissingValueImputation
from FeatureRefiner.encoding import FeatureEncoding
from FeatureRefiner.imputation import MissingValueImputation
from FeatureRefiner.encoding import FeatureEncoding
from FeatureRefiner.scaling import DataNormalize
from FeatureRefiner.date_time_features import DateTimeExtractor
from FeatureRefiner.create_features import PolynomialFeaturesTransformer
```

## Modules Overview

The `FeatureRefiner` package provides several modules for different data transformation tasks:

- **create_features.py** - Generate polynomial features.
- **date_time_features.py** - Extract and handle date-time related features.
- **encoding.py** - Encode categorical features using techniques like Label Encoding and One-Hot Encoding.
- **imputation.py** - Handle missing values with multiple imputation strategies.
- **scaling.py** - Normalize and scale numerical features.

Each of these modules is described in detail below.

### 1. `create_features.py`
The `create_features.py` module provides functionality to generate polynomial features from numeric columns in a pandas DataFrame. The `PolynomialFeaturesTransformer` class supports creating polynomial combinations of the input features up to a specified degree, enhancing the feature set for predictive modeling.

#### Key Features
- **Degree Specification:** Allows setting the degree of polynomial features during initialization or transformation.
- **Numeric Column Filtering:** Automatically filters and processes only the numeric columns in the DataFrame.
- **Error Handling:** Provides robust error handling for invalid inputs, including non-numeric data and improper degree values.

#### Supported Transformations
- **Polynomial Feature Creation:** Generates polynomial combinations of input features based on the specified degree.


#### Example Usage:
```python
from FeatureRefiner.create_features import PolynomialFeaturesTransformer
import pandas as pd

# Example DataFrame
data = {'feature1': [1, 2, 3], 'feature2': [4, 5, 6]}
df = pd.DataFrame(data)

# Initialize the PolynomialFeaturesTransformer object
transformer = PolynomialFeaturesTransformer(degree=2)

# Transform the DataFrame to include polynomial features
transformed_df = transformer.fit_transform(df)

print(transformed_df)
```
#### Methods


- **`__init__(degree)`**: Initializes the transformer with the specified degree of polynomial features.

- **`fit_transform(df, degree=None)`**: Fits the transformer to the numeric columns of the DataFrame and generates polynomial features. Optionally, updates the polynomial degree.

- **`_validate_input(df)`**: Validates the input DataFrame, ensuring it contains only numeric columns and no categorical data.

### 2. `date_time_features.py`

The `date_time_features.py` module provides functionality to extract and parse datetime components from a specified column in a pandas DataFrame. The `DateTimeExtractor` class supports extracting year, month, day, and day of the week from a datetime column.

#### Key Features
- **Date Parsing:** Handles multiple date formats for parsing datetime data.
- **Component Extraction:** Extracts year, month, day, and day of the week from a datetime column.

#### Supported Extractors
- **Year Extraction:** Adds a new column `year` with the extracted year.
- **Month Extraction:** Adds a new column `month` with the extracted month.
- **Day Extraction:** Adds a new column `day` with the extracted day.
- **Day of Week Extraction:** Adds a new column `day_of_week` with the extracted day of the week.

#### Example Usage
```python
from FeatureRefiner.date_time_features import DateTimeExtractor
import pandas as pd

# Example DataFrame
data = {'date': ['2024-01-01', '2024-02-14', '2024-03-21']}
df = pd.DataFrame(data)

# Initialize the DateTimeExtractor object
extractor = DateTimeExtractor(df, datetime_col='date')

# Extract all datetime components
result_df = extractor.extract_all()

print(result_df)
```
#### Methods

- **`_parse_date(date_str)`**: Tries to parse a date string using multiple formats.

- **`extract_year()`**: Extracts the year from the datetime column and adds it as a new column named `year`.

- **`extract_month()`**: Extracts the month from the datetime column and adds it as a new column named `month`.

- **`extract_day()`**: Extracts the day from the datetime column and adds it as a new column named `day`.

- **`extract_day_of_week()`**: Extracts the day of the week from the datetime column and adds it as a new column named `day_of_week`.

- **`extract_all()`**: Extracts year, month, day, and day of the week from the datetime column and adds them as new columns.

### 3. `encoding.py`
The `encoding.py` module provides functionality to encode categorical features in a pandas DataFrame using Label Encoding and One-Hot Encoding. The `FeatureEncoding` class in this module offers methods for converting categorical data into a numerical format suitable for machine learning algorithms.

#### Key Features:
- **Label Encoding**: Converts categorical text data into numerical data by assigning a unique integer to each category.
- **One-Hot Encoding**: Converts categorical data into a binary matrix, creating a new column for each unique category.

#### Supported Encoders:
- **LabelEncoder**: Converts each category to a unique integer.
- **OneHotEncoder**: Converts categorical data into a binary matrix, with an option to drop the first category to avoid multicollinearity.

#### Example Usage:
```python
from FeatureRefiner.encoding import FeatureEncoding
import pandas as pd

# Example DataFrame
data = {'Color': ['Red', 'Blue', 'Green'], 'Size': ['S', 'M', 'L']}
df = pd.DataFrame(data)

# Initialize the FeatureEncoding object
encoder = FeatureEncoding(df)

# Apply Label Encoding
df_label_encoded = encoder.label_encode(['Color'])

# Apply One-Hot Encoding
df_one_hot_encoded = encoder.one_hot_encode(['Size'])

print(df_label_encoded)
print(df_one_hot_encoded)
```
#### Methods:
- **`label_encode(columns: list) -> pd.DataFrame`**: Apply Label Encoding to the specified columns.
- **`one_hot_encode(columns: list) -> pd.DataFrame`**: Apply One-Hot Encoding to the specified columns, concatenate the encoded columns with the original DataFrame, and drop the original columns.

### 4. `imputation.py`
The `imputation.py` module provides functionality for handling missing values in a pandas DataFrame using various imputation strategies. The `MissingValueImputation` class in this module offers methods to fill missing values based on the specified strategies.

#### Key Features:
- **Flexible Imputation**: Allows for multiple imputation strategies such as mean, median, mode, or custom values.
- **Column-Specific Strategies**: Supports different strategies for different columns.
- **Fit and Transform**: Includes methods for fitting the imputation model and transforming data in a single step.

#### Supported Strategies:
- **Mean**: Fills missing values with the mean of the column (only applicable to numeric columns).
- **Median**: Fills missing values with the median of the column (only applicable to numeric columns).
- **Mode**: Fills missing values with the mode of the column.
- **Custom Values**: Allows specifying a custom value for imputation.

#### Example Usage:

```python
from FeatureRefiner.imputation import MissingValueImputation
import pandas as pd

# Example DataFrame
data = {'A': [1, 2, np.nan, 4, 5], 'B': [10, np.nan, 30, np.nan, 50]}
df = pd.DataFrame(data)

# Define imputation strategies
strategies = {
    'A': 'mean',
    'B': 25
}

# Initialize the MissingValueImputation object
imputer = MissingValueImputation(strategies=strategies)

# Fit and transform the DataFrame
imputed_df = imputer.fit_transform(df)

print(imputed_df)
```
#### Methods:
- **`_compute_fill_value(df: pd.DataFrame, column: str, strategy: Union[str, int, float]) -> Union[float, str]`**: Computes the fill value based on the imputation strategy for a given column.
- **`fit(df: pd.DataFrame) -> 'MissingValueImputation'`**: Computes the fill values for missing data based on the provided strategies.
- **`transform(df: pd.DataFrame) -> pd.DataFrame`**: Applies the imputation to the DataFrame using the computed fill values.
- **`fit_transform(df: pd.DataFrame) -> pd.DataFrame`**: Computes the fill values and applies the imputation to the DataFrame in one step.

### 5. `scaling.py`
The `scaling.py` module provides functionality to scale and normalize numerical data in a pandas DataFrame using various scaling techniques from `scikit-learn`. The `DataNormalize` class in this module offers methods for scaling data using different techniques provided by `scikit-learn`. It supports several scalers, such as `StandardScaler`, `MinMaxScaler`, `RobustScaler`, and others.

#### Key Features:
- **General Data Scaling**: Scales all numerical columns in the DataFrame.
- **Column-Specific Scaling**: Allows scaling specific columns within the DataFrame.
- **Multiple Scalers Supported**: Supports different scaling methods such as standardization, normalization, robust scaling, and more.

#### Supported Scalers:
- **StandardScaler** (`standard`): Scales data to have zero mean and unit variance.
- **MinMaxScaler** (`minmax`): Scales data to a specified range (default is 0 to 1).
- **RobustScaler** (`robust`): Scales data using statistics that are robust to outliers.
- **MaxAbsScaler** (`maxabs`): Scales data to the range [-1, 1] based on the maximum absolute value.
- **Normalizer** (`l2`): Scales each sample individually to have unit norm (L2 norm).
- **QuantileTransformer** (`quantile`): Transforms features to follow a uniform or normal distribution.
- **PowerTransformer** (`power`): Applies a power transformation to make data more Gaussian-like.

#### Example Usage:

```python
from FeatureRefiner.scaling import DataNormalize
import pandas as pd

# Example DataFrame
data = {'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# Initialize the DataNormalize object
scaler = DataNormalize()

# Scale the entire DataFrame using MinMaxScaler
scaled_df = scaler.scale(df, method='minmax')

print(scaled_df)
```
#### Methods:
- **`scale(df: pd.DataFrame, method: str = 'standard') -> pd.DataFrame`**: Scales the entire DataFrame using the specified method.
- **`scale_columns(df: pd.DataFrame, columns: list, method: str = 'standard') -> pd.DataFrame`**: Scales specific columns of the DataFrame using the specified method.


## Requirements

Before installing, please make sure you have the following packages installed:

- Python >= 3.7
- Streamlit
- Pandas
- NumPy
- scikit-learn
- st-aggrid

For more detailed information, see the `requirements.txt` file.

## Contributing

We welcome contributions! Please read our Contributing Guidelines for more details.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

Special thanks to all the libraries and frameworks that have helped in developing this package, including:

- [Streamlit](https://www.streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [scikit-learn](https://scikit-learn.org/stable/)


