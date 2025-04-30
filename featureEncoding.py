import os
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

import pyreadstat
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold, train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, SVMSMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import matplotlib.pyplot as plt

# Load the SAS file
def load_data(file_path):
    df, meta = pyreadstat.read_sas7bdat(file_path)
    return df

# Delete Proxy Skipped data
def drop_proxy_skipped(df):
    df = df.drop(df[df.AJ31 == -2].index)
    return df

def drop_dont_know(df, target_columns):
    df = df.copy()
    for col in target_columns:
        df = df[df[col] != 3]
        df[col] = df[col].replace({1: 0, 2: 1})
    return df

def multi_target_encode_kfold(data, features, target, n_splits=5, seed=42):
    df = data.copy()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    encoding_maps = {}

    for feature in features:
        col_encoded = feature + '_te'
        df[col_encoded] = np.nan

        for train_idx, valid_idx in kf.split(df):
            train_fold, valid_fold = df.iloc[train_idx], df.iloc[valid_idx]
            means = train_fold.groupby(feature)[target].mean()
            df.loc[df.index[valid_idx], col_encoded] = df.loc[df.index[valid_idx], feature].map(means)

        encoding_maps[feature] = df.groupby(feature)[target].mean().to_dict()

    return df, encoding_maps


def preprocess_features(df, target_column):
    df = df.copy()


    social2_map = {
        -1: 0,
        0: 0,
        1: 1,
        2: 2,
    }
    df['SOCIAL2_encoded'] = df['SOCIAL2'].map(social2_map)


    numcig_map = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5
    }
    df['NUMCIG_encoded'] = df['NUMCIG'].map(numcig_map)

 
    ac208_map = {
        0: 3,  # Never
        1: 0,
        2: 1,
        3: 2
    }
    df['AC208_encoded'] = df['AC208'].map(ac208_map)

    ae15a_map = {
        1: 2,
        2: 1,
        3: 0,
        -1: 0
    }
    df['AE15A_encoded'] = df['AE15A'].map(ae15a_map)


    df['MARIT_encoded'] = df['MARIT'].replace({1: 0, 2: 1, 3: 2})


    aj29_map = {
        1: 5,
        2: 4,
        3: 3,
        4: 2,
        5: 1
    }
    df['AJ29_encoded'] = df['AJ29'].map(aj29_map)

   
    ac117v2_days_map = {
        -1: 0,
        1: 0,
        2: 1.5,
        3: 4,
        4: 7.5,
        5: 15,
        6: 25,
        7: 30
    }
    df['AC117V2_days'] = df['AC117V2'].map(ac117v2_days_map)


    srage_map = {
        18: 21.5,
        26: 27.5,
        30: 32,
        35: 37,
        40: 42,
        45: 47,
        50: 52,
        55: 57,
        60: 62,
        65: 67,
        70: 72,
        75: 77,
        80: 82,
        85: 87
    }
    df['SRAGE_encoded'] = df['SRAGE_P1'].map(srage_map)

 
    rbmi_map = {
        1: 0,  # UNDERWEIGHT
        2: 1,  # NORMAL
        3: 2,  # OVERWEIGHT
        4: 3  # OBESE
    }
    df['RBMI_encoded'] = df['RBMI'].map(rbmi_map)

   
    high_card_features = ['OCCMAIN2', 'OMBSRR_P1', 'HOUSETYPE']
    for col in high_card_features:
        df[col] = df[col].replace(99, np.nan)

    df_encoded, encoding_maps = multi_target_encode_kfold(
        data=df,
        features=high_card_features,
        target=target_column
    )

    for col in high_card_features:
        df[col + '_te'] = df_encoded[col + '_te']

    return df, encoding_maps


def run_multiple_targets(df, target_list, model_func):
    results = {}
    for target in target_list:
        print(f"\n================ {target} ================")
        df_target = drop_dont_know(df, target_columns=[target])
        try:
            model = model_func(df_target, target)
            results[target] = model
        except Exception as e:
            print(f"Error training {target}: {e}")
    return results

def cross_validate_random_forest(df, target_column, cv=5, random_state=42, smote_type='borderline'):
    df_processed, _ = preprocess_features(df, target_column)
    features = [col for col in df_processed.columns if col not in [target_column] and not col.startswith(tuple(['NUMCIG', 'AC208', 'AE15A', 'AJ29', 'AC117V2', 'SRAGE', 'RBMI', 'OCCMAIN2', 'OMBSRR_P1', 'HOUSETYPE'])) or col.endswith('_encoded') or col.endswith('_te') or col.endswith('_days')]

    df_model = df_processed[features + [target_column]].dropna()
    if df_model.shape[0] == 0:
        raise ValueError("No data left after dropping missing values.")

    X = df_model.drop(columns=target_column)
    y = df_model[target_column]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)

    if smote_type == 'regular':
        smote = SMOTE(random_state=random_state)
    elif smote_type == 'borderline':
        smote = BorderlineSMOTE(random_state=random_state)
    elif smote_type == 'svm':
        smote = SVMSMOTE(random_state=random_state)
    else:
        raise ValueError("Invalid smote_type. Use 'regular', 'borderline', or 'svm'")

    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    model = RandomForestClassifier(random_state=random_state, class_weight='balanced')
    model.fit(X_train_res, y_train_res)

    y_train_pred = model.predict(X_train_res)
    y_train_prob = model.predict_proba(X_train_res)[:, 1]
    y_val_pred = model.predict(X_val)
    y_val_prob = model.predict_proba(X_val)[:, 1]

    train_acc = accuracy_score(y_train_res, y_train_pred)
    train_auc = roc_auc_score(y_train_res, y_train_prob)
    val_acc = accuracy_score(y_val, y_val_pred)
    val_auc = roc_auc_score(y_val, y_val_prob)

    print("Train Accuracy:", round(train_acc, 4), "AUC:", round(train_auc, 4))
    print("Val Accuracy:", round(val_acc, 4), "AUC:", round(val_auc, 4))
    print("\nTrain classification report:")
    print(classification_report(y_train_res, y_train_pred))
    print("\nVal classification report:")
    print(classification_report(y_val, y_val_pred))

    return model

def cross_validate_xgb_depth1(df, target_column, random_state=42):
    df_processed, _ = preprocess_features(df, target_column)
    features = [col for col in df_processed.columns if col not in [target_column] and not col.startswith(tuple(['NUMCIG', 'AC208', 'AE15A', 'AJ29', 'AC117V2', 'SRAGE', 'RBMI', 'OCCMAIN2', 'OMBSRR_P1', 'HOUSETYPE'])) or col.endswith('_encoded') or col.endswith('_te') or col.endswith('_days')]

    df_model = df_processed[features + [target_column]].dropna()
    if df_model.shape[0] == 0:
        raise ValueError("No data left after dropping missing values.")

    X = df_model.drop(columns=target_column)
    y = df_model[target_column]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=random_state, stratify=y)

    smote = BorderlineSMOTE(random_state=random_state)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    model = XGBClassifier(max_depth=1, eval_metric='logloss', objective='binary:logistic', random_state=random_state)
    model.fit(X_train_res, y_train_res)

    y_train_pred = model.predict(X_train_res)
    y_train_prob = model.predict_proba(X_train_res)[:, 1]
    y_val_pred = model.predict(X_val)
    y_val_prob = model.predict_proba(X_val)[:, 1]

    train_acc = accuracy_score(y_train_res, y_train_pred)
    train_auc = roc_auc_score(y_train_res, y_train_prob)
    val_acc = accuracy_score(y_val, y_val_pred)
    val_auc = roc_auc_score(y_val, y_val_prob)

    print("Train Accuracy:", round(train_acc, 4), "AUC:", round(train_auc, 4))
    print("Val Accuracy:", round(val_acc, 4), "AUC:", round(val_auc, 4))
    print("\nTrain classification report:")
    print(classification_report(y_train_res, y_train_pred))
    print("\nVal classification report:")
    print(classification_report(y_val, y_val_pred))

    return model


if __name__ == "__main__":
    PATH = 'ADULT SAS/adult.sas7bdat'

    # List of feature columns
    SELECTED_FEATURES = [
        "AC117V2", "AC174", "AC207", "AC208", "AC212", "AC81C",
        "AD13V2", "AD32_P1", "AE15A", "AE7V2", "AF81",
        "AJ29", "AJ30", "AJ31", "AJ32", "AJ33", "AJ34",
        "DSTRS12", "DSTRSYR", "DISABILITY", "BINGE30",
        "ESMKCUR", "HOUSETYPE", "AQ1", "AQ12",
        "MARCUR", "MAREXPOSE", "MARIT", "MARIT2", "MARIT_45",
        "NUMCIG", "OCCMAIN2", "OMBSRR_P1",
        "RBMI", "SMKEXPOSE",
        "SMOKING", "SOCIAL2", "SRAGE_P1", "SRSEX",
        "TOBCUR", "UR_CLRT4", "WGHTK_P"
    ]

    DISEASE_COLUMNS = ["AB154", "AB17", "AB22V2", "AB29V2", "AB34"]
    df = load_data(PATH)
    data = df[SELECTED_FEATURES+DISEASE_COLUMNS]
    data = drop_proxy_skipped(data)

    run_multiple_targets(
        data,
        target_list=["AB154", "AB17", "AB22V2", "AB29V2", "AB34"],
        model_func=cross_validate_xgb_depth1
    )



