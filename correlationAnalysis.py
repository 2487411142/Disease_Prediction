import pandas as pd
import pyreadstat

# Load the SAS file
file_path = 'adult_2023_sas/adult.sas7bdat'
df, meta = pyreadstat.read_sas7bdat(file_path)

# List of feature columns
selected_features = [
    "AC117V2", "AC174", "AC207", "AC208", "AB150","AC212", "AC81C",
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

# List of disease columns
disease_columns = ["AB154", "AB17", "AB22V2", "AB29V2", "AB34"]

# Initialize an empty DataFrame to store correlation results
correlation_results = pd.DataFrame(index=disease_columns, columns=selected_features)

# Compute correlation for each disease
for disease in disease_columns:
    df_filtered = df[selected_features + [disease]] # Filter dataset with selected columns
    correlation_matrix = df_filtered.corr(method="spearman") # Compute correlation matrix
    # Extract correlation with disease columns
    disease_corr = correlation_matrix[[disease]]

    # Drop disease columns themselves (if present)
    disease_corr = disease_corr.drop(index=disease, errors="ignore")

    correlation_results.loc[disease] = disease_corr[disease]

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)  # Increase width to prevent line breaks
# Display the final DataFrame
print(correlation_results)
