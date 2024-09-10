import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_trendlines_multiple(dataframes, num_chunks=3, residual_percentile=5):
    """
    Calculate trendlines for multiple assets.

    Parameters:
    - dataframes (dict): Dictionary where keys are asset identifiers and values are DataFrames containing financial data for each asset.
    - num_chunks (int, optional): Number of chunks to divide residuals into (default is 5).
    - residual_percentile (int, optional): Percentile for calculating residual cutoffs (default is 10).

    Returns:
    - dict: Dictionary where keys are asset identifiers and values are dictionaries containing trendline data:
      - 'resistance_line_gradient': Gradient of the resistance (high) trendline.
      - 'support_line_gradient': Gradient of the support (low) trendline.
      - 'resistance_line_start': First value of the resistance (high) trendline.
      - 'resistance_line_end': Last value of the resistance (high) trendline.
      - 'support_line_start': First value of the support (low) trendline.
      - 'support_line_end': Last value of the support (low) trendline.
    """
    trendlines_data = {}
    
    for asset_id, asset_data in dataframes.items():
        index_array = np.arange(len(asset_data))
        
        # Process the support (low) prices
        support_prices = asset_data['Low']
        X_support = index_array.reshape(-1, 1)

        # Perform linear regression on the support prices
        support_model = LinearRegression()
        support_model.fit(X_support, support_prices)
        support_predictions = support_model.predict(X_support)
        support_residuals = support_prices - support_predictions

        total_residuals = len(support_residuals)
        residuals_per_chunk = total_residuals // num_chunks

        support_residual_indices_list = []
        resistance_residual_indices_list = []

        # Process each chunk of residuals
        for chunk_index in range(num_chunks):
            start_idx = chunk_index * residuals_per_chunk
            end_idx = start_idx + residuals_per_chunk if chunk_index < num_chunks - 1 else total_residuals
            residuals_in_chunk = support_residuals.iloc[start_idx:end_idx]

            support_residual_cutoff = np.percentile(residuals_in_chunk, residual_percentile)
            resistance_residual_cutoff = np.percentile(residuals_in_chunk, 100 - residual_percentile)

            support_residual_indices = residuals_in_chunk[residuals_in_chunk <= support_residual_cutoff].index
            resistance_residual_indices = residuals_in_chunk[residuals_in_chunk >= resistance_residual_cutoff].index

            support_residual_indices_list.append(support_residual_indices)
            resistance_residual_indices_list.append(resistance_residual_indices)


        # Process the support trendline
        combined_support_residual_indices = pd.Index(np.concatenate(support_residual_indices_list))
        combined_resistance_residual_indices = pd.Index(np.concatenate(resistance_residual_indices_list))

        support_indices_selected = [asset_data.index.get_loc(idx) for idx in combined_support_residual_indices]
        support_selected_prices = asset_data['Low'].iloc[support_indices_selected]
        X_selected_support = np.array(support_indices_selected).reshape(-1, 1)
        support_trend_model = LinearRegression()
        support_trend_model.fit(X_selected_support, support_selected_prices)
        support_line_gradient = support_trend_model.coef_[0]

        support_line_start = support_trend_model.predict([[index_array[0]]])[0]
        support_line_end = support_trend_model.predict([[index_array[-1]]])[0]

        # Process the resistance trendline
        resistance_indices_selected = [asset_data.index.get_loc(idx) for idx in combined_resistance_residual_indices]
        resistance_selected_prices = asset_data['High'].iloc[resistance_indices_selected]
        X_selected_resistance = np.array(resistance_indices_selected).reshape(-1, 1)
        resistance_trend_model = LinearRegression()
        resistance_trend_model.fit(X_selected_resistance, resistance_selected_prices)
        resistance_line_gradient = resistance_trend_model.coef_[0]

        resistance_line_start = resistance_trend_model.predict([[index_array[0]]])[0]
        resistance_line_end = resistance_trend_model.predict([[index_array[-1]]])[0]

        # Store the results
        trendlines_data[asset_id] = {
            'resistance_line_gradient': resistance_line_gradient,
            'support_line_gradient': support_line_gradient,
            'resistance_line_start': resistance_line_start,
            'resistance_line_end': resistance_line_end,
            'support_line_start': support_line_start,
            'support_line_end': support_line_end,
        }
    
    return trendlines_data


def calculate_trendline_single(dataframe, num_chunks=3, residual_percentile=5):
    """
    Calculate trendlines for a single asset.

    Parameters:
    - dataframe (pd.DataFrame): A DataFrame containing financial data for the asset.
    - num_chunks (int, optional): Number of chunks to divide residuals into (default is 5).
    - residual_percentile (int, optional): Percentile for calculating residual cutoffs (default is 10).

    Returns:
    - dict: Dictionary containing trendline data:
      - 'resistance_line_gradient': Gradient of the resistance (high) trendline.
      - 'support_line_gradient': Gradient of the support (low) trendline.
      - 'resistance_line_start': First value of the resistance (high) trendline.
      - 'resistance_line_end': Last value of the resistance (high) trendline.
      - 'support_line_start': First value of the support (low) trendline.
      - 'support_line_end': Last value of the support (low) trendline.
    """
    # Select the data for the asset
    asset_data = dataframe
    index_array = np.arange(len(asset_data))
    
    # Process the support (low) prices
    support_prices = asset_data['Low']
    X_support = index_array.reshape(-1, 1)

    # Perform linear regression on the support prices
    support_model = LinearRegression()
    support_model.fit(X_support, support_prices)
    support_predictions = support_model.predict(X_support)
    support_residuals = support_prices - support_predictions

    total_residuals = len(support_residuals)
    residuals_per_chunk = total_residuals // num_chunks

    support_residual_indices_list = []
    resistance_residual_indices_list = []

    # Process each chunk of residuals
    for chunk_index in range(num_chunks):
        start_idx = chunk_index * residuals_per_chunk
        end_idx = start_idx + residuals_per_chunk if chunk_index < num_chunks - 1 else total_residuals
        residuals_in_chunk = support_residuals.iloc[start_idx:end_idx]

        support_residual_cutoff = np.percentile(residuals_in_chunk, residual_percentile)
        resistance_residual_cutoff = np.percentile(residuals_in_chunk, 100 - residual_percentile)

        support_residual_indices = residuals_in_chunk[residuals_in_chunk <= support_residual_cutoff].index
        resistance_residual_indices = residuals_in_chunk[residuals_in_chunk >= resistance_residual_cutoff].index

        support_residual_indices_list.append(support_residual_indices)
        resistance_residual_indices_list.append(resistance_residual_indices)


    # Process the support trendline
    combined_support_residual_indices = pd.Index(np.concatenate(support_residual_indices_list))
    combined_resistance_residual_indices = pd.Index(np.concatenate(resistance_residual_indices_list))

    support_indices_selected = [asset_data.index.get_loc(idx) for idx in combined_support_residual_indices]
    support_selected_prices = asset_data['Low'].iloc[support_indices_selected]
    X_selected_support = np.array(support_indices_selected).reshape(-1, 1)
    support_trend_model = LinearRegression()
    support_trend_model.fit(X_selected_support, support_selected_prices)
    support_line_gradient = support_trend_model.coef_[0]

    support_line_start = support_trend_model.predict([[index_array[0]]])[0]
    support_line_end = support_trend_model.predict([[index_array[-1]]])[0]

    # Process the resistance trendline
    resistance_indices_selected = [asset_data.index.get_loc(idx) for idx in combined_resistance_residual_indices]
    resistance_selected_prices = asset_data['High'].iloc[resistance_indices_selected]
    X_selected_resistance = np.array(resistance_indices_selected).reshape(-1, 1)
    resistance_trend_model = LinearRegression()
    resistance_trend_model.fit(X_selected_resistance, resistance_selected_prices)
    resistance_line_gradient = resistance_trend_model.coef_[0]

    resistance_line_start = resistance_trend_model.predict([[index_array[0]]])[0]
    resistance_line_end = resistance_trend_model.predict([[index_array[-1]]])[0]

    # Return the trendline data
    return {
        'resistance_line_gradient': resistance_line_gradient,
        'support_line_gradient': support_line_gradient,
        'resistance_line_start': resistance_line_start,
        'resistance_line_end': resistance_line_end,
        'support_line_start': support_line_start,
        'support_line_end': support_line_end,
    }
