import pandas as pd
from pandas import DataFrame
import logging
from typing import Tuple, List, Dict
import numpy as np
import os
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_aggregation_rules(df: DataFrame, exclude_columns: List[str]) -> dict:
    """
    Determine aggregation rules for the DataFrame columns based on their data types.
    """
    return {col: ('mean' if df[col].dtype in [np.float64, np.int64] else 'first')
            for col in df.columns if col not in exclude_columns}


def allforfree_endpoint_split(df: pd.DataFrame, split_size: float, smiles_column: str,
                              endpoint_date_columns: Dict[str, str], aggregation: str, exclude_columns: List[str] = []) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Convert specified date columns to datetime objects
    for column in endpoint_date_columns.values():
        df[column] = pd.to_datetime(df[column], errors='coerce')

    # Create a temporary date column to determine the earliest date per compound
    df['tmp_date'] = df[list(endpoint_date_columns.values())].min(axis=1, skipna=True)
    
    # Group by SMILES column and find the minimum date per compound
    compound_dates = df.groupby(smiles_column)['tmp_date'].min().sort_values().reset_index()

    # Calculate split index for test set based on split size and sorted dates
    split_index = int(len(compound_dates) * split_size)
    all_test_compounds = set(compound_dates.iloc[:split_index][smiles_column])

    # Create initial splits based on 'tmp_date' column and test compounds
    df_test = df[df[smiles_column].isin(all_test_compounds)]
    df_train = df[~df[smiles_column].isin(all_test_compounds)]

    # Determine aggregation rules
    aggregation_rules = {col: 'mean' if df[col].dtype in [np.float64, np.int64] and col not in exclude_columns and col != smiles_column
                         else 'first' for col in df.columns if col not in ['tmp_date'] + list(endpoint_date_columns.values())}

    # Update aggregation rules based on any custom rules provided
    aggregation_rules.update(aggregation if isinstance(aggregation, dict) else {})

    # Group by SMILES and apply aggregation to finalize train and test DataFrames
    all_train_df = df_train.groupby(smiles_column, as_index=False).agg(aggregation_rules)
    all_test_df = df_test.groupby(smiles_column, as_index=False).agg(aggregation_rules)

    # remove temporary column
    df.drop(columns=['tmp_date'], inplace=True)

    return all_train_df, all_test_df


def allforfree_folds_endpoint_split(df: DataFrame, num_folds: int, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str], chemprop: bool, save_path: str, aggregation: str) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Process a DataFrame by splitting it into multiple train/test sets for cross-validation, with the training set growing progressively.
    
    Args:
        df: DataFrame to be processed.
        num_folds: Number of folds for cross-validation.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary of endpoint names to their respective date columns.
        exclude_columns: List of columns to exclude from aggregation rules.
        chemprop: Boolean to indicate if data is for chemprop.
        save_path: Path to save the resulting dataframes.
        aggregation: min or max

    Returns:
        List of tuples containing training and testing DataFrames for each fold.
    """
    if aggregation not in ['min', 'max', 'avg']:
        raise ValueError("Aggregation method must be 'min', 'max', or 'avg'.")
    cv_splits = []
    for fold in range(1, num_folds + 1):
        split_size = 1 - (fold / (num_folds + 1))  # Decrease the test size progressively
        
        train_df, test_df = allforfree_endpoint_split(df, split_size, smiles_column, endpoint_date_columns, aggregation, exclude_columns)

        if chemprop:
            # Exclude the smiles_column from feature_columns, it will be included in the targets
            feature_columns = [col for col in df.columns if col not in [smiles_column, *endpoint_date_columns.keys(), *endpoint_date_columns.values(), *exclude_columns]]
            train_features = extract_features(train_df, smiles_column, feature_columns)
            test_features = extract_features(test_df, smiles_column, feature_columns)

            # Include smiles_column in the targets
            train_targets = train_df[[smiles_column] + list(endpoint_date_columns.keys())]
            test_targets = test_df[[smiles_column] + list(endpoint_date_columns.keys())]

            # Save features and targets
            train_features.to_csv(os.path.join(save_path, f'train_features_fold{fold}.csv'), index=False)
            test_features.to_csv(os.path.join(save_path, f'test_features_fold{fold}.csv'), index=False)
            train_targets.to_csv(os.path.join(save_path, f'train_targets_fold{fold}.csv'), index=False)
            test_targets.to_csv(os.path.join(save_path, f'test_targets_fold{fold}.csv'), index=False)
        else:
            # Save the complete data frames when chemprop is not used
            train_df.to_csv(os.path.join(save_path, f'train_fold{fold}.csv'), index=False)
            test_df.to_csv(os.path.join(save_path, f'test_fold{fold}.csv'), index=False)

        cv_splits.append((train_df, test_df))

    return cv_splits


def leaky_endpoint_split(df: pd.DataFrame, split_size: float, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process a DataFrame by identifying test compounds and splitting the DataFrame based on the earliest date across multiple endpoints,
    each with its own date column. This method ensures consistent test set selection across different endpoints by converting all date columns
    to datetime format before aggregation.

    Args:
        df: DataFrame to be processed.
        split_size: Fraction of the DataFrame to include in the test set.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary mapping endpoint names to their respective date columns.
        exclude_columns: List of columns not to be included in the aggregation.

    Returns:
        Tuple containing the training and testing DataFrames.
    """
    
    # Convert all date columns to datetime
    for date_column in endpoint_date_columns.values():
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Create a new column for the earliest date across all endpoints
    df['earliest_date'] = df[list(endpoint_date_columns.values())].min(axis=1)
    
    # Filter out rows where the earliest date is null
    df_filtered = df[df['earliest_date'].notnull()]

    # Sorting data to pick the most recent entries as the test set
    df_sorted = df_filtered.sort_values(by='earliest_date', ascending=False)
    
    test_size = int(len(df_sorted) * split_size)
    test_indices = df_sorted.iloc[:test_size].index
    train_indices = df_sorted.iloc[test_size:].index
    
    # Create test and train dataframes
    test_df = df.loc[test_indices].copy()
    train_df = df.loc[train_indices].copy()

    # Define aggregation rules without earliest_date
    aggregation_rules = {col: 'mean' if df[col].dtype in [np.float64, np.int64] else 'first' for col in df.columns if col not in exclude_columns + ['earliest_date'] and col != smiles_column}
    
    # Drop the 'earliest_date' column before aggregation
    test_df.drop(columns=['earliest_date'], inplace=True)
    train_df.drop(columns=['earliest_date'], inplace=True)
    
    # Aggregation to ensure no duplicate SMILES in the sets
    all_train_df = train_df.groupby(smiles_column).agg(aggregation_rules).reset_index()
    all_test_df = test_df.groupby(smiles_column).agg(aggregation_rules).reset_index()

    return all_train_df, all_test_df


# ------------------------------------ #
# with chemprop compatibility          #
# ------------------------------------ #

def expand_df_to_endpoints(df: pd.DataFrame, endpoint_date_columns: Dict[str, str]) -> pd.DataFrame:
    """
    Transforms the DataFrame so that each row corresponds to a single endpoint,
    setting null for other endpoint values. Rows where all endpoint values are None are not included.
    It also removes any duplicate rows and rows where all endpoint values are None post transformation.
    
    Args:
        df: Original DataFrame.
        endpoint_date_columns: Dictionary mapping endpoint values to their respective date columns.
    
    Returns:
        DataFrame with expanded rows for each endpoint, maintaining NaN where data is missing,
        removing rows where all endpoints are None, and eliminating duplicates.
    """
    rows = []
    for idx, row in df.iterrows():
        if any(row[value_col] is not None for value_col in endpoint_date_columns.keys()):
            for value_col, date_col in endpoint_date_columns.items():
                new_row = {col: None for col in df.columns}  # Initialize all columns to None
                new_row.update(row)  # Update with original data

                # Reset other endpoints and their dates to None
                for vc, dc in endpoint_date_columns.items():
                    new_row[vc] = None
                    new_row[dc] = None

                new_row[value_col] = row[value_col]  # Set current endpoint
                new_row[date_col] = row[date_col]    # Set current endpoint's date

                rows.append(new_row)

    new_df = pd.DataFrame(rows)
    new_df = new_df.drop_duplicates().reset_index(drop=True)

    # Remove rows where all endpoint values are None
    endpoints = list(endpoint_date_columns.keys())  # List of all endpoint columns
    new_df = new_df.dropna(subset=endpoints, how='all')  # Drop rows where all endpoints are NaN

    return new_df


def extract_features(df: pd.DataFrame, smiles_column: str, feature_columns: List[str]) -> pd.DataFrame:
    """
    Extract features from the DataFrame.

    Args:
        df: The original DataFrame.
        smiles_column: Column name containing the SMILES strings.
        feature_columns: List of columns to be used as features.

    Returns:
        A DataFrame containing the SMILES and features.
    """
    return df[[smiles_column] + feature_columns]

def leaky_folds_endpoint_split(df: DataFrame, num_folds: int, smiles_column: str, endpoint_date_columns: Dict[str, str], exclude_columns: List[str], chemprop: bool, save_path: str, feature_columns: List[str] = None) -> List[Tuple[DataFrame, DataFrame]]:
    """
    Process a DataFrame by splitting it into multiple train/test sets for cross-validation, with the training set growing progressively.
    The size of the test set decreases with each fold, increasing the training data size.

    Args:
        df: DataFrame to be processed.
        num_folds: Number of folds for cross-validation.
        smiles_column: Name of the column containing compound identifiers.
        endpoint_date_columns: Dictionary of endpoint names to their respective date columns.
        chemprop: Boolean to indicate if data is for chemprop.
        save_path: Path to save the resulting dataframes.
        feature_columns: List of columns to be used as features. If None, exclude_columns will be used.

    Returns:
        List of tuples containing training and testing DataFrames for each fold.
    """
    splits = []
    df = expand_df_to_endpoints(df, endpoint_date_columns)

    # test comment
    for fold in range(1, num_folds + 1 ):
        split_size = 1 - (fold / (num_folds + 1))  # Decrease the test size progressively
        
        # Use the leaky_endpoint_split function to generate each fold's split
        train_df, test_df = leaky_endpoint_split(df, split_size, smiles_column, endpoint_date_columns, exclude_columns)
        
        if chemprop:
            if feature_columns is None:
                feature_columns = [col for col in df.columns if col not in [smiles_column, *endpoint_date_columns.keys(), *endpoint_date_columns.values(), *exclude_columns]]
            train_features = extract_features(train_df, smiles_column, feature_columns)
            test_features = extract_features(test_df, smiles_column, feature_columns)

            # Include smiles_column in the targets
            train_targets = train_df[[smiles_column] + list(endpoint_date_columns.keys())]
            test_targets = test_df[[smiles_column] + list(endpoint_date_columns.keys())]

            # Save features and targets
            train_features.to_csv(os.path.join(save_path, f'train_features_fold{fold}.csv'), index=False)
            test_features.to_csv(os.path.join(save_path, f'test_features_fold{fold}.csv'), index=False)
            train_targets.to_csv(os.path.join(save_path, f'train_targets_fold{fold}.csv'), index=False)
            test_targets.to_csv(os.path.join(save_path, f'test_targets_fold{fold}.csv'), index=False)
        else:
            train_df.to_csv(os.path.join(save_path, f'train_fold{fold}.csv'), index=False)
            test_df.to_csv(os.path.join(save_path, f'test_fold{fold}.csv'), index=False)


        splits.append((train_df, test_df))

    return splits