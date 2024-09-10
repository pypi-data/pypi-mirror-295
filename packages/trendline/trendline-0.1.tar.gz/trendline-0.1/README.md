# Trendline

`trendline` is a Python library for calculating trendlines for financial data. It provides functions to analyze trends in multiple assets or a single asset.

## Installation

You can install the `trendline` library using pip:

```bash
pip install trendline
```

## Usage

### Importing the Library

To use the library, first import the necessary functions:

```python
from trendline import calculate_trendlines_multiple, calculate_trendline_single
```


### Calculating Trendlines for a Single Asset
For analyzing a single asset, use the calculate_trendline_single function. This function calculates trendlines for the provided DataFrame.

Parameters:
- dataframe (DataFrame): A DataFrame containing financial data for a single asset.
- num_chunks (int, optional): Number of chunks to divide residuals into (default is 5).
- residual_percentile (int, optional): Percentile for calculating residual cutoffs (default is 10).

Returns:
A dictionary containing trendline data for the single asset, including:
- 'support_line_gradient': Gradient of the support (low) trendline.
- 'resistance_line_gradient': Gradient of the resistance (high) trendline.
- 'support_line_start': First value of the support (low) trendline.
- 'support_line_end': Last value of the support (low) trendline.
- 'resistance_line_start': First value of the resistance (high) trendline.
- 'resistance_line_end': Last value of the resistance (high) trendline.

Example
```python
import pandas as pd
from trendline import calculate_trendline_single

# Example data
df = pd.DataFrame({
    'Open': [1, 2, 3, 4, 5],
    'High': [1.5, 2.5, 3.5, 4.5, 5.5],
    'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
    'Close': [1.2, 2.2, 3.2, 4.2, 5.2],
})

result = calculate_trendline_single(df)
print(result)
```


### Calculating Trendlines for Multiple Assets
If you have data for multiple assets, use the calculate_trendlines_multiple function. This function calculates trendlines for each asset in a dictionary of DataFrames.

Parameters:
- dataframes (dict): Dictionary where keys are asset identifiers and values are DataFrames containing financial data for each asset.
- num_chunks (int, optional): Number of chunks to divide residuals into (default is 5).
- residual_percentile (int, optional): Percentile for calculating residual cutoffs (default is 10).

Returns:
A dictionary where keys are asset identifiers and values are dictionaries containing trendline data for each asset, including:
- 'support_line_gradient': Gradient of the support (low) trendline.
- 'resistance_line_gradient': Gradient of the resistance (high) trendline.
- 'support_line_start': First value of the support (low) trendline.
- 'support_line_end': Last value of the support (low) trendline.
- 'resistance_line_start': First value of the resistance (high) trendline.
- 'resistance_line_end': Last value of the resistance (high) trendline.

Example
```python
import pandas as pd
from trendline import calculate_trendlines_multiple

# Example data for multiple assets
data = {
    'asset1': pd.DataFrame({
        'Open': [1, 2, 3, 4, 5],
        'High': [1.5, 2.5, 3.5, 4.5, 5.5],
        'Low': [0.5, 1.5, 2.5, 3.5, 4.5],
        'Close': [1.2, 2.2, 3.2, 4.2, 5.2],
    }),
    'asset2': pd.DataFrame({
        'Open': [2, 3, 4, 5, 6],
        'High': [2.5, 3.5, 4.5, 5.5, 6.5],
        'Low': [1.5, 2.5, 3.5, 4.5, 5.5],
        'Close': [2.2, 3.2, 4.2, 5.2, 6.2],
    })}
        
results = calculate_trendlines_multiple(data)
print(results)
```





