
import itertools as it
import time

from tqdm.auto import tqdm

import numpy as np
import pandas as pd

from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.metrics import cohen_kappa_score

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


def get_random_forest_hyperparams(n_samples, rf_n_estimators='auto', numeric=True, collin=False):

    # For 3000 samples or less, use 50 trees. Otherwise, stick to 10:
    if rf_n_estimators == 'auto':
        if n_samples >= 1000000:
            rf_n_estimators = 1 if collin else 2
        elif n_samples >= 10000:
            rf_n_estimators = 2 if collin else 5
        elif n_samples >= 3000:
            rf_n_estimators = 5 if collin else 10
        else:
            rf_n_estimators = 10 if collin else 50

    if numeric:
        if n_samples >= 5000:
            min_samples_leaf = np.ceil(0.01 * n_samples).astype(int)
        elif n_samples >= 500:
            min_samples_leaf = np.ceil(0.03 * n_samples).astype(int)
        else:
            min_samples_leaf = np.ceil(0.10 * n_samples).astype(int)

    else:
        min_samples_leaf = np.ceil(0.0025 * n_samples).astype(int)

    return rf_n_estimators, min_samples_leaf


def calc_numeric_features_target_corr(data_df, numeric_cols, master_columns_df, target_col, target_type='regression',
                                      rf_n_estimators='auto'):
    """
    Calculate the correlation between numeric features and the target
    variable.

    If the target variable is numeric (i.e., a regression problem), the
    Pearson correlation is calculated first.

    Then, a random forest model is run for each feature, with just that
    feature and the target variable. And the R^2 is reported as a proxy for
    correlation.

    Parameters
    ----------
    data_df : pd.DataFrame
        The input dataframe.

    numeric_cols : List
        A list of names of columns with numeric values (from the function
        'sort_numeric_nonnumeric_columns').

    target_col : str, default=None
        The name of the dataframe column containing the target variable.

    rf_n_estimators : int, default=10
        The number of separate trees to use when training the random forest
        model (in other words, this is the 'n_estimators' parameter in
        sklearn's RandomForestRegressor or RandomForestClassifier)

    Returns
    -------
    numeric_df : pd.DataFrame
        A dataframe with all numeric features and 3 different measures of
        their correlation with the target variable, for regression scenarios.
        For classification, ...
        The index of the dataframe is the feature/column names, and the
        columns are:
        - "Count not-Null": Number of non-null values for that feature.
        - "Pearson" [regression only]: The Pearson correlation between the
            feature and the target variable.
        - "Mutual Info" :
        - "Random Forest": The R^2 value when running a random forest model
            containing only this one feature and the target variable, using
            n_estimators=10.
    """

    rf_n_estimators, min_samples_leaf = get_random_forest_hyperparams(len(data_df), rf_n_estimators=rf_n_estimators)

    print('Running correlations of numeric features to target variable...')
    print('For random forest (RF) correlation measure, using {} trees and min_samples_leaf={}.\n'.format(
        rf_n_estimators, min_samples_leaf))

    if target_type == 'regression':
        numeric_df = pd.DataFrame(columns=["Count not-Null", "Pearson", "Mutual Info", "Random Forest"])
    else:
        numeric_df = pd.DataFrame(columns=["Count not-Null", "Mutual Info", "Random Forest"])

    # Loop over each numeric feature:
    for col in tqdm(numeric_cols):
        # Keep only rows that do not have NULL for that feature:
        data_df_col_notnull = data_df[[col, target_col]].dropna()

        if target_type == 'regression':
            # Calculate Pearson correlation between feature and target:
            pcorr = pearsonr(data_df_col_notnull[col].values, data_df_col_notnull[target_col].values)[0]
            # Calculate the Mutual Information for feature and target:
            minfo = mutual_info_regression(
                data_df_col_notnull[col].values.reshape(-1, 1), data_df_col_notnull[target_col].values)[0]

            # Train a random forest model with just that feature and the target variable:
            rf_reg = RandomForestRegressor(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
            rf_reg.fit(data_df_col_notnull[col].values.reshape(-1, 1), data_df_col_notnull[target_col].values)
            rfscore = rf_reg.score(data_df_col_notnull[col].values.reshape(-1, 1), data_df_col_notnull[target_col])

            # Save the results as a new row in the dataframe for output:
            numeric_df.loc[col] = len(data_df_col_notnull), round(pcorr, 2), round(minfo, 2), round(max(rfscore, 0), 2)

        else:
            # Calculate the Mutual Information for feature and target:
            minfo = mutual_info_classif(
                data_df_col_notnull[col].values.reshape(-1, 1), data_df_col_notnull[target_col].values)[0]

            # Train a random forest model with just that feature and the target variable:
            rf_class = RandomForestClassifier(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
            rf_class.fit(data_df_col_notnull[col].values.reshape(-1, 1), data_df_col_notnull[target_col].values)
            y_train_pred = rf_class.predict(data_df_col_notnull[col].values.reshape(-1, 1))
            rf_ck = max(cohen_kappa_score(data_df_col_notnull[target_col].values, y_train_pred), 0)

            # Save the results as a new row in the dataframe for output:
            numeric_df.loc[col] = len(data_df_col_notnull), round(minfo, 2), round(rf_ck, 2)
    print()

    master_columns_df.loc[numeric_df.index, numeric_df.columns] = numeric_df

    # The counts of NULL values should be integers:
    # numeric_df["Count not-Null"] = numeric_df["Count not-Null"].astype(int)

    # Sort the dataframe by the Random Forest R^2 for each feature, in
    # descending order:
    # numeric_df = numeric_df.sort_values(by=["Random Forest"], ascending=False)

    return master_columns_df


def calc_corr_numeric_features(data_df, numeric_cols, master_columns_df):
    """

    :param data_df:
    :param numeric_cols:
    :return:
    """

    rf_n_estimators, min_samples_leaf = get_random_forest_hyperparams(len(data_df), collin=True)

    print('Running correlations between numeric features...')
    print('For random forest (RF) correlation measure, using {} trees and min_samples_leaf={}.\n'.format(
        rf_n_estimators, min_samples_leaf))

    numeric_collinear_df = pd.DataFrame(columns=["Feature1", "Feature2", "Count not-Null", "Pearson", "Random Forest"])

    jj = 0
    total_iters = len(list(it.combinations(numeric_cols, 2)))
    for pair in tqdm(it.combinations(numeric_cols, 2), total=total_iters):
        col1, col2 = pair[0], pair[1]

        data_df_cols_notnull = data_df[[col1, col2]].dropna()

        pcorr = pearsonr(data_df_cols_notnull[col1].values, data_df_cols_notnull[col2].values)[0]

        rf_reg = RandomForestRegressor(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
        rf_reg.fit(data_df_cols_notnull[col1].values.reshape(-1, 1), data_df_cols_notnull[col2].values)
        rfscore1 = max(rf_reg.score(data_df_cols_notnull[col1].values.reshape(-1, 1), data_df_cols_notnull[col2]), 0)

        rf_reg = RandomForestRegressor(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
        rf_reg.fit(data_df_cols_notnull[col2].values.reshape(-1, 1), data_df_cols_notnull[col1].values)
        rfscore2 = max(rf_reg.score(data_df_cols_notnull[col2].values.reshape(-1, 1), data_df_cols_notnull[col1]), 0)

        numeric_collinear_df.loc[jj] = col1, col2, len(data_df_cols_notnull), round(pcorr, 2), round((rfscore1+rfscore2)/2, 2)

        jj += 1

    numeric_collinear_df = numeric_collinear_df.sort_values(by=["Random Forest"], ascending=False)

    numeric_collinear_summary_df = pd.DataFrame(
        columns=["COLLIN Avg Pearson Corr", "COLLIN Avg RF Corr", "COLLIN Max Pear Corr Feature", "COLLIN Max Pear",
                 "COLLIN Max RF Corr Feature", "COLLIN Max RF Corr"])

    for col in numeric_cols:
        numeric_collinear_df_col = numeric_collinear_df.loc[
            (numeric_collinear_df["Feature1"] == col) | (numeric_collinear_df["Feature2"] == col)]

        pn_xx = np.argmax(np.abs(numeric_collinear_df_col["Pearson"].values))
        max_corr_feat1, max_corr_feat2 = numeric_collinear_df_col[["Feature1", "Feature2"]].iloc[pn_xx]
        max_pn_corr_feat = max_corr_feat1 if max_corr_feat1 != col else max_corr_feat2

        rf_xx = np.argmax(numeric_collinear_df_col["Random Forest"].values)
        max_corr_feat1, max_corr_feat2 = numeric_collinear_df_col[["Feature1", "Feature2"]].iloc[rf_xx]
        max_rf_corr_feat = max_corr_feat1 if max_corr_feat1 != col else max_corr_feat2

        numeric_collinear_summary_df.loc[col] = (
            round(np.mean(np.abs(numeric_collinear_df_col["Pearson"].values)), 2),
            round(numeric_collinear_df_col["Random Forest"].mean(), 2), max_pn_corr_feat,
            numeric_collinear_df_col["Pearson"].iloc[pn_xx], max_rf_corr_feat,
            numeric_collinear_df_col["Random Forest"].iloc[rf_xx])
    
    master_columns_df.loc[
        numeric_collinear_summary_df.index, numeric_collinear_summary_df.columns] = numeric_collinear_summary_df

    # numeric_collinear_summary_df = numeric_collinear_summary_df.sort_values(by=["Max RF Corr"], ascending=False)

    return numeric_collinear_df, master_columns_df


def calc_max_rfscore(num=2):
    """
    Calculate the theoretical maximum R^2 score one could expect for a given
    number of unique values for a categorical feature.

    The idea behind this calculation is that, say one had a target variable
    that ranged from 0 to 1. If a categorical variable has only two unique
    values, say 'yes' and 'no', then the best-case scenario is that the target
    variable equals somewhere between 0 and 0.5 for 'yes' and between 0.5 and
    1 for 'no'. If we assume a uniform distribution of values for the target
    variable between 0 and 1, then we could say a value of 'yes' predicts a
    target value of 0.25, and a value of 'no' predicts a value of 0.75. So,
    the R^2 score in this case works out to be 0.75.

    If instead, we had 10 unique values for a categorical variable, then a
    best-case scenario, would be 'categorical_value_1' predicts a value
    between 0 and 0.1, 'categorical_value_2' predicts a value between 0.2 and
    0.3, etc. In this case, the R^2 score works out to be 0.99.

    So, this function gives us this maximum value, so we can adjust all
    categorical features' R^2 scores to be roughly on the same scale.

    Parameters
    ----------
    num : int
        The number of unique values for a categorical feature.

    Returns
    -------
    r2 : float
        The theoretical maximum R^2 for the given number of unique values.
    """
    y = np.arange(0, 1.001, 0.001)
    y_pred = np.zeros(1001)

    split = 1 / float(num)
    split_mid = split / 2

    for jj in range(num):
        if jj < num - 1:
            y_pred[int(jj*split*1000):int((jj+1)*split*1000)] = split_mid + jj*split
        else:
            y_pred[int(jj*split*1000):] = split_mid + jj*split

    r2 = (1 - ((y - y_pred)**2).sum() / ((y - 0.5)**2).sum())

    return r2


def calc_nonnumeric_features_target_corr(data_df, non_numeric_cols, master_columns_df, target_col,
                                         target_type='regression'):
    """
    Calculate the correlation between non-numeric features and the target
    variable.

    To do this, a random forest model is run for each feature, with just that
    feature and the target variable. And the R^2 is reported as a proxy for
    correlation.

    Parameters
    ----------
    data_df : pd.DataFrame
        The input dataframe.

    non_numeric_cols : List
        A list of names of columns with non-numeric values.

    target_col : str, default=None
        The name of the dataframe column containing the target variable.

    rf_n_estimators : int, default=10
        The number of separate trees to use when training the random forest
        model (in other words, this is the 'n_estimators' parameter in
        sklearn's RandomForestRegressor or RandomForestClassifier)

    Returns
    -------
    non_numeric_df : pd.DataFrame
        A dataframe with all non-numeric/categorical features and a measure of
        their correlation with the target variable. The index of the dataframe
        is the feature/column names, and the columns are:
        - "Count not-Null": Number of non-null values for that feature.
        - "Num Unique": The number of unique values in that data column.
        - "Random Forest": The R^2 value when running a random forest model
            containing only this one feature and the target variable, using
            n_estimators=10. To be precise, each feature is split into
            multiple features for the random forest training using one-hot
            encoding.
        - "RF_norm": In a regression problem, the greater number of unique
            values that a categorical variable has will have a higher
            theoretical maximum R^2, so this R^2 is adjusted to more easily
            compare categorical features with different number of unique
            values (see documentation for further explanation).
    """

    rf_n_estimators, min_samples_leaf = get_random_forest_hyperparams(len(data_df), rf_n_estimators='auto',
                                                                      numeric=False)

    print('Running correlations of non-numeric features to target variable...')
    print('For random forest (RF) correlation measure, using {} trees and min_samples_leaf={}.\n'.format(
        rf_n_estimators, min_samples_leaf))

    if target_type == 'regression':
        non_numeric_df = pd.DataFrame(columns=["Count not-Null", "Mutual Info", "Random Forest", "RF_norm"])
    else:
        non_numeric_df = pd.DataFrame(columns=["Count not-Null", "Mutual Info", "Random Forest", "RF_norm"])

    # Loop over each categorical feature:
    for col in tqdm(non_numeric_cols):
        # Keep only rows that do not have NULL for that feature:
        train_col_notnull = data_df[[col, target_col]].dropna()

        # Split the feature into multiple features for the random forest
        # training using one-hot encoding:
        X_col = pd.get_dummies(train_col_notnull[col], dtype=int)

        if target_type == 'regression':
            # Calculate the Mutual Information for feature and target:
            minfo = mutual_info_regression(
                LabelEncoder().fit_transform(train_col_notnull[col]).reshape(-1, 1),
                train_col_notnull[target_col].values, discrete_features=True)[0]

            # Train a random forest model:
            rf_reg = RandomForestRegressor(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
            rf_reg.fit(X_col, train_col_notnull[target_col].values)
            rfscore = max(rf_reg.score(X_col, train_col_notnull[target_col]), 0)

            # The number of unique values is calculated for the purpose of
            # adjusting the Random Forest R^2:
            num_uniq = master_columns_df.loc[col, "Num Unique Values"]
            # Adjust the R^2 based on the number of unique values affecting a
            # feature's maximum theoretical R^2:
            rfscore_norm = rfscore * (1 / calc_max_rfscore(num_uniq))

            # Save the results as a new row in the dataframe for output:
            non_numeric_df.loc[col] = len(train_col_notnull), round(minfo, 2), round(rfscore, 2), round(rfscore_norm, 2)

        else:
            minfo = mutual_info_classif(LabelEncoder().fit_transform(train_col_notnull[col]).reshape(-1, 1),
                                        train_col_notnull[target_col].values, discrete_features=True)[0]

            # Train a random forest model with just that feature and the target variable:
            rf_class = RandomForestClassifier(n_estimators=rf_n_estimators, min_samples_leaf=min_samples_leaf)
            rf_class.fit(X_col, train_col_notnull[target_col].values)
            y_train_pred = rf_class.predict(X_col)
            rf_ck = max(cohen_kappa_score(train_col_notnull[target_col].values, y_train_pred), 0)

            # Save the results as a new row in the dataframe for output:
            num_uniq = master_columns_df.loc[col, "Num Unique Values"]
            non_numeric_df.loc[col] = len(train_col_notnull), round(minfo, 2), round(rf_ck, 2), round(rf_ck, 2)
    print()

    master_columns_df.loc[non_numeric_df.index, non_numeric_df.columns] = non_numeric_df
    
    # The counts of NULL values and unique values should be integers:
    # non_numeric_df["Count not-Null"] = non_numeric_df["Count not-Null"].astype(int)
    # non_numeric_df["Num Unique"] = non_numeric_df["Num Unique"].astype(int)

    # Sort the dataframe by the adjusted Random Forest R^2 for each feature,
    # in descending order:
    # non_numeric_df = non_numeric_df.sort_values(by=["RF_norm"], ascending=False)

    return master_columns_df

