# dualPredictor/df_preprocess.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import KNNImputer

'''
This module, dualPredictor/df_preprocess.py, is designed to preprocess data frames prior to machine learning modeling.
It includes functions to ensure consistency between training and testing datasets and to perform data cleaning, encoding, scaling, and imputing missing values. 

1. check_df_forms(df_train, df_test):
   - Ensures that the training and testing DataFrames have the same columns in the same order. If not, it aligns both DataFrames to contain only the columns present in both.
   - Parameters:
     df_train (pandas.DataFrame): The training dataset.
     df_test (pandas.DataFrame): The testing dataset.
   - Returns:
     tuple: A tuple containing the processed training and testing DataFrames.

2. data_preprocessing(df, target_col, id_col=None, drop_cols=None, scaler=None, imputer=None):
   - Processes the DataFrame by optionally dropping specified columns, encoding categorical data, scaling numerical features, and imputing missing values. Provides a comprehensive preparation of the data for modeling.
   - Parameters:
     df (pandas.DataFrame): The DataFrame to preprocess.
     target_col (str): The name of the target column in the DataFrame.
     id_col (str, optional): The name of the column to set as index. Defaults to None.
     drop_cols (list of str, optional): List of column names to drop from the DataFrame. Defaults to None.
     scaler (object, optional): An instance of a scaler from sklearn (e.g., StandardScaler). If None, a new StandardScaler instance will be created and fitted. Defaults to None.
     imputer (object, optional): An instance of an imputer from sklearn (e.g., KNNImputer). If None, a new KNNImputer instance will be created and fitted. Defaults to None.
   - Returns:
     tuple: A tuple containing the preprocessed features (X), target (y), scaler, and imputer used.

These functions are vital for maintaining the integrity and quality of the data used in machine learning models, ensuring that the data is clean, consistent, and well-prepared for any analytical tasks.
'''


def check_df_forms(df_train, df_test):
    # Check if the DataFrames have the same columns in the same order
    if list(df_train.columns) == list(df_test.columns):
        print("Both DataFrames have the same columns in the same order.")
        return df_train, df_test

    # Find the overlap of columns between df_train and df_test
    common_cols = df_train.columns.intersection(df_test.columns)

    # Select the overlap of columns for both DataFrames
    df_train_processed = df_train[common_cols]
    df_test_processed = df_test[common_cols]

    # Print the number of columns kept and dropped for each DataFrame
    print(f"df_train: Kept {len(common_cols)} columns, Dropped {len(df_train.columns) - len(common_cols)} columns.")
    print(f"df_test: Kept {len(common_cols)} columns, Dropped {len(df_test.columns) - len(common_cols)} columns.")

    return df_train_processed, df_test_processed

# Example usage:
# df_train, df_test=check_df_forms(df_train, df_test)

def data_preprocessing(df, target_col, id_col=None, drop_cols=None, scaler=None, imputer=None):
    # Drop specified columns
    if drop_cols is not None:
        df = df.drop(columns=drop_cols)

    # Drop rows with missing values in the target column if this is a df_train (scaler = None)
    if scaler is None:
      df = df.dropna(subset=[target_col])

    # Set id_col as the index column
    if id_col is not None:
        df = df.set_index(id_col)

    # Split the data into features and target
    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # display the stats
    # print('Before the pre-processing')
    # display(X.describe())
    # display(y.describe())

    # Detect numerical and categorical columns
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()

    # Label encode categorical features
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
    
    # Scale numerical features
    if scaler is None:
        scaler = StandardScaler()
        X[num_cols] = scaler.fit_transform(X[num_cols])
    else:
        X[num_cols] = scaler.transform(X[num_cols])
    

    # Impute missing values
    if imputer is None:
        imputer = KNNImputer(n_neighbors=2,keep_empty_features=True)
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
        # display(X.shape)
    else:
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    X = X.set_index(df.index)

    return X, y,scaler,imputer
