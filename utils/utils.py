import pandas as pd

# Re-create the resampling function
def resample_ohlcv(timestamps, open_col, high_col, low_col, close_col, volume_col, timeframe):
    """
    Resample OHLCV data to the desired timeframe.
    
    Parameters:
    - timestamps: Series or list containing the datetime timestamps.
    - open_col: Series or list containing the Open prices.
    - high_col: Series or list containing the High prices.
    - low_col: Series or list containing the Low prices.
    - close_col: Series or list containing the Close prices.
    - volume_col: Series or list containing the Volume data.
    - timeframe: string representing the desired timeframe (e.g., '5T', '15T', '30T', '1H', '4H', 'D').
    
    Returns:
    - DataFrame containing the resampled OHLCV data.

    Example:
    # Re-load the dataset
    dataset = pd.read_excel("./Data/HISTDATA_COM_XLSX_EURUSD_M12020/DAT_XLSX_EURUSD_M1_2020.xlsx")

    # Test the function with a 5-minute timeframe
    test_resampled = resample_ohlcv(dataset[dataset.columns[0]], 
                                    dataset[dataset.columns[1]], 
                                    dataset[dataset.columns[2]], 
                                    dataset[dataset.columns[3]], 
                                    dataset[dataset.columns[4]], 
                                    [0]*len(dataset),  # Since volume is always 0
                                    '5T')
    print(test_resampled.head())
    """
    
    # Create a DataFrame from the provided data
    data = pd.DataFrame({
        'Timestamp': timestamps,
        'Open': open_col,
        'High': high_col,
        'Low': low_col,
        'Close': close_col,
        'Volume': volume_col
    })
    
    # Set the Timestamp column as the index
    data.set_index('Timestamp', inplace=True)
    
    # Resample the data to the desired timeframe
    resampled_data = data.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    })
    
    # Drop any rows with NaN values (this can happen if there are gaps in the data)
    resampled_data = resampled_data.dropna()
    
    return resampled_data
